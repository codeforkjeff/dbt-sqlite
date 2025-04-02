{% macro sqlite__date_trunc(datepart, date) -%}
{#- Truncate a date to a specified datepart.

`sqlite__date_trunc` always returns a datetime.

Only supports the following date parts:
"year", "quarter", "month", "week", "day", "hour", "minute", "second"

Makes use of official datetime modifiers when possible.
For details of date and time functions in sqlite, refer to the official documentation:
https://www.sqlite.org/lang_datefunc.html -#}
{#- datepart can be quoted or unquoted, lower or uppercase -#}
{%- set datepart = datepart.lower().strip("'") -%}

{#- use the official modifier whenever possible -#}
{%- if datepart == "year" -%} datetime({{ date }}, 'start of year')
{%- elif datepart == "month" -%} datetime({{ date }}, 'start of month')
{%- elif datepart == "day" -%} datetime({{ date }}, 'start of day')

{%- elif datepart == "quarter" -%}
{#- truncate to start of year, then add necessary number of months -#}
{#- note that we make use of integer division to round down -#}
datetime(
    {{ date }},
    'start of year',
    '+' || cast((strftime('%m', {{ date }}) - 1) / 3 * 3 as text) || " month"
)

{%- elif datepart == "week" -%}
{#- remove {day_no} days and truncate to start of day -#}
{#- note that week starts at Sunday, i.e. Sunday=0 -#}
datetime({{ date }}, ('-' || strftime('%w', {{ date }}) || ' day'), 'start of day')

{%- elif datepart == "hour" -%}
{#- truncate to start of day, then add back hours -#}
datetime({{ date }}, 'start of day', '+' || strftime('%H', {{ date }}) || " hour")

{%- elif datepart == "minute" -%}
{#- truncate to start of day, then add back hours and minutes -#}
datetime(
    {{ date }},
    'start of day',
    '+' || strftime('%H', {{ date }}) || " hour",
    '+' || strftime('%M', {{ date }}) || " minute"
)
{%- elif datepart == "second" -%}
{#- truncate to start of day, then add back hours, minutes, seconds -#}
datetime(
    {{ date }},
    'start of day',
    '+' || strftime('%H', {{ date }}) || " hour",
    '+' || strftime('%M', {{ date }}) || " minute",
    '+' || strftime('%S', {{ date }}) || " second"
)

{%- else -%}
{#- arithmetics for micro-/nanoseconds is more complicated, skipped for now -#}
{{
    exceptions.raise_compiler_error(
        "Unsupported datepart for macro date_trunc in sqlite: {!r}".format(datepart)
    )
}}
{%- endif -%}
{%- endmacro %}
