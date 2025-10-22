# generator/generator.py
from core import DataLoader
from core import FrameGeometryCalculator

# from structure import Assembler

# from geometry import create_pillars


class Generator:
    def __init__(self, data_path):
        self.data_path = data_path
        self.building_data = None
        self.calc_results = None

    def load_data(self, row=0):
        loader = DataLoader(self.data_path)
        loader.load_csv()
        self.building_data = loader.get_building_data(row)

    def compute(self):
        building_dimension_info = self.building_data["dimension_info"]
        calc = FrameGeometryCalculator(**building_dimension_info)
        self.calc_results = calc.compute_all()

    # def assembler(self):
    #     structurer = Assembler()
    #     return structurer

    def run(self, row=0):
        self.load_data(row)
        self.compute()
        # return self.calc_results


if __name__ == "__main__":
    gen = Generator("./data/data-2.csv")
    gen.run()
    print(type(gen.calc_results["walls"]))

    # import json
    # import numpy as np

    # def convert_numpy_types(obj):
    #     """递归转换numpy类型为Python原生类型"""
    #     if isinstance(obj, dict):
    #         return {key: convert_numpy_types(value) for key, value in obj.items()}
    #     elif isinstance(obj, list):
    #         return [convert_numpy_types(item) for item in obj]
    #     elif isinstance(obj, np.integer):
    #         return int(obj)
    #     elif isinstance(obj, np.floating):
    #         return float(obj)
    #     elif isinstance(obj, np.ndarray):
    #         return obj.tolist()
    #     elif isinstance(obj, np.bool_):
    #         return bool(obj)
    #     else:
    #         return obj

    # # 先转换再保存
    # converted_result = convert_numpy_types(result)
    # with open("./test/result.json", "w") as f:
    #     json.dump(converted_result, f, indent=4)
