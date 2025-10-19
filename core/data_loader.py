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
        self.data = None
        self.building_data = None

    def load_csv(self) -> np.ndarray:
        """加载CSV数据"""

        raw_data = np.genfromtxt(self.path, delimiter=",", dtype=str, encoding="utf-8")
        self.headers = raw_data[0, :].tolist()
        self.data = raw_data[2:, :]

        return self.data

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
        if self.data is None:
            raise ValueError("数据尚未加载。请先调用 load_csv。")

        if row_index < 0 or row_index >= len(self.data):
            raise ValueError(f"行索引 {row_index} 超出范围")

        row = self.data[row_index]

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
            "construction": self.get_str_value(row, "建筑形式"),
            "corridor": self.get_str_value(row, "出廊"),
        }

        # 3. 描述信息
        description_info = {
            "form": self.get_str_value(row, "描述1"),
        }

        num_lintels = None
        construction = structure_info.get("construction")
        if "四檩" in construction:
            num_lintels = 4
        elif "五檩" in construction:
            num_lintels = 5
        elif "六檩" in construction:
            num_lintels = 6
        elif "七檩" in construction:
            num_lintels = 7
        elif "八檩" in construction:
            num_lintels = 8

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

        # 5.3 檐柱径
        D = all_bays[0] * 0.8

        # 组合所有数据
        self.building_data = {
            "basic_info": basic_info,
            "structure_info": structure_info,
            "description_info": description_info,
            "dimension_info": {
                "num_lintels": num_lintels,
                "num_bays": bays,
                "bay_widths": bay_widths.tolist(),
                "depth_total": float(depth_total),
                "eave_step": float(eave_step),
                "D": float(D),
            },
        }

        return self.building_data


# 示例用法
if __name__ == "__main__":
    # 创建加载器
    loader = DataLoader("data/data-2.csv")
    # loader.load_csv()
    # array=loader.data
    print(loader.get_building_data(1))

    # 获取第一个建筑的数据
    # building = loader.get_building_data(1)
    # print(building)
