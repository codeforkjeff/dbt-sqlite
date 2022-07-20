{% macro sqlite__bool_or(expression) -%}

    max({{ expression }})

{%- endmacro %}
