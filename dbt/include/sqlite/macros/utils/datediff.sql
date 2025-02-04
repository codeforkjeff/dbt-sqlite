{#
-- The sqlite__datediff macro uses epoch time deltas to calculate differences between dates, offering precision down to the millisecond level. 
-- Despite SQLite's limitations in handling sub-millisecond accuracy, the macro reliably handles differences across various date parts 
-- (year, month, week, day, hour, minute, second, millisecond).
-- To ensure the macro's effectiveness even with the smallest discernible time differences (e.g., one millisecond), empirical adjustments have been implemented. 
-- These adjustments are particularly crucial for broader date parts like 'week'. 
-- The decision to use CEIL or FLOOR for rounding was refined through testing to accurately reflect differences when dates are separated by as little as one millisecond.
-- This empirical approach ensures that the macro not only meets expected functional accuracy but also addresses real-world use cases effectively. 
-- For example, calculating the week difference between two timestamps only a millisecond apart requires careful consideration of how to round fractional weeks. 
-- The choice to use CEIL in certain contexts was driven by the need to acknowledge even the minimal time difference as a full unit where contextually appropriate.
-- TODO: More unit testing should be done with a comprehensive calendar table "solved" in another RDBMS that supports datediff natively for comparing against the results of this macro.
#}
{% macro sqlite__datediff(first_date, second_date, datepart) -%}
    {% set datepart = datepart.lower() %}
    {% if datepart == 'year' %}
        (strftime('%Y', {{ second_date }}) - strftime('%Y', {{ first_date }}))
    {% elif datepart == 'month' %}
        ((strftime('%Y', {{ second_date }}) - strftime('%Y', {{ first_date }})) * 12) +
        (strftime('%m', {{ second_date }}) - strftime('%m', {{ first_date }}))
    {% elif datepart == 'day' %}
        CASE
            WHEN 
                ((strftime('%s', {{ second_date }}) - strftime('%s', {{ first_date }})) / 86400.0) >= 0
            THEN CEIL(
                (strftime('%s', {{ second_date }}) - strftime('%s', {{ first_date }})) / 86400.0
            )
            ELSE FLOOR(
                (strftime('%s', {{ second_date }}) - strftime('%s', {{ first_date }})) / 86400.0
            )
        END
    {% elif datepart == 'week' %}
        CASE
            WHEN 
                ((strftime('%s', {{ second_date }}) - strftime('%s', {{ first_date }})) / 604800.0) >= 0.285715
            THEN CEIL(
                (strftime('%s', {{ second_date }}) - strftime('%s', {{ first_date }})) / 604800.0
            )
            WHEN 
                ((strftime('%s', {{ second_date }}) - strftime('%s', {{ first_date }})) / 604800.0) <= -0.285715
            THEN FLOOR(
                (strftime('%s', {{ second_date }}) - strftime('%s', {{ first_date }})) / 604800.0
            )
            ELSE CAST(
                (strftime('%s', {{ second_date }}) - strftime('%s', {{ first_date }})) / 604800.0
            AS INTEGER)
        END
    {% elif datepart == 'hour' %}
        CASE
            WHEN 
                ((strftime('%s', {{ second_date }}) - strftime('%s', {{ first_date }})) / 3600.0) >= 0 
            THEN CEIL(
                (strftime('%s', {{ second_date }}) - strftime('%s', {{ first_date }})) / 3600.0
            )
            ELSE FLOOR(
                (strftime('%s', {{ second_date }}) - strftime('%s', {{ first_date }})) / 3600.0
            )
        END
    {% elif datepart == 'minute' %}
        CASE
            WHEN 
                ((strftime('%s', {{ second_date }}) - strftime('%s', {{ first_date }})) / 60.0) >= 0 
            THEN CEIL(
                (strftime('%s', {{ second_date }}) - strftime('%s', {{ first_date }})) / 60.0
            )
            ELSE FLOOR(
                (strftime('%s', {{ second_date }}) - strftime('%s', {{ first_date }})) / 60.0
            )
        END
    {% elif datepart == 'second' %}
        CASE
            WHEN 
                ((strftime('%s', {{ second_date }}) + cast(substr(strftime('%f', {{ second_date }}), instr(strftime('%f', {{ second_date }}), '.') + 1) as real) / 1000.0) - 
                 (strftime('%s', {{ first_date }}) + cast(substr(strftime('%f', {{ first_date }}), instr(strftime('%f', {{ first_date }}), '.') + 1) as real) / 1000.0)) >= 0 
            THEN CEIL(
                (strftime('%s', {{ second_date }}) + cast(substr(strftime('%f', {{ second_date }}), instr(strftime('%f', {{ second_date }}), '.') + 1) as real) / 1000.0) - 
                (strftime('%s', {{ first_date }}) + cast(substr(strftime('%f', {{ first_date }}), instr(strftime('%f', {{ first_date }}), '.') + 1) as real) / 1000.0)
            )
            ELSE FLOOR(
                (strftime('%s', {{ second_date }}) + cast(substr(strftime('%f', {{ second_date }}), instr(strftime('%f', {{ second_date }}), '.') + 1) as real) / 1000.0) - 
                (strftime('%s', {{ first_date }}) + cast(substr(strftime('%f', {{ first_date }}), instr(strftime('%f', {{ first_date }}), '.') + 1) as real) / 1000.0)
            )
        END
    {% elif datepart == 'millisecond' %}
        ((1000 * (strftime('%s', {{ second_date }}))) + cast(substr(strftime('%f', {{ second_date }}), instr(strftime('%f', {{ second_date }}), '.') + 1) as integer) -
         (1000 * (strftime('%s', {{ first_date }}))) + cast(substr(strftime('%f', {{ first_date }}), instr(strftime('%f', {{ first_date }}), '.') + 1) as integer))
    {% else %}
        {{ exceptions.raise_compiler_error("Unsupported datepart for macro datediff in SQLite: '" ~ datepart ~ "'") }}
    {% endif %}
{%- endmacro %}
