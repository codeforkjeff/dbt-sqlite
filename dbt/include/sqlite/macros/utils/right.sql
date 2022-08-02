{% macro sqlite__right(string_text, length_expression) %}
    case
      when {{ length_expression }} <> 0 then 
      substr(
          {{ string_text }},
          -1 * {{ length_expression }}
      )
      else ''
    end
{%- endmacro -%}
