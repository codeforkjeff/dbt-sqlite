
import decimal
from typing import List, Optional, Set

import agate
from dbt.adapters.base import available
from dbt.adapters.base.relation import BaseRelation, InformationSchema
from dbt.adapters.sql import SQLAdapter
from dbt.adapters.sqlite import SQLiteConnectionManager
from dbt.adapters.sqlite.relation import SQLiteRelation
from dbt.contracts.graph.manifest import Manifest
from dbt.exceptions import NotImplementedException


class SQLiteAdapter(SQLAdapter):
    ConnectionManager = SQLiteConnectionManager

    Relation = SQLiteRelation

    @classmethod
    def date_function(cls):
        return 'date()'

    def get_live_relation_type(self, relation):
        """
        returns the type of relation (table, view) from the live database
        """
        sql = f"SELECT type as data_type FROM { relation.schema }.sqlite_master WHERE name = '{relation.identifier}'"
        result = self.connections.execute(sql, fetch=True)
        data_type = result[1].rows[0][0]
        return data_type

    def rename_relation(self, from_relation, to_relation):
        """
        Override method instead of calling the macro in adapters.sql
        because renaming views is complicated
        """
        self.cache_renamed(from_relation, to_relation)

        existing_relation_type = from_relation.type

        if existing_relation_type == 'table':

            self.connections.execute(f"ALTER TABLE {from_relation} RENAME TO {to_relation.identifier}")

        elif existing_relation_type == 'view':

            result = self.connections.execute(f"""
                SELECT sql FROM {from_relation.schema}.sqlite_master
                WHERE type = 'view' and name = '{from_relation.identifier}'
                """, fetch=True)

            definition = result[1].rows[0][0]

            self.connections.execute(f"DROP VIEW {from_relation}")

            self.connections.execute(f"DROP VIEW IF EXISTS {to_relation}")

            new_definition = definition.replace(from_relation.identifier, f"{to_relation}", 1)

            self.connections.execute(new_definition)

        else:
            raise NotImplementedException(
                f"I don't know how to rename this type of relation: {from_relation.type}," +
                f" from: {from_relation}, to: {to_relation}")

    def list_schemas(self, database: str) -> List[str]:
        """
        Schemas in SQLite are attached databases
        """
        results = self.connections.execute("PRAGMA database_list", fetch=True)
        
        schemas = [row[1] for row in results[1]]

        return schemas

    def check_schema_exists(self, database: str, schema: str) -> bool:
        return schema in self.list_schemas(database)

    def get_columns_in_relation(self, relation):
        _, results = self.connections.execute(f"pragma {relation.schema}.table_info({relation.identifier})", fetch=True)

        new_rows = []
        for row in results:
            new_row = [
                row[1],
                row[2] or 'TEXT',
                None,
                None,
                None
            ]
            new_rows.append(new_row)

        column_names = [
            'column_name',
            'data_type',
            'character_maximum_length',
            'numeric_precision',
            'numeric_scale'
        ]

        table = agate.Table(new_rows, column_names)

        kwargs = {
            'table': table
        }

        result = self.execute_macro(
            'sql_convert_columns_in_relation',
            kwargs=kwargs
        )
        return result

    def _get_one_catalog(
        self,
        information_schema: InformationSchema,
        schemas: Set[str],
        manifest: Manifest,
    ) -> agate.Table:
        """
        bad form to override this method but...
        """

        # this does N+1 queries but there doesn't seem to be
        # any other way to do this

        rows = []
        for schema in schemas:
            # TODO: violates DRY but I couldn't figure out how to get
            # a BaseRelation object to pass into
            # list_relations_without_caching()
            sql = f"""SELECT
                '{ information_schema.database }' as database
                ,name
                ,'{ schema }' AS schema
                ,type as data_type
            FROM
                { schema }.sqlite_master
            WHERE
                name NOT LIKE 'sqlite_%'
            """

            results = self.connections.execute(sql, fetch=True)

            for relation_row in results[1]:
                name = relation_row['name']
                relation_type = relation_row['data_type']

                table_info = self.connections.execute(
                    f"pragma {schema}.table_info({name})", fetch=True)

                for table_row in table_info[1]:
                    rows.append([
                        information_schema.database,
                        schema,
                        name,
                        relation_type,
                        '',
                        '',
                        table_row['name'],
                        table_row['cid'],
                        table_row['type'] or 'TEXT',
                        ''
                    ])

        column_names = [
            'table_database',
            'table_schema',
            'table_name',
            'table_type',
            'table_comment',
            'table_owner',
            'column_name',
            'column_index',
            'column_type',
            'column_comment'
        ]
        table = agate.Table(rows, column_names)

        results = self._catalog_filter_table(table, manifest)
        return results

    def get_rows_different_sql(
        self,
        relation_a: BaseRelation,
        relation_b: BaseRelation,
        column_names: Optional[List[str]] = None,
        except_operator: str = 'EXCEPT',
    ) -> str:
        # This method only really exists for test reasons.
        names: List[str]
        if column_names is None:
            columns = self.get_columns_in_relation(relation_a)
            names = sorted((self.quote(c.name) for c in columns))
        else:
            names = sorted((self.quote(n) for n in column_names))
        columns_csv = ', '.join(names)

        # difference from base class: sqlite requires SELECTs around UNION
        # queries
        COLUMNS_EQUAL_SQL = '''
        with diff_count as (
            SELECT
                1 as id,
                COUNT(*) as num_missing FROM (
                    SELECT * FROM
                    (SELECT {columns} FROM {relation_a} {except_op}
                     SELECT {columns} FROM {relation_b}) t1
                     UNION ALL
                    SELECT * FROM
                    (SELECT {columns} FROM {relation_b} {except_op}
                     SELECT {columns} FROM {relation_a}) t2
                ) as a
        ), table_a as (
            SELECT COUNT(*) as num_rows FROM {relation_a}
        ), table_b as (
            SELECT COUNT(*) as num_rows FROM {relation_b}
        ), row_count_diff as (
            select
                1 as id,
                table_a.num_rows - table_b.num_rows as difference
            from table_a, table_b
        )
        select
            row_count_diff.difference as row_count_difference,
            diff_count.num_missing as num_mismatched
        from row_count_diff
        join diff_count using (id)
        '''.strip()

        sql = COLUMNS_EQUAL_SQL.format(
            columns=columns_csv,
            relation_a=str(relation_a),
            relation_b=str(relation_b),
            except_op=except_operator,
        )

        return sql

    def _transform_seed_value(self, value):
        new_value = value
        if isinstance(value, decimal.Decimal):
            new_value = str(value)
        return new_value

    @available
    def transform_seed_row(self, row):
        """
        sqlite3 chokes on Decimal values (emitted by agate) in
        bound values so convert those to strings. there may be other
        types that need to be added here.

        This is the error that comes up:
        "Error binding parameter 0 - probably unsupported type."

        see dbt.clients.agate_helper.build_type_tester() for the
        TypeTester passed to agate when parsing CSVs.

        """
        return [self._transform_seed_value(value) for value in row]

    def timestamp_add_sql(
        self, add_to: str, number: int = 1, interval: str = 'hour'
    ) -> str:
        return f"DATETIME({add_to}, '{number} {interval}')"

    def drop_schema(self, relation: BaseRelation) -> None:
        super().drop_schema(relation)

        # never detach main
        if relation.schema != 'main':
            self.connections.execute(f"DETACH DATABASE {relation.schema}")
