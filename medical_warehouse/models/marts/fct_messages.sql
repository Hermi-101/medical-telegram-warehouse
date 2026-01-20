select
    m.message_id,
    c.channel_key,
    -- Add this line back:
    m.message_date, 
    cast(to_char(m.message_date, 'YYYYMMDD') as integer) as date_key,
    m.message_text,
    m.message_length,
    m.views,
    m.forwards,
    m.has_image_flag as has_image
from {{ ref('stg_telegram_messages') }} m
join {{ ref('dim_channels') }} c on m.channel_name = c.channel_name