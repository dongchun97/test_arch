from abc import ABC, abstractmethod
from typing import Dict, Any, List
import numpy as np


class BaseFormatter(ABC):
    """格式化器基类"""

    def __init__(self, headers: List[str]):
        self.headers = headers

    def _get_header_index(self, field_name: str) -> int:
        """获取字段在CSV中的列索引"""
        return self.headers.index(field_name)

    def _get_value(
        self, row: np.ndarray, field_name: str, as_float: bool = False
    ) -> Any:
        """根据列名获取行中对应值"""
        try:
            idx = self._get_header_index(field_name)
            val = str(row[idx]).strip()
            if as_float:
                try:
                    return float(val) if val else np.nan
                except ValueError:
                    return np.nan
            return val
        except Exception:
            return np.nan if as_float else ""

    @abstractmethod
    def format(self, row: np.ndarray) -> Dict[str, Any]:
        pass


class BasicInfoFormatter(BaseFormatter):
    """基础信息格式化器"""

    def format(self, row: np.ndarray) -> Dict[str, Any]:
        return {
            "garden_name": self._get_value(row, "园林名称"),
            "garden_id": self._get_value(row, "园中园编号"),
            "building_id": self._get_value(row, "建筑编号"),
            "building_name": self._get_value(row, "建筑名称"),
        }


class CategoryInfoFormatter(BaseFormatter):
    """种类信息格式化器"""

    def format(self, row: np.ndarray) -> Dict[str, Any]:
        return {
            "building_category": self._get_value(row, "建筑类别"),
            "sub_category": self._get_value(row, "建筑子类"),
            "roof_forms": self._get_value(row, "屋顶形式"),
            "ridge_types": self._get_value(row, "屋脊类型"),
            "construction_grades": self._get_value(row, "建筑等级"),
            "corridor": self._get_value(row, "出廊"),
        }


class PrecisionInfoFormatter(BaseFormatter):
    """精度信息格式化器"""

    def format(self, row: np.ndarray) -> Dict[str, Any]:
        return {
            "pricision": self._get_value(row, "模型精度"),
        }


class DimensionInfoFormatter(BaseFormatter):
    """尺寸信息格式化器"""

    def format(self, row: np.ndarray) -> Dict[str, Any]:
        # 面阔数据
        all_bays = np.array(
            [
                self._get_value(row, "明间", True),
                self._get_value(row, "次间", True),
                self._get_value(row, "二次间", True),
                self._get_value(row, "三次间", True),
            ]
        )

        bay_widths = all_bays[~np.isnan(all_bays)]
        bays = len(bay_widths) * 2 - 1

        # 进深数据
        depth_total = np.array(self._get_value(row, "通进深", True))
        eave_step = np.array(self._get_value(row, "檐步架", True))

        # # 檩数计算
        # num_purlins = int(depth_total // eave_step) + 2
        # if num_purlins == 8:
        #     purlin_name = "八檩"
        # elif num_purlins == 7:
        #     purlin_name = "七檩"
        # elif num_purlins == 6:
        #     purlin_name = "六檩"
        # elif num_purlins == 5:
        #     purlin_name = "五檩"
        # else:
        #     purlin_name = "四檩"

        # # 结构名称
        # ridge_types = self._get_value(row, "屋脊类型")
        # construction_grades = self._get_value(row, "建筑等级")
        # # structure_name = f"{purlin_name}{ridge_types}{construction_grades}"

        return {
            # "num_lin": num_purlins,
            "num_bays": bays,
            "bay_widths": bay_widths,
            "depth_total": depth_total,
            "eave_step": eave_step,
            # "structure_name": structure_name,
        }


