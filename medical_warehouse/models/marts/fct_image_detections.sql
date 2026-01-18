select
    y.message_id,
    f.channel_key,
    f.date_key,
    y.detected_class,
    y.confidence as confidence_score,
    y.image_category
from {{ source('detection_data', 'yolo_results') }} y
join {{ ref('fct_messages') }} f on y.message_id = f.message_id