with aggregated_channels as (
    -- First, we group the data by channel
    select
        channel_name,
        min(message_date) as first_post_date,
        max(message_date) as last_post_date,
        count(message_id) as total_posts,
        avg(views) as avg_views
    from {{ ref('stg_telegram_messages') }}
    group by 1
)

select
    -- Now we add the unique ID (surrogate key) to the grouped results
    row_number() over (order by channel_name) as channel_key,
    channel_name,
    first_post_date,
    last_post_date,
    total_posts,
    avg_views
from aggregated_channels