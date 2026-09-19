WITH station_totals AS (
    SELECT
        station_name,
        year,
        quarter,
        SUM(total_passengers) AS total_passengers
    FROM {{ ref('passenger_flow_by_station') }}
    GROUP BY
        station_name,
        year,
        quarter
)

SELECT
    station_name,
    year,
    quarter,
    total_passengers,
    RANK() OVER (
        PARTITION BY year, quarter
        ORDER BY total_passengers DESC
    ) AS station_rank
FROM station_totals