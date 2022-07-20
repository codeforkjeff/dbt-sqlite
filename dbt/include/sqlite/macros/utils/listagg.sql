{% macro sqlite__listagg(measure, delimiter_text, order_by_clause, limit_num) -%}

    {# group_concat() is not as fully featured as Oracle's listagg() but it's what's available #}
    group_concat({{ measure }}, {{ delimiter_text }})

{%- endmacro %}
