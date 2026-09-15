CREATE TABLE IF NOT EXISTS staging.metro_lines(
    global_id BIGINT PRIMARY KEY,
    signature_date TEXT,
    line_name TEXT,
    metro_line_number TEXT,
    status TEXT
);

CREATE TABLE IF NOT EXISTS staging.passenger_flow(
    global_id BIGINT PRIMARY KEY,
    metro_station_name TEXT,
    line_name TEXT,
    year INTEGER,
    quarter TEXT,
    incoming_passengers BIGINT,
    outgoing_passengers BIGINT
);

CREATE TABLE IF NOT EXISTS staging.metro_stations(
    global_id BIGINT PRIMARY KEY,
    name TEXT,
    number_of_exit TEXT,
    on_territory_of_moscow TEXT,
    area TEXT,
    district TEXT,
    longitude DOUBLE PRECISION,
    latitude DOUBLE PRECISION,
    vestibule_type TEXT,
    metro_station_name TEXT,
    line_name TEXT,
    cultural_heritage_site_status TEXT,
    working_schedule_on_even_days TEXT,
    working_schedule_on_odd_days TEXT,
    ticket_machines_amount DOUBLE PRECISION,
    repair_of_escalators TEXT,
    object_status TEXT,
    geodata TEXT,
    centroid TEXT
);