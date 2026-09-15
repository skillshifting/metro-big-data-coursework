markers = [
    "Дата подписания",
    "Наименование линии",
    "Номер линии",
    "Статус",
    "Станция метрополитена",
    "Линия",
    "Год",
    "Квартал",
    "Входы пассажиров",
    "Выходы пассажиров",
    "Наименование",
    "Номер входа/выхода",
    "На территории Москвы",
    "Административный округ",
    "Район",
    "Долгота в WGS-84",
    "Широта в WGS-84",
    "Тип вестибюля",
    "Статус объекта культурного наследия",
    "Режим работы по чётным дням",
    "Режим работы по нечётным дням",
    "Количество полнофункциональных БПА (все типы билетов)",
    "Количество малофункциональных БПА (билеты на 1 и 2 поездки)",
    "Общее количество БПА",
    "Ремонт эскалаторов",
    "Статус объекта",
    "Геоданные",
    "Центроид"
]



numeric_columns = [
            "Year",
            "Incoming passengers",
            "Outgoing passengers",
            "global_id",
            "Incoming passengers",
            "Outgoing passengers",
            "Ticket machines amount",
            "Longitude in WGS-84",
            "Latitude in WGS-84"
        ]



files = {
    "data-2278-08-09-2026.csv": {
        "table": "metro_lines",
        "rename":{
            "global_id": "global_id",
            "signature_date": "signature_date",
            "Line name": "line_name",
            "Metro line number": "metro_line_number",
            "Status": "status"
        }
        
    },
    "data-62743-08-09-2026.csv": {
        "table": "passenger_flow",
        "rename":{
            "Metro station name": "metro_station_name",
            "Line name": "line_name",
            "Year": "year",
            "Quarter": "quarter",
            "Incoming passengers": "incoming_passengers",
            "Outgoing passengers": "outgoing_passengers",
            "global_id": "global_id"
        }
        
    },
    "data-624-11-09-2026.csv":{
        "table":"metro_stations",
        "rename":{
            "Name": "name",
            "Number of exit": "number_of_exit",
            "On territory of Moscow": "on_territory_of_moscow",
            "Area": "area",
            "District": "district",
            "Longitude in WGS-84": "longitude",
            "Latitude in WGS-84": "latitude",
            "Vestibule type": "vestibule_type",
            "Metro station name": "metro_station_name",
            "Line name": "line_name",
            "Cultural heritage site status": "cultural_heritage_site_status",
            "Working schedule on even days": "working_schedule_on_even_days",
            "Working schedule on odd days": "working_schedule_on_odd_days",
            "Ticket machines amount": "ticket_machines_amount",
            "RepairOfEscalators": "repair_of_escalators",
            "Object status": "object_status",
            "Geodata": "geodata",
            "Centroid": "centroid",
            "global_id": "global_id"
        }
        
    }
}