from core import DataLoader, FormInferencer
from core import CalculatorFactory
from configs import RuleManager


class Generator:
    def __init__(self, csv_path: str, row: int = None):
        self.data_loader = DataLoader(csv_path)
        self.rule_manager = RuleManager("configs/rules")

        self.row = row

    def run(self):
        # Step 1: 加载数据（建筑信息）
        data = self.data_loader.get_complete_building_data(self.row)

        # Step 2: 获取建筑数据
        basic_info = data["basic_info"]
        category_info = data["category_info"]
        dimension_info = data["dimension_info"]

        category = data["category_info"]["building_category"]

        # # Step 3: 根据规则表查询对应配置
        # rule = self.rule_manager.get_rule(category)
        # config = self.config_loader.load_config(rule["config_file"])

        # # Step 4: 创建正确的计算器实例
        # calculator = CalculatorFactory.create(rule["calculator_class"], config)

        # # Step 5: 执行计算
        # result = calculator.compute(data)
        # return result
        print(category)


if __name__ == "__main__":
    csv_data = "data/data.csv"
    gen = Generator(csv_data, row=1)
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
