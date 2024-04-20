{% macro sqlite__current_timestamp() -%}
    datetime()
{%- endmacro %}

{% macro sqlite__snapshot_string_as_time(timestamp) -%}
    {# just return the string; SQLite doesn''t have a timestamp data type per se #}
    {{ return("'" + timestamp|string + "'") }}
{%- endmacro %}

{% macro sqlite__snapshot_get_time() -%}
    datetime()
{%- endmacro %}