from core import DataLoader
import os

path = os.path.dirname(os.path.dirname(__file__))


# # 使用示例
# def main():
#     # 初始化加载器
#     loader = DataLoader(path + "/data/data-2.csv")

#     # 加载CSV数据
#     loader.load_csv()

#     # 获取所有建筑的结构化数据
#     all_buildings = loader.get_structured_building_data()

#     for building in all_buildings:
#         print("=== 建筑数据 ===")
#         print(f"一级集合: {building['collections']['level_1']['name']}")
#         print(f"二级集合: {building['collections']['level_2']['name']}")
#         print(f"建筑形式: {building['config']['building_form']}")
#         print(f"开间数: {building['config']['columns_count']}")
#         print(f"开间宽度: {[bay['width'] for bay in building['geometry']['bays']]}")

#         # 这些数据可以直接用于后续模块
#         collection_name = building["collections"]["level_2"]["name"]
#         # structure模块可以直接使用这个集合名称


# # 或者获取单行数据
# single_building = loader.get_structured_building_data(0)  # 第一行
