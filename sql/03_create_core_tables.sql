CREATE TABLE IF NOT EXISTS core.lines (
    line_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    line_name TEXT UNIQUE NOT NULL,
    metro_line_number VARCHAR(4),
    status TEXT
);

WITH all_lines AS (
    SELECT line_name FROM staging.metro_lines
    UNION
    SELECT line_name FROM staging.passenger_flow
    UNION
    SELECT line_name FROM staging.metro_stations
)

INSERT INTO core.lines(line_name, metro_line_number, status)
SELECT all_lines.line_name, metro_lines.metro_line_number, metro_lines.status
FROM all_lines
LEFT JOIN staging.metro_lines AS metro_lines ON all_lines.line_name = metro_lines.line_name
ON CONFLICT (line_name) DO NOTHING;





CREATE TABLE IF NOT EXISTS core.stations (
    station_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    station_name TEXT UNIQUE NOT NULL
);

WITH all_stations AS (
    SELECT metro_station_name FROM staging.passenger_flow
    UNION
    SELECT metro_station_name FROM staging.metro_stations
)

INSERT INTO core.stations(station_name)
SELECT metro_station_name
FROM all_stations
ON CONFLICT (station_name) DO NOTHING;






CREATE TABLE IF NOT EXISTS core.station_lines (
    station_id BIGINT,
    line_id INT,
    
    PRIMARY KEY (station_id, line_id),

    CONSTRAINT fk_station FOREIGN KEY (station_id) REFERENCES core.stations (station_id) ON DELETE CASCADE,
    CONSTRAINT fk_line FOREIGN KEY (line_id) REFERENCES core.lines (line_id) ON DELETE CASCADE
);

WITH all_stations_lines AS(
    SELECT DISTINCT metro_station_name, line_name
    FROM staging.metro_stations
    UNION
    SELECT DISTINCT metro_station_name,line_name
    FROM staging.passenger_flow
)

INSERT INTO core.station_lines (station_id, line_id)
SELECT 
    s.station_id,
    l.line_id
FROM all_stations_lines asl

JOIN core.stations s ON asl.metro_station_name = s.station_name
JOIN core.lines l ON asl.line_name = l.line_name

ON CONFLICT (station_id, line_id) DO NOTHING;





CREATE TABLE IF NOT EXISTS core.passenger_flow(
    flow_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    station_id BIGINT,
    line_id INT,
    year INT,
    quarter TEXT,
    incoming_passengers BIGINT,
    outgoing_passengers BIGINT,
    source_global_id BIGINT,

    CONSTRAINT fk_station FOREIGN KEY (station_id) REFERENCES core.stations (station_id) ON DELETE CASCADE,
    CONSTRAINT fk_line FOREIGN KEY (line_id) REFERENCES core.lines (line_id) ON DELETE CASCADE,

    UNIQUE (station_id, line_id, year, quarter)
);



INSERT INTO core.passenger_flow (station_id, line_id,year,quarter, incoming_passengers, outgoing_passengers, source_global_id)
SELECT 
    s.station_id,
    l.line_id,
    pf.year,
    pf.quarter,
    pf.incoming_passengers,
    pf.outgoing_passengers,
    pf.global_id
FROM staging.passenger_flow pf

JOIN core.stations s ON pf.metro_station_name = s.station_name
JOIN core.lines l ON pf.line_name = l.line_name
ON CONFLICT (station_id,line_id,year,quarter) DO NOTHING;





CREATE TABLE IF NOT EXISTS core.station_entrances(
    entrance_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    station_id BIGINT NOT NULL,
    line_id INT NOT NULL, 
    entrance_name TEXT,
    number_of_exit TEXT,
    area TEXT,
    district TEXT,
    longitude DOUBLE PRECISION NOT NULL, 
    latitude DOUBLE PRECISION NOT NULL,
    vestibule_type TEXT, 
    ticket_machines_amount INT,
    object_status TEXT,
    source_global_id BIGINT UNIQUE,

    CONSTRAINT fk_station FOREIGN KEY (station_id) REFERENCES core.stations (station_id) ON DELETE CASCADE,
    CONSTRAINT fk_line FOREIGN KEY (line_id) REFERENCES core.lines (line_id) ON DELETE CASCADE
);

INSERT INTO core.station_entrances (station_id,line_id,entrance_name,number_of_exit,area,district,longitude,latitude,vestibule_type,ticket_machines_amount,object_status,source_global_id)
SELECT 
    s.station_id,
    l.line_id,
    ms.name,
    ms.number_of_exit,
    ms.area,
    ms.district,
    ms.longitude,
    ms.latitude,
    ms.vestibule_type,
    ms.ticket_machines_amount,
    ms.object_status,
    ms.global_id
FROM staging.metro_stations AS ms

JOIN core.stations s ON ms.metro_station_name = s.station_name
JOIN core.lines l ON ms.line_name = l.line_name

ON CONFLICT (source_global_id) DO NOTHING;