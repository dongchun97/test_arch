# generator/generator.py
from core import DataLoader
from core import generate_frame_geometry
# from structure import Assembler

def process_data_file(file_path):
    """主流程协调器"""
    # 1. 加载数据
    loader = DataLoader(file_path)
    return loader
    
    # 2. 标准化命名
    # naming_service = NamingService('configs/naming_standard.toml')
    # standardized_data = naming_service.standardize_columns(raw_data)
    
    # # 3. 结构化数据
    # structurer = Assembler()
    # structured_objects = structurer.create_objects(standardized_data)
    
    # 4. 返回或保存结果
    # return structured_objects

# 提供简化接口
def generator(file_path):
    return process_data_file(file_path)


if __name__ == "__main__":
    loader=process_data_file("data/data-2.csv")
    data=loader.get_building_data(1)

    purlin,dimension,*_=data['dimension_info'].values()
    print(dimension)
    # generate_frame_geometry(dimensions)


    # # 获取第一个建筑的数据
    # building = loader.get_building_data(1)
    # print(building)
