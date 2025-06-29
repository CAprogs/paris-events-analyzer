WITH qfap_tags_analysis AS (
    SELECT
        string_agg(qfap_tags, ';' ORDER BY qfap_tags ASC) AS qfap_tags_agg,
        regexp_split_to_array(qfap_tags_agg, ';') AS qfap_tags_list,
    FROM {{ ref('up_to_date_events') }}
)

SELECT
    qfap_tags_distinct,
    count(*) AS nb_events
FROM qfap_tags_analysis, unnest(qfap_tags_list) AS t(qfap_tags_distinct)
GROUP BY qfap_tags_distinct
ORDER BY nb_events DESC
