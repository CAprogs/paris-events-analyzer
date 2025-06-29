WITH exploded AS (
    SELECT
        id,
        fragment
    FROM {{ ref('filtered_rows') }},
        unnest(regexp_split_to_array(occurrences, ';')) AS t(fragment)
),

parsed AS (
    SELECT
        id,
        timezone('Europe/London', regexp_extract(fragment, '([^_]+)_([^_]+)', 1)::TIMESTAMPTZ) AS start_ts, -- LONDON timezone is used because the timezone is not aligned with the event's date description
        timezone('Europe/London', regexp_extract(fragment, '([^_]+)_([^_]+)', 2)::TIMESTAMPTZ) AS end_ts
    FROM exploded
)

SELECT
    id,
    list(
        struct_pack(start_time := start_ts, end_time := end_ts)
    ) AS tous_les_creneaux,
    len(tous_les_creneaux) AS nb_total_occurences,
    list_filter(tous_les_creneaux, lambda x: x['start_time'] > current_localtimestamp()) AS prochains_creneaux,
    [x['start_time']::DATE FOR x IN prochains_creneaux] AS next_start_date,
    list_contains(next_start_date, current_date) AS has_event_today,
    len(prochains_creneaux) AS nb_next_occurrences
FROM parsed
GROUP BY id
