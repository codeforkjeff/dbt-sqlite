{% macro sqlite__position(substring_text, string_text) %}

    instr({{ string_text }}, {{ substring_text }})

{%- endmacro -%}
