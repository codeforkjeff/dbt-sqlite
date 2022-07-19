{% macro sqlite__any_value(expression) -%}

    min({{ expression }})

{%- endmacro %}
