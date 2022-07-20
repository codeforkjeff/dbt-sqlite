{% macro sqlite__cast_bool_to_text(field) %}
    case
      when {{ field }} = 0 then 'false'
      when {{ field }} = 1 then 'true'    
    end
{% endmacro %}
