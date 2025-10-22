# data_loader.py
# 负责数据读取和结构化，不包含计算逻辑

import numpy as np
from typing import Dict, Any


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
        self.csv_data = None
        self.building_data = None

        self._load_csv()


    def _load_csv(self) -> np.ndarray:
        """加载CSV数据"""

        raw_data = np.genfromtxt(self.path, delimiter=",", dtype=str, encoding="utf-8")
        self.headers = raw_data[0, :].tolist()
        self.csv_data = raw_data[2:, :]

        return self.csv_data

    def get_str_value(
        self, row: np.ndarray, field_name: str, as_float: bool = False
    ) -> Any:
        try:
            idx = self.headers.index(field_name)
            val = str(row[idx]).strip()

            if as_float:
                try:
                    return float(val) if val else np.nan
                except ValueError:
                    return np.nan
            return val
        except Exception as e:
            return np.nan if as_float else ""

    def get_building_data(self, row_index: int) -> Dict[str, Any]:
        """获取指定行的建筑数据

        Args:
            row_index: 行索引

        Returns:
            结构化的建筑数据字典
        """
        if self.csv_data is None:
            raise ValueError("数据尚未加载。请先调用 load_csv。")

        if row_index < 0 or row_index >= len(self.csv_data):
            raise ValueError(f"行索引 {row_index} 超出范围")

        row = self.csv_data[row_index]

        # 1. 基础信息
        basic_info = {
            "garden_name": self.get_str_value(row, "园林名称"),
            "garden_id": self.get_str_value(row, "园中园编号"),
            "sub_garden_name": self.get_str_value(row, "园中园名称"),
            "building_id": self.get_str_value(row, "建筑编号"),
            "building_name": self.get_str_value(row, "建筑名称"),
        }

        # 2. 构造信息
        structure_info = {
            "building_category": self.get_str_value(row, "建筑类别"),
            "sub_category": self.get_str_value(row, "建筑子类"),
            "construction_grades": self.get_str_value(row, "建筑等级"),
            "roof_forms": self.get_str_value(row, "屋顶形式"),
            "ridge_types": self.get_str_value(row, "屋脊类型"),
            "corridor": self.get_str_value(row, "出廊"),
        }

        # 3. 描述信息
        description_info = {
            "form": self.get_str_value(row, "描述1"),
        }

        # 5. 尺寸信息
        # 5.1 面阔数据
        all_bays = np.array(
            [
                self.get_str_value(row, "明间", True),
                self.get_str_value(row, "次间", True),
                self.get_str_value(row, "二次间", True),
                self.get_str_value(row, "三次间", True),
            ]
        )

        bay_widths = all_bays[~np.isnan(all_bays)]
        bays = len(bay_widths) * 2 - 1

        # 5.2 进深数据
        depth_total = np.array(self.get_str_value(row, "通进深", True))
        eave_step = np.array(self.get_str_value(row, "檐步架", True))



        # 组合所有数据
        self.building_data = {
            "basic_info": basic_info,
            "structure_info": structure_info,
            "description_info": description_info,
            "dimension_info": {
                "num_bays": bays,
                "bay_widths": bay_widths.tolist(),
                "depth_total": depth_total,
                "eave_step": eave_step,
            },
        }

        return self.building_data


# 示例用法
if __name__ == "__main__":
    # 创建加载器
    loader = DataLoader("data/data-2.csv")
    print(loader.get_building_data(1))

    # 获取第一个建筑的数据
    # building = loader.get_building_data(1)
    # print(building)
