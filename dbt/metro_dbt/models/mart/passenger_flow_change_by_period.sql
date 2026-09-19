SELECT
    year,
    quarter,
    total_passengers,
    LAG(total_passengers) OVER (
        ORDER BY
            year,
            CASE quarter
                WHEN 'I квартал' THEN 1
                WHEN 'II квартал' THEN 2
                WHEN 'III квартал' THEN 3
                WHEN 'IV квартал' THEN 4
            END
    ) AS previous_total_passengers,
    total_passengers - LAG(total_passengers) OVER (
        ORDER BY
            year,
            CASE quarter
                WHEN 'I квартал' THEN 1
                WHEN 'II квартал' THEN 2
                WHEN 'III квартал' THEN 3
                WHEN 'IV квартал' THEN 4
            END
    ) AS change_absolute
FROM {{ ref('passenger_flow_by_period') }}