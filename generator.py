from core import DataLoader, FormInferencer
from core import CalculatorFactory
from configs import RuleManager


class Generator:
    def __init__(self, raw_csv_path: str, row: int):
        self.csv_loader = DataLoader(raw_csv_path)
        self.rule_manager = RuleManager()

        self.row = row

    def run(self):
        # Step 1: 加载数据（建筑信息）
        parsed_building_data = self.csv_loader.get_complete_building_data(self.row)

        # Step 2: 根据加载的建筑信息增加推断形态，完善建筑信息
        infer = FormInferencer(parsed_building_data)
        inferred_building_data=infer.building_data
        inferred_construction_name=infer.infer_form_name()


        # Step 2: 获取建筑数据
        basic_info = inferred_building_data["basic_info"]
        category_info = inferred_building_data["category_info"]
        dimension_info = inferred_building_data["dimension_info"]

        category = category_info["building_category"]

        # Step 3: 根据规则表查询对应配置
        rule = self.rule_manager.get_rule_class_from_json(category)
        # config = self.config_loader.load_config(rule["config_file"])

        # # Step 4: 创建正确的计算器实例
        # calculator = CalculatorFactory.create(rule["calculator_class"], config)

        # # Step 5: 执行计算
        # result = calculator.compute(inferred_building_data)
        # return result
        print(rule)


if __name__ == "__main__":
    raw_csv_path = "data/data.csv"
    gen = Generator(raw_csv_path, row=1)
    gen.run()

    # from pathlib import Path
    # from configs.rule_manager import RuleManager
    # from core.calculator_factory import CalculatorFactory

    # rule_manager = RuleManager(Path("configs/rules"))
    # factory = CalculatorFactory(rule_manager)

    # calculator = factory.create("house")
    # result = calculator.compute("四檩卷棚小式")

    # print("\n计算结果：")
    # for k, v in result.items():
    #     print(f"{k}: {v}")
