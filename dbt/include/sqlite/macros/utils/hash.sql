{% macro sqlite__hash(field) -%}
    case 
      when {{ field }} is not null 
      then lower(hex(md5(cast({{ field }} as {{ api.Column.translate_type('string') }}))))
    end
{%- endmacro %}
