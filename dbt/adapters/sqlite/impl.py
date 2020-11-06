
from typing import List, Set

import agate
from dbt.adapters.base.relation import BaseRelation, InformationSchema
from dbt.adapters.sql import SQLAdapter
from dbt.adapters.sqlite import SQLiteConnectionManager
from dbt.contracts.graph.manifest import Manifest
from dbt.exceptions import NotImplementedException


class SQLiteAdapter(SQLAdapter):
    ConnectionManager = SQLiteConnectionManager

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

        # can't use from_relation.type b/c that reflects the project files, not actual state of db.
        # I'm not sure why this is needed, since other postgres and others odn't seem to have
        # this issue. this may be a patch for something else that's not working quite right
        # in this adapter.
        existing_relation_type = self.get_live_relation_type(from_relation)

        if existing_relation_type == 'table':

            # this is complicated:
            #
            # sqlite doesn't support DROP CASCADE. this means after it renames a table to a 'backup',
            # (which updates references in views, like postgres does), dropping the backup won't drop
            # the dependent views. the views remain, with "bad" references, and sqlite doesn't throw an
            # error. when dbt tries to "rename" a view by dropping/re-creating its definition containing
            # a bad reference, sqlite throws an error about the backup table not existing.
            #
            # workaround: use the legacy_alter_table pragma, so that when a table is renamed, views don't
            # get their references auto-updated. this is gross non-standard behavior but it preserves the
            # integrity of the downstream view, so it can be backed up. there may still be other problems
            # (e.g. if you delete a table entirely from the project.)
            #
            # I think the real fix is to implement DROP CASCADE behavior in drop_relation

            self.connections.execute(f"PRAGMA legacy_alter_table=ON")

            self.connections.execute(f"ALTER TABLE {from_relation.schema}.{from_relation.identifier} RENAME TO {to_relation.identifier}")
        elif existing_relation_type == 'view':
            result = self.connections.execute(f"""
                SELECT sql FROM {from_relation.schema}.sqlite_master WHERE type = 'view' and name = '{from_relation.identifier}'
                """, fetch=True)

            definition = result[1].rows[0][0]

            self.connections.execute(f"DROP VIEW {from_relation.schema}.{from_relation.identifier}");

            self.connections.execute(f"DROP VIEW IF EXISTS {to_relation.schema}.{to_relation.identifier}");

            new_definition = definition.replace(from_relation.identifier, f"{to_relation.schema}.{to_relation.identifier}", 1)

            self.connections.execute(new_definition)

        else:
            raise NotImplementedException(f"I don't know how to rename this type of relation: {from_relation.type}, from: {from_relation}, to: {to_relation}")

    def list_schemas(self, database: str) -> List[str]:
        """
        Schemas in SQLite are attached databases
        """
        results = self.connections.execute("PRAGMA database_list", fetch=True)
        
        schemas = [row[1] for row in results[1]]

        return schemas

    def check_schema_exists(self, database: str, schema: str) -> bool:
        return schema in self.list_schemas(database)

    def create_schema(self, relation: BaseRelation) -> None:
        raise NotImplementedException(
            '`create_schema` is not implemented for SQLite adapter, it should never be called'
        )

    def get_columns_in_relation(self, relation):

        results = self.connections.execute(f"pragma {relation.schema}.table_info({relation.identifier})", fetch=True)

        # TODO: transform this using agate table

        print(results)

        # column_name
        # , data_type
        # , character_maximum_length
        # , numeric_precision
        # , numeric_scale

        raise NotImplementedException(
                '`get_columns_in_relation` needs to be implemented for SQLite adapter'
            )

        # what does sql_convert_columns_in_relation macro do?

        # return(results)

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
                relation_type= relation_row['data_type']

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
