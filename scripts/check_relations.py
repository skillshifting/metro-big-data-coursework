from pathlib import Path

import pandas as pd

from inspect_data import DataSetScanner


if __name__ == "__main__":
    raw_path = Path(__file__).resolve().parents[1] / "data" / "raw"

    passenger_file = raw_path / "data-62743-08-09-2026.csv"
    station_file = raw_path / "data-624-11-09-2026.csv"
    line_reference_file = raw_path / "data-2278-08-09-2026.csv"

    passenger_scanner = DataSetScanner(passenger_file)
    station_scanner = DataSetScanner(station_file)
    line_reference_scanner = DataSetScanner(line_reference_file)

    passenger_df = passenger_scanner.df
    station_df = station_scanner.df
    line_reference_df = line_reference_scanner.df

    passenger_lines = set(passenger_df["Line name"].dropna().unique())
    station_lines = set(station_df["Line name"].dropna().unique())
    reference_lines = set(line_reference_df["Line name"].dropna().unique())

    print("\nЛинии")

    print("Линий в пассажиропотоке:", len(passenger_lines))
    print("Линий в справочнике станций:", len(station_lines))
    print("Линий в справочнике линий:", len(reference_lines))

    passenger_only_lines = passenger_lines - station_lines
    station_only_lines = station_lines - passenger_lines

    print("\nЕсть в пассажиропотоке, но нет в справочнике станций:")
    print(passenger_only_lines)

    print("\nЕсть в справочнике станций, но нет в пассажиропотоке:")
    print(station_only_lines)

    problem_lines = passenger_only_lines | station_only_lines

    print("\nДетали по несовпадающим линиям")

    for line in sorted(problem_lines):
        print(f"\nЛиния: {line}")

        if line in passenger_lines:
            passenger_rows = passenger_df[passenger_df["Line name"] == line]
            passenger_stations = passenger_rows["Metro station name"].dropna().unique().tolist()

            print("Пассажиропоток, строк:", len(passenger_rows))
            print("Станции:", passenger_stations)

        if line in station_lines:
            station_rows = station_df[station_df["Line name"] == line]
            station_stations = station_rows["Metro station name"].dropna().unique().tolist()

            print("Справочник станций, строк:", len(station_rows))
            print("Станции:", station_stations)

    print("\nИнформация из справочника линий")

    reference_rows = line_reference_df[line_reference_df["Line name"].isin(problem_lines)]

    if reference_rows.empty:
        print("Несовпадающих линий в справочнике линий нет")
    else:
        print(reference_rows[["Line name", "Metro line number", "Status"]].to_string(index=False))

    passenger_stations = set(passenger_df["Metro station name"].dropna().unique())
    station_stations = set(station_df["Metro station name"].dropna().unique())

    print("\nСтанции")

    print("Уникальных станций в пассажиропотоке:", len(passenger_stations))
    print("Уникальных станций в справочнике станций:", len(station_stations))

    passenger_only_stations = passenger_stations - station_stations
    station_only_stations = station_stations - passenger_stations

    print("\nЕсть в пассажиропотоке, но нет в справочнике станций:")
    print(sorted(passenger_only_stations))

    print("\nЕсть в справочнике станций, но нет в пассажиропотоке:")
    print(sorted(station_only_stations))

    print("\nДетали станций, которые есть только в пассажиропотоке")

    if passenger_only_stations:
        passenger_problem_rows = passenger_df[passenger_df["Metro station name"].isin(passenger_only_stations)]
        passenger_station_info = passenger_problem_rows[["Metro station name", "Line name"]].drop_duplicates().sort_values(["Line name", "Metro station name"])
        print(passenger_station_info.to_string(index=False))
    else:
        print("Таких станций нет")

    print("\nДетали станций, которые есть только в справочнике станций")

    if station_only_stations:
        station_problem_rows = station_df[station_df["Metro station name"].isin(station_only_stations)]
        station_station_info = station_problem_rows[["Metro station name", "Line name"]].drop_duplicates().sort_values(["Line name", "Metro station name"])
        print(station_station_info.to_string(index=False))
    else:
        print("Таких станций нет")

    passenger_pairs = set(zip(passenger_df["Metro station name"], passenger_df["Line name"]))
    station_pairs = set(zip(station_df["Metro station name"], station_df["Line name"]))

    passenger_only_pairs = passenger_pairs - station_pairs
    station_only_pairs = station_pairs - passenger_pairs

    print("\nСтанция + линия")

    print("Уникальных связок в пассажиропотоке:", len(passenger_pairs))
    print("Уникальных связок в справочнике станций:", len(station_pairs))

    print("\nСвязки, которые есть в пассажиропотоке, но отсутствуют в справочнике станций:")

    if passenger_only_pairs:
        for station, line in sorted(passenger_only_pairs):
            print(f"{station} | {line}")
    else:
        print("Таких связок нет")

    print("\nСвязки, которые есть в справочнике станций, но отсутствуют в пассажиропотоке:")

    if station_only_pairs:
        for station, line in sorted(station_only_pairs):
            print(f"{station} | {line}")
    else:
        print("Таких связок нет")

    passenger_pairs_df = passenger_df[["Metro station name", "Line name"]].dropna().drop_duplicates()
    station_pairs_df = station_df[["Metro station name", "Line name"]].dropna().drop_duplicates()

    all_pairs = pd.concat([passenger_pairs_df, station_pairs_df], ignore_index=True)
    all_pairs = all_pairs.drop_duplicates().reset_index(drop=True)
    all_pairs = all_pairs.sort_values(["Line name", "Metro station name"]).reset_index(drop=True)

    print("\nОбщий справочник станция + линия")

    print("Всего уникальных связок:", len(all_pairs))
    print(all_pairs.to_string(index=False))

    duplicated_pairs = all_pairs.duplicated(subset=["Metro station name", "Line name"]).sum()

    print("\nДубликатов в общем справочнике:", duplicated_pairs)