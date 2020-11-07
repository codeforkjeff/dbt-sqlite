{% macro sqlite__list_schemas(database) %}
    {# no-op #}
    {# see SQLiteAdapter.list_schemas() #}
{% endmacro %}

{% macro sqlite__create_schema(database_name, schema_name, auto_begin=False) %}
  {% set path = '/'.join(adapter.config.credentials.schema_directory, schema_name, '.db') %}
  {%- call statement('create_schema') -%}
    attach database '{{ path }}' as {{ schema_name }}
  {%- endcall -%}
{% endmacro %}

{% macro sqlite__drop_schema(relation) -%}
  {# drop all tables in the schema, but leave the scgema itself alone. we can't detach 'main' #}

  {% set relations_in_schema = list_relations_without_caching(relation.without_identifier().include(database=False)) %}

  {% for row in relations_in_schema %}
      {%- call statement('drop_relation_in_schema') -%}
        drop {{ row.data_type}} {{ row.schema }}.{{ row.name }}
      {%- endcall -%}
  {% endfor %}
{% endmacro %}

{% macro sqlite__drop_relation(relation) -%}
    {% call statement('drop_relation', auto_begin=False) -%}
        drop {{ relation.type }} if exists {{ relation.include(database=False) }}
    {%- endcall %}
{% endmacro %}

{% macro sqlite__truncate_relation(relation) -%}
    {% call statement('truncate_relation') -%}
        delete from {{ relation.include(database=False) }}
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
      {%- endif %} table {{ relation.include(database=False) }}
      as
        {{ sql }}
{% endmacro %}

{% macro sqlite__create_view_as(relation, sql, auto_begin=False) -%}
    create view {{ relation.include(database=False) }} as
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
    {{ return(result) }}
{%- endmacro %}
