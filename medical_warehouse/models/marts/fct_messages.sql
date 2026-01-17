select
    m.message_id,
    c.channel_key,
    m.message_date,
    m.message_text,
    m.message_length,
    m.views,
    m.forwards,
    m.has_image_flag as has_image
from {{ ref('stg_telegram_messages') }} m
join {{ ref('dim_channels') }} c on m.channel_name = c.channel_name