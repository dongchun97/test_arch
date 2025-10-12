# core/loader.py
import numpy as np
import os
import yaml, json
from typing import Dict, Any

path = os.path.dirname(os.path.dirname(__file__))


class DataLoader:
    """数据加载器 - 使用numpy和配置映射"""

    def __init__(self, csv_path: str, config_dir: str = None):
        self.csv_path = csv_path
        self.config_dir = config_dir or os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "configs"
        )
        self.headers = []
        self.data = None
        self.mapping_config = self._load_mapping_config()

    def _load_mapping_config(self) -> Dict[str, Any]:
        """加载映射配置"""
        try:
            # 这里应该从YAML文件加载，暂时返回示例配置
            return {
                "csv_header_mapping": {
                    "collection_levels": {
                        "level_1": {
                            "name": "一级集合",
                            "fields": ["园林名称", "园中园编号", "园中园名称"],
                            "naming_template": "COL_{园林名称}_{园中园编号}_{园中园名称}",
                        },
                        "level_2": {
                            "name": "二级集合",
                            "fields": ["建筑编号", "建筑名称"],
                            "naming_template": "COL_{建筑编号}_{建筑名称}",
                        },
                    },
                    "building_config": {
                        "category": "配置信息",
                        "fields": ["建筑形式", "出廊", "楹", "描述1"],
                    },
                    "geometry_data": {
                        "category": "几何数据",
                        "fields": [
                            "明间",
                            "次间",
                            "二次间",
                            "三次间",
                            "四次间",
                            "通进深",
                            "檐步架",
                        ],
                    },
                    "dimension_data": {
                        "category": "标注尺寸",
                        "fields": [
                            "标注檐柱高",
                            "标注柱径",
                            "标注台明高",
                            "标注上出",
                            "标注下出",
                        ],
                    },
                },
                "field_aliases": {
                    "园林名称": "garden_name",
                    "园中园编号": "garden_id",
                    "园中园名称": "sub_garden_name",
                    "建筑编号": "building_id",
                    "建筑名称": "building_name",
                    "建筑形式": "building_form",
                    "出廊": "corridor_type",
                    "楹": "columns_count",
                    "描述1": "description",
                    "明间": "mingjian",
                    "次间": "cijian",
                    "二次间": "ercijian",
                    "三次间": "sancijian",
                    "四次间": "sicijian",
                    "通进深": "total_depth",
                    "檐步架": "eave_step",
                    "标注檐柱高": "annotated_column_height",
                    "标注柱径": "annotated_column_diameter",
                    "标注台明高": "annotated_pedestal_height",
                    "标注上出": "annotated_upper_overhang",
                    "标注下出": "annotated_lower_overhang",
                },
            }
        except Exception as e:
            print(f"加载映射配置失败: {e}")
            return {}

    def load_csv(self) -> np.ndarray:
        """加载CSV数据"""
        try:
            # 使用numpy读取CSV
            raw_data = np.genfromtxt(
                self.csv_path,
                delimiter=",",
                dtype=str,
                encoding="utf-8",
                filling_values="",
            )

            # 处理可能的空行
            valid_rows = []
            for row in raw_data:
                if any(cell.strip() for cell in row):
                    valid_rows.append(row)

            self.headers = [header.strip() for header in valid_rows[0]]
            self.data = np.array(valid_rows[1:])  # 跳过标题行

            print(f"成功加载CSV数据，共 {len(self.data)} 行建筑数据")
            return self.data

        except Exception as e:
            print(f"读取CSV文件失败: {str(e)}")
            raise

    def get_header_index(self, field_name: str) -> int:
        """获取字段索引"""
        try:
            return self.headers.index(field_name)
        except ValueError:
            print(f"字段 '{field_name}' 不存在于CSV头部")
            raise ValueError(f"字段 '{field_name}' 不存在")

    def _clean_value(self, value: str, as_float: bool = False) -> Any:
        """清理数据值"""
        if value is None or value == "":
            return np.nan if as_float else ""

        value_str = str(value).strip()

        # 处理各种NaN表示
        if value_str.lower() in ["nan", "null", "none", ""]:
            return np.nan if as_float else ""

        if as_float:
            try:
                return float(value_str)
            except (ValueError, TypeError):
                return np.nan
        else:
            return value_str

    def get_structured_building_data(self, row_index: int = None) -> Dict[str, Any]:
        """获取结构化的建筑数据"""
        if self.data is None:
            raise ValueError("数据尚未加载，请先调用 load_csv()")

        if row_index is not None:
            # 获取单行数据
            if row_index < 0 or row_index >= len(self.data):
                raise ValueError(f"行索引 {row_index} 超出范围")
            return self._parse_single_row(self.data[row_index])
        else:
            # 获取所有数据
            all_buildings = []
            for i, row in enumerate(self.data):
                building_data = self._parse_single_row(row)
                if building_data:  # 跳过空数据
                    all_buildings.append(building_data)
            return all_buildings

    def _parse_single_row(self, row: np.ndarray) -> Dict[str, Any]:
        """解析单行CSV数据"""
        try:
            # 转换为字典格式便于处理
            row_dict = {}
            for i, header in enumerate(self.headers):
                if i < len(row):
                    row_dict[header] = row[i]

            # 1. 提取集合信息
            collections = self._extract_collection_data(row_dict)

            # 2. 提取建筑配置
            building_config = self._extract_building_config(row_dict)

            # 3. 提取几何数据
            geometry_data = self._extract_geometry_data(row_dict)

            # 4. 提取标注尺寸
            dimension_data = self._extract_dimension_data(row_dict)

            return {
                "collections": collections,
                "config": building_config,
                "geometry": geometry_data,
                "dimensions": dimension_data,
                "raw_row": row_dict,  # 保留原始数据
            }

        except Exception as e:
            print(f"解析行数据时出错: {e}")
            return None

    def _extract_collection_data(self, row_dict: Dict[str, str]) -> Dict[str, Any]:
        """提取集合信息"""
        collections = {}
        mapping = self.mapping_config["csv_header_mapping"]["collection_levels"]

        # 一级集合
        level_1_config = mapping["level_1"]
        level_1_fields = {}
        for field in level_1_config["fields"]:
            if field in row_dict:
                alias = self.mapping_config["field_aliases"].get(field, field)
                level_1_fields[alias] = self._clean_value(row_dict[field])

        # 生成集合名称
        try:
            collection_1_name = level_1_config["naming_template"].format(**row_dict)
        except KeyError:
            collection_1_name = "_".join([str(v) for v in level_1_fields.values() if v])

        collections["level_1"] = {
            "name": collection_1_name,
            "fields": level_1_fields,
            "description": level_1_config["name"],
        }

        # 二级集合
        level_2_config = mapping["level_2"]
        level_2_fields = {}
        for field in level_2_config["fields"]:
            if field in row_dict:
                alias = self.mapping_config["field_aliases"].get(field, field)
                level_2_fields[alias] = self._clean_value(row_dict[field])

        try:
            collection_2_name = level_2_config["naming_template"].format(**row_dict)
        except KeyError:
            collection_2_name = "_".join([str(v) for v in level_2_fields.values() if v])

        collections["level_2"] = {
            "name": collection_2_name,
            "fields": level_2_fields,
            "description": level_2_config["name"],
        }

        return collections

    def _extract_building_config(self, row_dict: Dict[str, str]) -> Dict[str, Any]:
        """提取建筑配置信息"""
        config_fields = self.mapping_config["csv_header_mapping"]["building_config"][
            "fields"
        ]

        config_data = {}
        for field in config_fields:
            if field in row_dict:
                alias = self.mapping_config["field_aliases"].get(field, field)
                # 楹数需要转换为整数
                if field == "楹":
                    config_data[alias] = int(
                        self._clean_value(row_dict[field], True) or 0
                    )
                else:
                    config_data[alias] = self._clean_value(row_dict[field])

        return config_data

    def _extract_geometry_data(self, row_dict: Dict[str, str]) -> Dict[str, Any]:
        """提取几何数据"""
        geometry_fields = self.mapping_config["csv_header_mapping"]["geometry_data"][
            "fields"
        ]

        geometry_data = {}
        for field in geometry_fields:
            if field in row_dict:
                alias = self.mapping_config["field_aliases"].get(field, field)
                geometry_data[alias] = self._clean_value(row_dict[field], True)

        # 特殊处理：开间数据
        geometry_data["bays"] = self._extract_bay_data(row_dict)

        return geometry_data

    def _extract_bay_data(self, row_dict: Dict[str, str]) -> List[Dict[str, Any]]:
        """提取开间数据"""
        bay_fields = ["明间", "次间", "二次间", "三次间", "四次间"]
        bay_data = []

        for field in bay_fields:
            if field in row_dict:
                value = self._clean_value(row_dict[field], True)
                # 过滤NaN值
                if value is not None and not np.isnan(value):
                    alias = self.mapping_config["field_aliases"].get(field, field)
                    bay_data.append(
                        {
                            "chinese_name": field,
                            "english_name": alias,
                            "width": float(value),
                        }
                    )

        return bay_data

    def _extract_dimension_data(self, row_dict: Dict[str, str]) -> Dict[str, Any]:
        """提取标注尺寸数据"""
        dimension_fields = self.mapping_config["csv_header_mapping"]["dimension_data"][
            "fields"
        ]

        dimension_data = {}
        for field in dimension_fields:
            if field in row_dict:
                alias = self.mapping_config["field_aliases"].get(field, field)
                dimension_data[alias] = self._clean_value(row_dict[field], True)

        return dimension_data


class ConfigLoader:
    def __init__(self, base_dir=path):
        self.base_dir = base_dir
        self.config_path = os.path.join(self.base_dir, "configs/")

    def load_naming_rules(self):
        return self._load_config(self.config_path + "naming_rules.yaml")

    def load_dougong_rules(self):
        return self._load_config(self.config_path + "dougong_rules.json")

    def _load_config(self, filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            if filepath.endswith(".yaml") or filepath.endswith(".yml"):
                return yaml.safe_load(f)
            elif filepath.endswith(".json"):
                return json.load(f)


if __name__ == "__main__":
    # loader = ConfigLoader()
    # naming_rules = loader.load_naming_rules()
    # print(naming_rules.get("object_templates"))

    # 创建加载器
    loader = DataLoader("./test_arch/data/data.csv")
    loader.load_csv()

    # 获取第一个建筑的数据
    building = loader.get_building_data(5)
    print(building)
