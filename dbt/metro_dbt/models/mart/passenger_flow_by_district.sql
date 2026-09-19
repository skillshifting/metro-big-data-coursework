WITH district_counts AS (
    SELECT
        station_id,
        line_id,
        district,
        COUNT(*) AS entrances_count
    FROM {{ source('core', 'station_entrances') }}
    WHERE district IS NOT NULL
    GROUP BY station_id, line_id, district
),

main_districts AS (
    SELECT
        station_id,
        line_id,
        district,
        ROW_NUMBER() OVER (
            PARTITION BY station_id, line_id
            ORDER BY entrances_count DESC, district
        ) AS rn
    FROM district_counts
)

SELECT
    md.district,
    pf.year,
    pf.quarter,
    CASE pf.quarter
    WHEN 'I квартал' THEN 1
    WHEN 'II квартал' THEN 2
    WHEN 'III квартал' THEN 3
    WHEN 'IV квартал' THEN 4
    END AS quarter_num,
    SUM(pf.incoming_passengers) AS incoming_passengers,
    SUM(pf.outgoing_passengers) AS outgoing_passengers,
    SUM(pf.incoming_passengers + pf.outgoing_passengers) AS total_passengers
FROM {{ source('core', 'passenger_flow') }} pf
JOIN main_districts md
    ON md.station_id = pf.station_id
    AND md.line_id = pf.line_id
    AND md.rn = 1
GROUP BY
    md.district,
    pf.year,
    pf.quarter
    