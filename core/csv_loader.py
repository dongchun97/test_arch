from configs import ConfigManager

# services/csv_loader.py
class CSVLoader:
    def __init__(self, csv_path: str,config_manager:ConfigManager):
        self.csv_path = csv_path
        self.config_manager = config_manager
        # 只关心字段映射
        self.field_config = self.config_manager.get_field_mapping()
    
    def load_and_standardize(self, csv_data):
        """加载并标准化CSV数据"""
        standardized = {}
        for raw_field, value in csv_data.items():
            # 使用field_mapping进行字段名映射
            std_field = self.field_config['field_aliases'].get(raw_field, raw_field)
            standardized[std_field] = value
        
        # 简单值映射（如出廊类型）
        self._map_simple_values(standardized)
        return standardized
    

if __name__ == "__main__":
    # 示例用法
    loader = CSVLoader()
    csv_data = {"building_type": "住宅", "outdoor_type": "出廊"}
    standardized_data = loader.load_and_standardize(csv_data)
    print(standardized_data)