# generator.py
# 简化后的自动建模生成器，负责调度各模块逻辑

from core.data_manager import DataManager
from structure.assembler import Assembler
from structure.collection import Collection


class Generator:
    """
    统一的建筑生成器
    职责：
    1. 加载并解析数据
    2. 调用尺寸计算模块（DataManager）
    3. 调用装配模块（Assembler）生成建筑
    4. 管理集合层级（Collection）
    """

    def __init__(self, csv_path: str, row_index: int = 0):
        self.csv_path = csv_path
        self.row_index = row_index

        self.data_manager = None
        self.collection = None
        self.assembler = None

        # 数据缓存
        self.building_data = {}
        self.calc_results = {}

    def prepare_data(self):
        """加载与计算建筑数据"""
        self.data_manager = DataManager(self.csv_path)
        self.building_data = self.data_manager.get_building_data(self.row_index)
        self.calc_results = self.data_manager.calculate_dimensions(self.building_data)

    def build_structure(self):
        """建立建筑系统并组装"""
        self.collection = Collection(self.building_data["basic_info"])
        self.assembler = Assembler(
            calc_data=self.calc_results,
            collection=self.collection
        )
        building_obj = self.assembler.build_building()
        return building_obj

    def run(self):
        """执行完整流程"""
        print(" 正在加载与计算数据...")
        self.prepare_data()

        print(" 正在生成建筑结构...")
        building = self.build_structure()

        print(" 建筑生成完成！")
        return building


if __name__ == "__main__":
    gen = Generator("data/data.csv", row_index=0)
    gen.run()
