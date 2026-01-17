-- Messages cannot have a date in the future
select
    message_id,
    message_date
from {{ ref('fct_messages') }}
where message_date > current_date