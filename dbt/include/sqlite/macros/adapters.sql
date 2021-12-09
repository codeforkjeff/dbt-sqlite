{% macro sqlite__list_schemas(database) %}
    {% call statement('list_schemas', fetch_result=True) %}
        pragma database_list
    {% endcall %}
    {% set results = load_result('list_schemas').table %}
    {{ return(results.select(['name']).rename(column_names = {'name': 'schema'})) }}
{% endmacro %}

{% macro sqlite__create_schema(relation, auto_begin=False) %}
  {% set path = [ adapter.config.credentials.schema_directory, relation.without_identifier().include(database=False) | string + '.db' ] | join('/') %}
  {%- call statement('create_schema') -%}
    attach database '{{ path }}' as {{ relation.without_identifier().include(database=False) }}
  {%- endcall -%}
{% endmacro %}

{% macro sqlite__drop_schema(relation) -%}
  {# drop all tables in the schema; detaching happens in the adapter class #}

  {% set relations_in_schema = list_relations_without_caching(relation.without_identifier()) %}

  {% for row in relations_in_schema %}
      {%- call statement('drop_relation_in_schema') -%}
        drop {{ row.data_type}} {{ row.schema }}.{{ row.name }}
      {%- endcall -%}
  {% endfor %}
{% endmacro %}

{% macro sqlite__drop_relation(relation) -%}
    {% call statement('drop_relation', auto_begin=False) -%}
        drop {{ relation.type }} if exists {{ relation }}
    {%- endcall %}
{% endmacro %}

{% macro sqlite__truncate_relation(relation) -%}
    {% call statement('truncate_relation') -%}
        delete from {{ relation }}
    {%- endcall %}
{% endmacro %}

{% macro sqlite__check_schema_exists(information_schema, schema) -%}
    {% if schema in list_schemas(database).columns[0].values() %}
        {% call statement('check_schema_exists', fetch_result=True) %}
            SELECT 1 as schema_exist
        {% endcall %}
        {{ return(load_result('check_schema_exists').table) }}
    {% else %}
        {% call statement('check_schema_exists', fetch_result=True) %}
            SELECT 0 as schema_exist
        {% endcall %}
        {{ return(load_result('check_schema_exists').table) }}
    {% endif %}
{% endmacro %}

{% macro sqlite__list_relations_without_caching(schema_relation) %}

    {% set schemas = list_schemas(schema_relation.database).columns[0].values() %}

    {% if schema_relation.schema in schemas %}
        {% call statement('list_relations_without_caching', fetch_result=True) %}
            SELECT
                '{{ schema_relation.database }}' as database
                ,name
                ,'{{ schema_relation.schema }}' AS schema
                ,type as data_type
            FROM
                {{ schema_relation.schema }}.sqlite_master
            WHERE
                name NOT LIKE 'sqlite_%'
        {% endcall %}

        {{ return(load_result('list_relations_without_caching').table) }}
    {% else %}
        {% call statement('empty_table', fetch_result=True) %}
            SELECT null as database, null as name, null as schema, null as data_type WHERE 1=0
        {% endcall %}

        {{ return(load_result('empty_table').table) }}
    {% endif %}
{% endmacro %}

{% macro sqlite__create_table_as(temporary, relation, sql) -%}
      create {% if temporary -%}
        temporary
      {%- endif %} table {{ relation }}
      as
        {{ sql }}
{% endmacro %}

{% macro sqlite__create_view_as(relation, sql, auto_begin=False) -%}
    create view {{ relation }} as
    {{ sql }};
{%- endmacro %}

{% macro sqlite__rename_relation(from_relation, to_relation) -%}
  {# no-op #}  
  {# see SQLiteAdapter.rename_relation() #}
{% endmacro %}

{% macro sqlite__snapshot_get_time() -%}
  datetime()
{%- endmacro %}

{% macro sqlite__snapshot_string_as_time(timestamp) -%}
    {# just return the string; SQLite doesn't have a timestamp data type per se #}
    {{ return("'" + timestamp|string + "'") }}
{%- endmacro %}

{#
the only allowable schema for temporary tables in SQLite is 'temp', so set
that here when making the relation and everything else should Just Work
#}
{% macro sqlite__make_temp_relation(base_relation, suffix) %}
    {% set tmp_identifier = base_relation.identifier ~ suffix %}
    {% set tmp_relation = base_relation.incorporate(
                                path={"schema": "temp", "identifier": tmp_identifier}) -%}

    {% do return(tmp_relation) %}
{% endmacro %}

{% macro sqlite__current_timestamp() -%}
  datetime()
{%- endmacro %}
