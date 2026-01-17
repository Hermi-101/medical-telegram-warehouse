with date_series as (
    -- Generate a series of dates from 2024 to 2026
    select generate_series(
        '2024-01-01'::date,
        '2026-12-31'::date,
        '1 day'::interval
    )::date as full_date
)

select
    -- date_key in format YYYYMMDD (e.g., 20260117)
    cast(to_char(full_date, 'YYYYMMDD') as integer) as date_key,
    full_date,
    extract(year from full_date) as year,
    extract(month from full_date) as month,
    to_char(full_date, 'Month') as month_name,
    extract(day from full_date) as day,
    extract(dow from full_date) as day_of_week,
    to_char(full_date, 'Day') as day_name,
    extract(quarter from full_date) as quarter,
    -- Weekend flag (Saturday=6, Sunday=0)
    case when extract(dow from full_date) in (0, 6) then true else false end as is_weekend
from date_series