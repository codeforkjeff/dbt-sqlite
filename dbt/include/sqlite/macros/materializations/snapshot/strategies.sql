{% macro sqlite__snapshot_hash_arguments(args) -%}
    hex(md5({%- for arg in args -%}
        coalesce(cast({{ arg }} as varchar ), '')
        {% if not loop.last %} || '|' || {% endif %}
    {%- endfor -%}))
{%- endmacro %}
