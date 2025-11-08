from core import DataLoader
from core import CalculatorFactory
from configs import RuleEngine, ConfigManager, RuleManager


class Generator:
    def __init__(self):
        self.data_loader = DataLoader()
        self.config_manager = RuleManager("configs/rules")
        self.rule_engine = RuleEngine(self.config_manager)

    def run(self):
        # Step 1: 加载数据（建筑信息）
        data = self.data_loader.load_data()

        # Step 2: 根据 category_info 获取建筑类型
        category = data["category_info"]["building_category"]

        # Step 3: 根据规则表查询对应配置
        rule = self.rule_manager.get_rule(category)
        config = self.config_loader.load_config(rule["config_file"])

        # Step 4: 创建正确的计算器实例
        calculator = CalculatorFactory.create(rule["calculator_class"], config)

        # Step 5: 执行计算
        result = calculator.compute(data)
        return result


if __name__ == "__main__":
    # csv_data = "data/data.csv"
    # gen = Generator(csv_data, row=0)
    # gen.run()

    from pathlib import Path
    from configs.rule_manager import RuleManager
    from core.calculator_factory import CalculatorFactory

    rule_manager = RuleManager(Path("configs/rules"))
    factory = CalculatorFactory(rule_manager)

    calculator = factory.create("house")
    result = calculator.compute("四檩卷棚小式")

    print("\n计算结果：")
    for k, v in result.items():
        print(f"{k}: {v}")
