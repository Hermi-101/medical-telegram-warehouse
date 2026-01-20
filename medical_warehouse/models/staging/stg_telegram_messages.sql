with raw_data as (
    select * from {{ source('raw_data', 'telegram_messages') }}
),
deduplicated as (
    select
        *,
        -- Assign a number to each version of the same message_id
        row_number() over (
            partition by message_id 
            order by message_date desc -- Keep the most recent one
        ) as row_num
    from raw_data
    where message_id is not null
)

select
    message_id,
    channel_username as channel_name,
    cast(message_date as timestamp) as message_timestamp,
    cast(message_date as date) as message_date,
    message_text,
    length(message_text) as message_length,
    has_media,
    media_path as image_path,
    case when has_media = true then 1 else 0 end as has_image_flag,
    coalesce(views, 0) as views,
    coalesce(forwards, 0) as forwards
from deduplicated
where row_num = 1 -- Only keep the first unique record per message_id
  and message_text is not null