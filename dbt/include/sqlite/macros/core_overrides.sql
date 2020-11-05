
{% macro ref(model_name) %}

  {# override to strip off database, and return only schema.table #}

  {% set rel = builtins.ref(model_name) %}
  {% do return(rel.schema + "." + rel.identifier) %}

{% endmacro %}

{% macro source(source_name, model_name) %}

  {# override to strip off database, and return only schema.table #}

  {% set rel = builtins.source(source_name, model_name) %}
  {% do return(rel.schema + "." + rel.identifier) %}

{% endmacro %}