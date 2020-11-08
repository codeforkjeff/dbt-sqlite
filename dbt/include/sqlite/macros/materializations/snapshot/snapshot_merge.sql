
{% macro sqlite__snapshot_merge_sql(target, source, insert_cols) -%}
    {%- set insert_cols_csv = insert_cols | join(', ') -%}

    {% set update_sql %}
    update {{ target }}
    set dbt_valid_to = (
        SELECT
            DBT_INTERNAL_SOURCE.dbt_valid_to
        from {{ source }} as DBT_INTERNAL_SOURCE
        where DBT_INTERNAL_SOURCE.dbt_scd_id = {{ target }}.dbt_scd_id
            and DBT_INTERNAL_SOURCE.dbt_change_type = 'update'
    )
    WHERE dbt_valid_to is null;
    {% endset %}

    {#
    TODO: this is a hack: this macro is supposed to return a SQL string
    but we're executing a query here. this happens to work and it avoids having
    to override the snapshot_merge macro to properly execute two separate
    statements but it's horrible.
    #}
    {% do adapter.add_query(update_sql, auto_begin=False) %}

    insert into {{ target }} ({{ insert_cols_csv }})
    select {% for column in insert_cols -%}
        DBT_INTERNAL_SOURCE.{{ column }} {%- if not loop.last %}, {%- endif %}
    {%- endfor %}
    from {{ source }} as DBT_INTERNAL_SOURCE
    where DBT_INTERNAL_SOURCE.dbt_change_type = 'insert';

{% endmacro %}
