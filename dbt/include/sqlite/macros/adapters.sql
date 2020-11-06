{% macro sqlite__list_schemas(database) %}
    {# no-op #}
    {# see SQLiteAdapter.list_schemas() #}
{% endmacro %}

{% macro sqlite__create_schema(database_name, schema_name, auto_begin=False) %}
    {# no-op #}
    {# see SQLiteAdapter.create_schema() #}
{% endmacro %}

{% macro sqlite__drop_relation(relation) -%}
    {% call statement('drop_relation', auto_begin=False) -%}
        drop {{ relation.type }} if exists {{ relation.schema }}.{{ relation.identifier }}
    {%- endcall %}
{% endmacro %}

{% macro sqlite__truncate_relation(relation) -%}
    {% call statement('truncate_relation') -%}
        delete from {{ relation.schema }}.{{ relation.identifier }}
    {%- endcall %}
{% endmacro %}

{% macro sqlite__check_schema_exists(database, schema) -%}
    {# no-op #}
    {# see SQLiteAdapter.check_schema_exists() #}
{% endmacro %}

{% macro sqlite__list_relations_without_caching(schema_relation) %}
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
{% endmacro %}

{% macro sqlite__create_table_as(temporary, relation, sql) -%}
      create {% if temporary -%}
        temporary
      {%- endif %} table {{ relation.schema }}.{{ relation.identifier }}
      as
        {{ sql }}
{% endmacro %}

{% macro sqlite__create_view_as(relation, sql, auto_begin=False) -%}
    create view {{ relation.schema }}.{{ relation.identifier }} as
    {{ sql }};
{%- endmacro %}

{% macro sqlite__rename_relation(from_relation, to_relation) -%}
  {# no-op #}  
  {# see SQLiteAdapter.rename_relation() #}
{% endmacro %}

{% macro sqlite__get_columns_in_relation(relation) -%}
    {% call statement('get_columns_in_relation', fetch_result=True) %}
        -- TODO: implement this in SQLite
        select 
            column_name
            , data_type
            , character_maximum_length
            , numeric_precision
            , numeric_scale
        from 
            information_schema.columns
        where 
            table_catalog    = '{{ relation.database }}'
            and table_schema = '{{ relation.schema }}'
            and table_name   = '{{ relation.identifier }}'
    {% endcall %}

    {% set table = load_result('get_columns_in_relation').table %}
    {{ return(sql_convert_columns_in_relation(table)) }}
{% endmacro %}
