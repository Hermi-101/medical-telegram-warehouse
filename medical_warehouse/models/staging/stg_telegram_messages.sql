with raw_data as (
    select * from {{ source('raw_data', 'telegram_messages') }}
)

select
    -- Primary Key
    message_id,
    
    -- Foreign Keys / IDs
    channel_username as channel_name,
    
    -- Timestamps
    cast(message_date as timestamp) as message_timestamp,
    cast(message_date as date) as message_date,
    
    -- Content
    message_text,
    length(message_text) as message_length,
    
    -- Media details
    has_media,
    media_path as image_path,
    case when has_media = true then 1 else 0 end as has_image_flag,
    
    -- Metrics
    coalesce(views, 0) as views,
    coalesce(forwards, 0) as forwards

from raw_data
where message_id is not null