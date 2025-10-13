# data_loader.py
# 负责数据读取和结构化，不包含计算逻辑

import numpy as np
import logging
from typing import Dict, Any


logger = logging.getLogger("ArchBuilder.DataLoader")
 

class DataLoader:
    """数据加载器
    职责：
    1. 读取CSV数据
    2. 提供结构化的建筑数据
    3. 支持建筑数据获取功能
    """

    def __init__(self, path: str):
        self.path = path
        self.headers = []
        self.data = None
        self.building_data = None
        logger.info(f"初始化数据加载器，文件路径: {path}")

    def load_csv(self) -> np.ndarray:
        """加载CSV数据"""
        try:
            logger.info(f"开始读取CSV文件: {self.path}")
            raw_data = np.genfromtxt(
                self.path, delimiter=",", dtype=str, encoding="utf-8"
            )
            self.headers = raw_data[0, :].tolist()
            self.data = raw_data[2:, :]
            logger.info(f"成功加载数据，共 {len(self.data)} 行")
            return self.data
        except Exception as e:
            logger.error(f"读取CSV文件失败: {str(e)}")
            raise

    def get_header_index(self, field_name: str) -> int:
        """获取字段索引"""
        try:
            return self.headers.index(field_name)
        except ValueError:
            logger.error(f"字段 '{field_name}' 不存在")
            raise ValueError(f"字段 '{field_name}' 不存在")

    def get_value(
        self, row: np.ndarray, field_name: str, as_float: bool = False
    ) -> Any:
        """获取字段值"""
        try:
            idx = self.get_header_index(field_name)
            val = str(row[idx]).strip()

            if as_float:
                try:
                    return float(val) if val else np.nan
                except ValueError:
                    return np.nan
            return val
        except Exception as e:
            logger.warning(f"获取字段 {field_name} 值时出错: {str(e)}")
            return np.nan if as_float else ""

    def get_building_data(self, row_index: int) -> Dict[str, Any]:
        """获取指定行的建筑数据

        Args:
            row_index: 行索引

        Returns:
            结构化的建筑数据字典
        """
        if self.data is None:
            raise ValueError("数据尚未加载。请先调用 load_csv。")

        if row_index < 0 or row_index >= len(self.data):
            raise ValueError(f"行索引 {row_index} 超出范围")

        row = self.data[row_index]

        # 1. 基础信息
        basic_info = {
            "garden_name": self.get_value(row, "园林名称"),
            "garden_id": self.get_value(row, "园中园编号"),
            "sub_garden_name": self.get_value(row, "园中园名称"),
            "garden_area": self.get_value(row, "园中园区域属性"),
            "building_id": self.get_value(row, "建筑编号"),
            "building_name": self.get_value(row, "建筑名称"),
        }

        # 2. 构造信息
        structure_info = {
            "construction": self.get_value(row, "构造"),
            "combination": self.get_value(row, "组合"),
            "doukou": self.get_value(row, "斗口"),
            "corridor": self.get_value(row, "出廊"),
            "shoushan": self.get_value(row, "收山"),
            "purlin_count": int(self.get_value(row, "檩", True)),
        }

        # 3. 描述信息
        description_info = {
            "form": self.get_value(row, "描述1-形态"),
            "orientation": self.get_value(row, "描述2-朝向"),
            "level": self.get_value(row, "描述3-等级"),  # 建筑等级
            "bay_count": int(self.get_value(row, "描述4-楹", True)),
            "gable": self.get_value(row, "描述5-山墙"),
            "dougong": self.get_value(row, "描述6-斗拱"),
        }

        # 4. 模型精度
        precision_levels = {
            "precision": self.get_value(row, "模型精度"),  # 建模精度等级
        }

        # 5. 尺寸信息
        # 5.1 面阔数据
        all_bays = np.array(
            [
                self.get_value(row, "明间", True),
                self.get_value(row, "次间", True),
                self.get_value(row, "二次间", True),
                self.get_value(row, "三次间", True),
            ]
        )

        span_data = {
            "main_bay": self.get_value(row, "明间", True),
            "all_bays": all_bays[~np.isnan(all_bays)],
        }

        # 5.2 进深数据
        depth_data = {
            "total": np.array(self.get_value(row, "通进深", True)),
            "eave_step": np.array(self.get_value(row, "檐步架", True)),
        }

        # 5.3 高度数据
        annotated_height_data = {
            "annotated_column_height": np.array(
                self.get_value(row, "标注檐柱高", True)
            ),
            "annotated_column_diameter": np.array(
                self.get_value(row, "标注柱径", True)
            ),
            "annotated_pedestal_height": np.array(
                self.get_value(row, "标注台明高", True)
            ),
        }

        # 5.4 出檐数据
        annotated_overhang_data = {
            "upper": np.array(self.get_value(row, "标注上出", True)),
            "lower": np.array(self.get_value(row, "标注下出", True)),
        }

        # 6. 材料信息
        material_info = {
            "brick_type": self.get_value(row, "砖类别"),
            "tile_type": self.get_value(row, "瓦类别"),
            "stone_type": self.get_value(row, "石类别"),
            "stair_type": self.get_value(row, "踏跺类型"),
        }

        # 7. 装修信息
        decoration_info = {
            "front": {
                "main_bay": self.get_value(row, "前檐装修明间"),
                "side_bays": [
                    self.get_value(row, "次间_1"),
                    self.get_value(row, "次间_2"),
                    self.get_value(row, "次间_3"),
                ],
            },
            "back": {
                "main_bay": self.get_value(row, "后檐装修明间"),
                "side_bays": [
                    self.get_value(row, "次间_4"),
                    self.get_value(row, "二次间_5"),
                    self.get_value(row, "三次间_6"),
                ],
            },
        }

        # 8. 坐标信息
        coordinate_info = {
            "x": self.get_value(row, "X坐标", True),
            "y": self.get_value(row, "Y坐标", True),
            "z": self.get_value(row, "Z坐标", True),
        }

        # 9. 外部链接信息
        external_info = {
            "fbx1": self.get_value(row, "Fbx1"),
            "fbx2": self.get_value(row, "Fbx2"),
        }

        # 组合所有数据
        self.building_data = {
            "basic_info": basic_info,
            "structure_info": structure_info,
            "description_info": description_info,
            "precision_levels": precision_levels,
            "dimension_info": {
                "span": span_data,
                "depth": depth_data,
                "annotated_height": annotated_height_data,
                "annotated_overhang": annotated_overhang_data,
            },
            "material_info": material_info,
            "decoration_info": decoration_info,
            "coordinate_info": coordinate_info,
            "external_info": external_info,
        }

        return self.building_data


# 示例用法
if __name__ == "__main__":
    # 创建加载器
    loader = DataLoader("data/data.csv")
    loader.load_csv()

    # 获取第一个建筑的数据
    building = loader.get_building_data(5)
    print(building)
