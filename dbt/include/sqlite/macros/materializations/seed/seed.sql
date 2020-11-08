
{% macro sqlite__load_csv_rows(model, agate_table) %}
    {% set batch_size = 100000 %}
    {% set cols_sql = get_seed_column_quoted_csv(model, agate_table.column_names) %}
    {% set bindings = [] %}

    {% set statements = [] %}

    {% for chunk in agate_table.rows | batch(batch_size) %}
        {% set bindings = [] %}

        {% for row in chunk %}
            {# transform rows so sqlite is happy with data types #}
            {% set processed_row = adapter.transform_seed_row(row) %}
            {% do bindings.extend(processed_row) %}
        {% endfor %}

        {% set sql %}
            insert into {{ this.schema }}.{{ this.identifier}} ({{ cols_sql }}) values
            {% for row in chunk -%}
                ({%- for column in agate_table.column_names -%}
                    {# sqlite uses ? as placeholder character #}
                    ?
                    {%- if not loop.last%},{%- endif %}
                {%- endfor -%})
                {%- if not loop.last%},{%- endif %}
            {%- endfor %}
        {% endset %}

        {% do adapter.add_query(sql, bindings=bindings, abridge_sql_log=True) %}

        {% if loop.index0 == 0 %}
            {% do statements.append(sql) %}
        {% endif %}
    {% endfor %}

    {# Return SQL so we can render it out into the compiled files #}
    {{ return(statements[0]) }}
{% endmacro %}
