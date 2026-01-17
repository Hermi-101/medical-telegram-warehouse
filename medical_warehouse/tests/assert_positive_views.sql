-- View counts must be 0 or higher
select
    message_id,
    views
from {{ ref('fct_messages') }}
where views < 0