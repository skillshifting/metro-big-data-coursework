SELECT
    pf.year,
    pf.quarter,
    SUM(pf.incoming_passengers) AS incoming_passengers,
    SUM(pf.outgoing_passengers) AS outgoing_passengers,
    SUM(pf.incoming_passengers + pf.outgoing_passengers) AS total_passengers
FROM {{ source('core', 'passenger_flow') }} pf
GROUP BY
    pf.year,
    pf.quarter