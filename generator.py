# generator/generator.py
from core import DataLoader
from core import FrameGeometryCalculator

from geometry import create_pillars

# from structure import Assembler


def process_data_file(file_path):
    """主流程协调器"""

    # 1. 加载数据
    loader = DataLoader(file_path)
    data = loader.get_building_data(1)  # 加载数据行
    dimension = data["dimension_info"]

    # 2. 计算数据

    result = FrameGeometryCalculator(**dimension)
    create_pillars(result)

    # # 3. 结构化数据
    # structurer = Assembler()
    # structured_objects = structurer.create_objects(standardized_data)

    # 4. 返回或保存结果
    # return structured_objects
    return result


# 提供简化接口
def generator(file_path):
    return process_data_file(file_path)


if __name__ == "__main__":
    file_path = "data/data-2.csv"
    building_dimension = generator(file_path)
    print(building_dimension.pillar_coords)

    # generate_frame_geometry(dimensions)

    # # 获取第一个建筑的数据
    # building = loader.get_building_data(1)
    # print(building)
