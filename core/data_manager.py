# generator.py
from core.data_loader import DataLoader
from core.component_calculator import ComponentCalculator
from structure.assembler import Assembler

class Generator:
    """
    统一生成流程控制器：
    1. 加载数据（DataLoader）
    2. 计算构件与位置（ComponentCalculator）
    3. 组装建筑（Assembler）
    """

    def __init__(self, data_path, row=0):
        self.data_path = data_path
        self.row = row
        self.loader = DataLoader(data_path)
        self.calculator = None
        self.assembler = None

    def run(self):
        """完整生成流程"""
        # Step 1: 加载数据
        building_data = self.loader.get_building_data(self.row)
        basic_info = building_data["basic_info"]
        dimension_info = building_data["dimension_info"]

        # Step 2: 计算构件数据
        self.calculator = ComponentCalculator(dimension_info)
        calc_data = self.calculator.calculate_all()

        # Step 3: 组装模型
        self.assembler = Assembler(
            basic_info=basic_info,
            calc_data=calc_data
        )
        self.assembler.build()

        print(f"✅ {basic_info['name']} 建筑生成完成。")

if __name__ == "__main__":
    gen = Generator("data/data2.csv", row=0)
    gen.run()
