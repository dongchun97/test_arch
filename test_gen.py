# generator/generator.py
from core import DataLoader
from core import FrameGeometryCalculator

# from structure import Assembler

# from geometry import create_pillars


class ArchitectureGenerator:
    def __init__(self, building_data, calculator, assembler):
        """
        通过依赖注入传入所需组件，不在init中创建
        """
        self.building_data = building_data  # 已经加载好的数据
        self.calculator = calculator  # 已经创建的计算器
        # self.assembler = assembler          # 已经创建的组装器

    @classmethod
    def create_from_file(cls, data_path, config_manager, row=0):
        """工厂方法：从文件创建生成器"""
        # 加载数据
        loader = DataLoader(data_path, config_manager)
        building_data = loader.get_building_data(row)

        # 创建依赖组件
        # calculator = FrameGeometryCalculator(config_manager)
        # assembler = BuildingAssembler(config_manager)

        # 创建生成器实例
        return cls(building_data)  # calculator)  , assembler)


if __name__ == "__main__":
    # 使用
    # config_manager = ConfigManager()
    generator = ArchitectureGenerator.create_from_file("data/buildings.csv", row=0)
