{# adapted from postgresql #}
{% macro sqlite__datediff(first_date, second_date, datepart) -%}

    {% if datepart == 'year' %}
        (strftime('%Y', {{second_date}}) - strftime('%Y', {{first_date}}))
    {#
    {% elif datepart == 'quarter' %}
        ({{ datediff(first_date, second_date, 'year') }} * 4 + date_part('quarter', ({{second_date}})::date) - date_part('quarter', ({{first_date}})::date))
    #}
    {% elif datepart == 'month' %}
        (({{ datediff(first_date, second_date, 'year') }} * 12 + strftime('%m', {{second_date}})) - strftime('%m', {{first_date}}))
    {% elif datepart == 'day' %}
        (floor(cast(strftime('%s', {{second_date}}) - strftime('%s', {{first_date}}) as real) / 86400) +
        case when {{second_date}} <= strftime('%Y-%m-%d 23:59:59.999999', {{first_date}}) then -1 else 0 end)
    {% elif datepart == 'week' %}
        ({{ datediff(first_date, second_date, 'day') }} / 7 + case
            when strftime('%w', {{first_date}}) <= strftime('%w', {{second_date}}) then
                case when {{first_date}} <= {{second_date}} then 0 else -1 end
            else
                case when {{first_date}} <= {{second_date}} then 1 else 0 end
        end)
    {% elif datepart == 'hour' %}
        {# ({{ datediff(first_date, second_date, 'day') }} * 24 + strftime("%H", {{second_date}}) - strftime("%H", {{first_date}})) #}
        (ceil(cast(strftime('%s', {{second_date}}) - strftime('%s', {{first_date}}) as real) / 3600))
    {% elif datepart == 'minute' %}
        {# ({{ datediff(first_date, second_date, 'hour') }} * 60 + strftime("%M", {{second_date}}) - strftime("%M", {{first_date}})) #}
        (ceil(cast(strftime('%s', {{second_date}}) - strftime('%s', {{first_date}}) as real) / 60))
    {% elif datepart == 'second' %}
        (strftime('%s', {{second_date}}) - strftime('%s', {{first_date}}))
    {#
    {% elif datepart == 'millisecond' %}
        ({{ datediff(first_date, second_date, 'minute') }} * 60000 + floor(date_part('millisecond', ({{second_date}})::timestamp)) - floor(date_part('millisecond', ({{first_date}})::timestamp)))
    {% elif datepart == 'microsecond' %}
        ({{ datediff(first_date, second_date, 'minute') }} * 60000000 + floor(date_part('microsecond', ({{second_date}})::timestamp)) - floor(date_part('microsecond', ({{first_date}})::timestamp)))
    #}
    {% else %}
        {{ exceptions.raise_compiler_error("Unsupported datepart for macro datediff in sqlite: {!r}".format(datepart)) }}
    {% endif %}

{%- endmacro %}
