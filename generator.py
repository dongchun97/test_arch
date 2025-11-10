from core import DataLoader, FormInferencer
from core import CalculatorFactory
from configs import ConfigManager


class Generator:
    def __init__(self, raw_csv_path: str, row: int):
        self.csv_loader = DataLoader(raw_csv_path)
        self.config_mgr = ConfigManager()
        self.calc = CalculatorFactory()

        self.row = row

    def run(self):
        # Step 1: 加载数据（建筑信息）
        initial_building_data = self.csv_loader.get_complete_building_data(self.row)

        # Step 2: 根据加载的建筑信息增加推断形态，完善建筑信息
        infer = FormInferencer(initial_building_data)

        building_data = infer.building_data
        building_construction_name = infer.infer_form_name()

        print(self.calc.create_calculator(building_data))

        # Step 2: 获取建筑数据
        # basic_info = building_data["basic_info"]
        # category_info = building_data["category_info"]
        # dimension_info = building_data["dimension_info"]

        # category = category_info["building_category"]

        # Step 3: 根据规则表查询对应配置
        # rule = self.config_mgr.get_class_mapping(category)
        # config = self.config_loader.load_config(rule["config_file"])

        # # Step 4: 创建正确的计算器实例
        # calculator = CalculatorFactory.create(rule["calculator_class"], config)

        # # Step 5: 执行计算
        # result = calculator.compute(building_data)
        # return result


if __name__ == "__main__":
    raw_csv_path = "data/data.csv"
    gen = Generator(raw_csv_path, row=1)
    gen.run()

    # from pathlib import Path
    # from configs.config_mgr import ConfigManager
    # from core.calculator_factory import CalculatorFactory

    # config_mgr = ConfigManager(Path("configs/rules"))
    # factory = CalculatorFactory(config_mgr)

    # calculator = factory.create("house")
    # result = calculator.compute("四檩卷棚小式")

    # print("\n计算结果：")
    # for k, v in result.items():
    #     print(f"{k}: {v}")
