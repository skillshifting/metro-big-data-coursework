SELECT 
    s.station_name,
    l.line_name,
    pf.year,
    pf.quarter,
    pf.incoming_passengers,
    pf.outgoing_passengers,
    (pf.incoming_passengers + pf.outgoing_passengers) AS total_passengers
FROM {{ source('core', 'passenger_flow') }} as pf

JOIN {{ source('core', 'stations')}} s ON s.station_id = pf.station_id
JOIN {{ source('core', 'lines')}} l ON l.line_id = pf.line_id

