import numpy as np
import tomllib


class DataLoader:
    def __init__(self, path):
        self.path = path
        self.headers = []
        self.data = None

    def load_csv(self) -> np.ndarray:
        raw_data = np.genfromtxt(self.path, delimiter=",", dtype=str, encoding="utf-8")
        self.headers = raw_data[0, :].tolist()
        self.data = raw_data[2:, :]
        return self.data

    def get_header_index(self, field_name: str) -> int:
        return self.headers.index(field_name)

    def get_value(self, row: np.ndarray, field_name: str, as_float: bool = False):
        idx = self.get_header_index(field_name)
        val = str(row[idx]).strip()
        if as_float:
            try:
                return float(val) if val else np.nan
            except ValueError:
                return np.nan
        return val

    def get_arch_data(self, row_index: int):
        row = self.data[row_index]
        return {
            "建筑编号": self.get_value(row, "建筑编号"),
            "楹": self.get_value(row, "楹"),
            "明间": self.get_value(row, "明间", True),
            "次间": self.get_value(row, "次间", True),
            "二次间": self.get_value(row, "二次间", True),
            "三次间": self.get_value(row, "三次间", True),
        }


if __name__ == "__main__":
    loader = DataLoader("./data/data-2.csv")
    loader.load_csv()
    print(loader.get_arch_data(2))
