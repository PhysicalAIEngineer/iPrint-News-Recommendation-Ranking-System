# iPrint Data Dictionary

## consumer_transactions

| Feature | Type | Meaning | Downstream Use |
|---|---|---|---|
| consumer_id | ID | User identifier | User profile / CF |
| item_id | ID | Article identifier | User-item matrix |
| event_timestamp | timestamp | User interaction time | Recency / temporal split |
| interaction_type | categorical | User behavior | Implicit feedback |
| consumer_session_id | ID | Session identifier | Session features |
| consumer_device_info | categorical | Device context | Ranking |
| consumer_location | categorical | User location | Context |
| country | categorical | User country | Context |

## platform_content

| Feature | Type | Meaning | Downstream Use |
|---|---|---|---|
| item_id | ID | Article identifier | Join key |
| title | text | Article title | TF-IDF / embeddings |
| text_description | text | Article description | TF-IDF / embeddings |
| language | categorical | Article language | English filter |
| item_type | categorical | HTML/VIDEO/RICH | Ranking |
| producer_id | ID | Content producer | Producer affinity |
| event_timestamp | timestamp | Content event time | Freshness |
| interaction_type | categorical | Present/pulled | Availability filter |