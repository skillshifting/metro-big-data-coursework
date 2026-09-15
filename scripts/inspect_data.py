from pathlib import Path
import os

import pandas as pd

import library


class DataFolderScanner:
    def __init__(self, folder_path):
        self.__folder_path = folder_path

    @property
    def folder_path(self):
        return self.__folder_path

    @property
    def get_files(self):
        return [item for item in self.folder_path.iterdir() if item.is_file() and item.suffix.lower() == ".csv"]

    def has_file(self):
        return any(item.is_file() and item.suffix.lower() == ".csv" for item in self.folder_path.iterdir())

    def validate_or_raise(self):
        if not self.folder_path.exists():
            raise ValueError(f"Папка не существует: {self.folder_path}")

        if not self.folder_path.is_dir():
            raise ValueError(f"Указанный путь не является папкой: {self.folder_path}")

        if not self.has_file():
            raise ValueError(f"В папке нет CSV-файлов: {self.folder_path}")

    def print_file_names_and_weights(self):
        self.validate_or_raise()

        for item in self.get_files:
            size_kb = os.path.getsize(item) / 1024
            size_mb = size_kb / 1024
            print(f"Файл {item.name} весит {size_kb:.3f}КБ {size_mb:.3f}МБ")


class DataSetScanner:
    def __init__(self, file_path):
        if not file_path.is_file():
            raise ValueError(f"По пути {file_path} нет файла")

        self.__file_path = file_path
        self.__df = pd.read_csv(self.file_path, sep=";")
        self.__df = self.clean_data(self.__df)

    @property
    def df(self):
        return self.__df

    @property
    def file_path(self):
        return self.__file_path

    def clean_data(self, df):
        df = df.loc[:, ~df.columns.str.contains("^Unnamed", case=False)]

        if not df.empty:
            first_row = df.iloc[0].astype(str).values

            if any(marker in first_row for marker in library.markers):
                df = df.drop(index=0).reset_index(drop=True)

        if "Quarter" in df.columns:
            df["Quarter"] = df["Quarter"].astype(str).str.strip().replace({
                "Iквартал": "I квартал",
                "IIквартал": "II квартал",
                "IIIквартал": "III квартал",
                "IVквартал": "IV квартал"
            })

        return self.convert_types(df)

    def convert_types(self, df):
        for column in library.numeric_columns:
            if column in df.columns:
                df[column] = pd.to_numeric(df[column], errors="coerce")

        return df

    def drop_sparse_columns(self, threshold=0.95):
        missing_ratio = self.__df.isna().mean()
        columns_to_drop = missing_ratio[missing_ratio >= threshold].index.tolist()

        if columns_to_drop:
            self.__df = self.__df.drop(columns=columns_to_drop)

        return columns_to_drop

    def get_basic_summary(self):
        return {
            "shape": self.__df.shape,
            "columns": self.__df.columns.tolist(),
            "dtypes": self.__df.dtypes.astype(str).to_dict(),
            "missing_values": self.__df.isna().sum().to_dict()
        }

    def get_unique_values(self):
        info = {}

        if "Metro station name" in self.__df.columns:
            info["unique_stations"] = int(self.__df["Metro station name"].nunique())

        if "Line name" in self.__df.columns:
            info["unique_lines"] = int(self.__df["Line name"].nunique())

        if "Year" in self.__df.columns:
            info["years"] = sorted(self.__df["Year"].dropna().unique().tolist())

        if "Quarter" in self.__df.columns:
            info["quarters"] = self.__df["Quarter"].dropna().unique().tolist()

        return info

    def check_duplicates(self):
        result = {}

        if "global_id" in self.__df.columns:
            result["global_id_duplicates"] = int(self.__df.duplicated(subset=["global_id"]).sum())

        passenger_subset = ["Metro station name", "Line name", "Year", "Quarter"]

        if all(column in self.__df.columns for column in passenger_subset):
            result["station_period_duplicates"] = int(self.__df.duplicated(subset=passenger_subset).sum())

        return result

    def check_numeric_ranges(self):
        required_columns = ["Incoming passengers", "Outgoing passengers"]

        if not all(column in self.__df.columns for column in required_columns):
            return "Проверка пассажиропотока для этого файла неприменима"

        incoming = self.__df["Incoming passengers"]
        outgoing = self.__df["Outgoing passengers"]

        zero_mask = (incoming == 0) | (outgoing == 0)

        result = {
            "incoming_min": int(incoming.min()),
            "incoming_max": int(incoming.max()),
            "outgoing_min": int(outgoing.min()),
            "outgoing_max": int(outgoing.max()),
            "zero_rows": int(zero_mask.sum())
        }

        if all(column in self.__df.columns for column in ["Year", "Quarter"]):
            result["zero_by_period"] = self.__df[zero_mask].groupby(["Year", "Quarter"]).size().to_dict()

        if "Metro station name" in self.__df.columns:
            result["zero_by_station"] = self.__df[zero_mask].groupby("Metro station name").size().sort_values(ascending=False).to_dict()

        return result

    def check_missing_values(self):
        missing = self.__df.isna().sum()
        missing = missing[missing > 0]

        if missing.empty:
            return "Пропусков нет"

        return missing.to_dict()

    def get_missing_percentage(self):
        missing_percentage = self.__df.isna().mean().mul(100)
        missing_percentage = missing_percentage[missing_percentage > 0].round(2)

        if missing_percentage.empty:
            return {}

        return missing_percentage.to_dict()

    def get_rows_with_missing_values(self):
        missing_mask = self.__df.isna().any(axis=1)
        return self.__df[missing_mask]


if __name__ == "__main__":
    folder_path = Path(__file__).resolve().parents[1] / "data" / "raw"

    scanner = DataFolderScanner(folder_path)
    scanner.print_file_names_and_weights()

    for item in scanner.get_files:
        print(f"\n{'=' * 70}")
        print(f"Файл: {item.name}")
        print(f"{'=' * 70}\n")

        dataset_scanner = DataSetScanner(item)

        dropped_columns = dataset_scanner.drop_sparse_columns()

        if dropped_columns:
            print(f"Удалены почти полностью пустые столбцы: {dropped_columns}")
        else:
            print("Почти полностью пустых столбцов нет")

        print("\nОбщая информация")
        print(dataset_scanner.get_basic_summary())

        print("\nУникальные значения")
        print(dataset_scanner.get_unique_values())

        print("\nИнформация по дубликатам")
        print(dataset_scanner.check_duplicates())

        print("\nИнформация по пассажиропотоку")
        print(dataset_scanner.check_numeric_ranges())

        print("\nИнформация по пропускам")
        print(dataset_scanner.check_missing_values())

        print("\nПроцент пропусков")
        print(dataset_scanner.get_missing_percentage())

        missing_rows = dataset_scanner.get_rows_with_missing_values()

        if not missing_rows.empty:
            print("\nСтроки с пропусками")
            print(missing_rows.to_string(index=False))