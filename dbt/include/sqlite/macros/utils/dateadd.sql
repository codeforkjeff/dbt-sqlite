{% macro sqlite__dateadd(from_date_or_timestamp, interval, datepart) %}
    -- If provided a DATETIME, returns a DATETIME
    -- If provided a DATE, returns a DATE

    CASE
        -- Matches DATETIME type based on ISO-8601 
        WHEN {{ from_date_or_timestamp }} LIKE '%:%' OR ({{ from_date_or_timestamp }} LIKE '%T%' AND {{ from_date_or_timestamp }} LIKE '%Z%') THEN
            CASE
                WHEN LOWER({{ datepart }}) = 'second' THEN datetime({{ from_date_or_timestamp }}, '+' || {{ interval }} || ' seconds')
                WHEN LOWER({{ datepart }}) = 'minute' THEN datetime({{ from_date_or_timestamp }}, '+' || {{ interval }} || ' minutes')
                WHEN LOWER({{ datepart }}) = 'hour' THEN datetime({{ from_date_or_timestamp }}, '+' || {{ interval }} || ' hours')
                WHEN LOWER({{ datepart }}) = 'day' THEN datetime({{ from_date_or_timestamp }}, '+' || {{ interval }} || ' days')
                WHEN LOWER({{ datepart }}) = 'week' THEN datetime({{ from_date_or_timestamp }}, '+' || ({{ interval }} * 7) || ' days')
                WHEN LOWER({{ datepart }}) = 'month' THEN datetime({{ from_date_or_timestamp }}, '+' || {{ interval }} || ' months')
                WHEN LOWER({{ datepart }}) = 'quarter' THEN datetime({{ from_date_or_timestamp }}, '+' || ({{ interval }} * 3) || ' months')
                WHEN LOWER({{ datepart }}) = 'year' THEN datetime({{ from_date_or_timestamp }}, '+' || {{ interval }} || ' years')
                ELSE NULL
            END
        -- Matches DATE type based on ISO-8601
        WHEN {{ from_date_or_timestamp }} LIKE '%-%' AND {{ from_date_or_timestamp }} NOT LIKE '%T%' AND {{ from_date_or_timestamp }} NOT LIKE '% %' THEN
            CASE
                WHEN LOWER({{ datepart }}) IN ('second', 'minute', 'hour') THEN date({{ from_date_or_timestamp }})
                WHEN LOWER({{ datepart }}) = 'day' THEN date({{ from_date_or_timestamp }}, '+' || {{ interval }} || ' days')
                WHEN LOWER({{ datepart }}) = 'week' THEN date({{ from_date_or_timestamp }}, '+' || ({{ interval }} * 7) || ' days')
                WHEN LOWER({{ datepart }}) = 'month' THEN date({{ from_date_or_timestamp }}, '+' || {{ interval }} || ' months')
                WHEN LOWER({{ datepart }}) = 'quarter' THEN date({{ from_date_or_timestamp }}, '+' || ({{ interval }} * 3) || ' months')
                WHEN LOWER({{ datepart }}) = 'year' THEN date({{ from_date_or_timestamp }}, '+' || {{ interval }} || ' years')
                ELSE NULL
            END
        ELSE
            NULL
    END
{% endmacro %}
