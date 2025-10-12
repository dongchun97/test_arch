from utils import NamingService


class DataLoader:
    def __init__(self, csv_path: str, config_loader):
        self.csv_path = csv_path
        self.config_loader = config_loader
        self.naming_service = NamingService(config_loader)
        self.mapping_config = self.config_loader.load_config("csv_mapping")

    def _parse_single_row(self, row: np.ndarray) -> Dict[str, Any]:
        """解析单行CSV数据"""
        row_dict = {}
        for i, header in enumerate(self.headers):
            if i < len(row):
                # 使用命名服务获取英文别名
                english_header = self.naming_service.get_field_alias(header)
                row_dict[english_header] = row[i]

        # 特殊处理建筑形式
        if "building_form" in row_dict:
            row_dict["building_form"] = self.naming_service.resolve_building_form(
                row_dict["building_form"]
            )

        # 提取集合信息（使用命名服务生成集合名称）
        collections = {
            "level_1": {
                "name": self.naming_service.generate_collection_name(
                    "level_1", row_dict
                ),
                "fields": {**row_dict},  # 包含所有字段
            },
            "level_2": {
                "name": self.naming_service.generate_collection_name(
                    "level_2", row_dict
                ),
                "fields": {**row_dict},
            },
        }

        return {
            "collections": collections,
            "config": self._extract_building_config(row_dict),
            "geometry": self._extract_geometry_data(row_dict),
            "dimensions": self._extract_dimension_data(row_dict),
        }
