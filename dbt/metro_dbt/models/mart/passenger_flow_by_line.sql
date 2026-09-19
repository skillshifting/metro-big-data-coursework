SELECT
    l.line_name,
    pf.year,
    pf.quarter,
    SUM(pf.incoming_passengers) AS incoming_passengers,
    SUM(pf.outgoing_passengers) AS outgoing_passengers,
    SUM(pf.incoming_passengers + pf.outgoing_passengers) AS total_passengers
FROM {{ source('core', 'passenger_flow') }} pf
JOIN {{ source('core', 'lines') }} l ON l.line_id = pf.line_id
GROUP BY
    l.line_name,
    pf.year,
    pf.quarter