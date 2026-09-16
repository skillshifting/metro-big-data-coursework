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

