# generator/generator.py
from core import DataLoader
from core import FrameGeometryCalculator

# from structure import Assembler


def process_data_file(file_path):
    """主流程协调器"""

    loader = DataLoader(file_path)      # 1. 加载数据
    
    data=loader.get_building_data(1)            # 2. 加载数据行

    # 2. 计算数据
    dimension=data['dimension_info']
    result=FrameGeometryCalculator(**dimension)
    print(result.beams)

    # # 3. 结构化数据
    # structurer = Assembler()
    # structured_objects = structurer.create_objects(standardized_data)

    # 4. 返回或保存结果
    # return structured_objects


# 提供简化接口
def generator(file_path):
    return process_data_file(file_path)


if __name__ == "__main__":
    file_path = "data/data-2.csv"
    process_data_file(file_path)


    # generate_frame_geometry(dimensions)


    # # 获取第一个建筑的数据
    # building = loader.get_building_data(1)
    # print(building)