class DataLoader:
    """数据加载器 - 重构版本
    职责：
    1. 读取CSV数据
    2. 按需提供结构化的建筑数据
    3. 支持批量数据获取
    """

    def __init__(self, path: str):
        self.path = path
        self.headers = []
        self.raw_data = None
        self._formatters = {}
        self._building_cache = {}  # 缓存格式化的建筑数据

        # 初始化格式化器
        self._init_formatters()
        # 加载原始数据
        self._load_raw_data()

    def _init_formatters(self):
        """初始化所有格式化器"""
        # 注意：这里先创建格式化器，但headers在_load_raw_data后设置
        self._formatters = {
            "basic_info": BasicInfoFormatter,
            "category_info": CategoryInfoFormatter,
            "precision_info": PrecisionInfoFormatter,
            "dimension_info": DimensionInfoFormatter,
        }

    def _load_raw_data(self):
        """加载原始CSV数据"""
        self.raw_data = np.genfromtxt(
            self.path, delimiter=",", dtype=str, encoding="utf-8"
        )
        self.headers = self.raw_data[0, :].tolist()

        # 设置格式化器的headers
        for formatter_class in self._formatters.values():
            formatter_class.headers = self.headers

    def get_building_section(self, row_index: int, section_key: str) -> Dict[str, Any]:
        """获取指定建筑的特定数据段（懒加载）"""
        self._validate_row_index(row_index)

        cache_key = f"{row_index}_{section_key}"

        if cache_key not in self._building_cache:
            formatter_class = self._formatters.get(section_key)
            if not formatter_class:
                raise ValueError(f"未知的数据段: {section_key}")

            row = self.raw_data[2 + row_index]  # 跳过表头和说明行
            formatter = formatter_class(self.headers)
            self._building_cache[cache_key] = formatter.format(row)

        return self._building_cache[cache_key]

    def get_complete_building_data(self, row_index: int) -> Dict[str, Any]:
        """获取完整的建筑数据（一次性获取所有段）"""
        self._validate_row_index(row_index)

        cache_key = f"{row_index}_complete"

        if cache_key not in self._building_cache:
            building_data = {}
            for section_key in self._formatters.keys():
                building_data[section_key] = self.get_building_section(
                    row_index, section_key
                )
            self._building_cache[cache_key] = building_data

        return self._building_cache[cache_key]

    def get_all_buildings(self) -> List[Dict[str, Any]]:
        """获取所有建筑的完整数据（批量处理）"""
        buildings = []
        for i in range(len(self.raw_data) - 2):  # 跳过表头和说明行
            buildings.append(self.get_complete_building_data(i))
        return buildings

    def get_building_count(self) -> int:
        """获取建筑数量"""
        return len(self.raw_data) - 2 if self.raw_data is not None else 0

    def _validate_row_index(self, row_index: int):
        """验证行索引有效性"""
        if self.raw_data is None:
            raise ValueError("数据尚未加载")
        if row_index < 0 or row_index >= len(self.raw_data) - 2:
            raise ValueError(f"行索引 {row_index} 超出范围 [0, {len(self.raw_data)-3}]")

    def clear_cache(self):
        """清空缓存（用于内存管理）"""
        self._building_cache.clear()


if __name__ == "__main__":
    # 初始化
    loader = DataLoader("data/data.csv")

    # 方式1：按需获取特定数据段（懒加载）
    # basic_info = loader.get_building_section(0, "basic_info")
    # dimension_info = loader.get_building_section(0, "dimension_info")
    # print(basic_info)
    # print(dimension_info)

    # # 方式2：获取完整建筑数据
    complete_data = loader.get_complete_building_data(0)
    print(complete_data)
    # print(complete_data["basic_info"]["building_name"])
    # print(complete_data["dimension_info"]["structure_name"])

    # # 方式3：批量处理所有建筑
    # all_buildings = loader.get_all_buildings()
    # for building in all_buildings:
    #     print(f"建筑: {building['basic_info']['building_name']}")

    # # 方式4：遍历处理
    # for i in range(loader.get_building_count()):
    #     basic = loader.get_building_section(i, "basic_info")
    #     if basic["garden_name"] == "目标园林":
    #         dimension = loader.get_building_section(i, "dimension_info")
    # 处理逻辑...
