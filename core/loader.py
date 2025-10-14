import numpy as np
from typing import Dict, List, Any, Optional

class DataLoader:
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.headers = None
        self.data = None
        self.standardized_headers = None
    
    def load_csv(self) -> np.ndarray:
        """加载CSV文件，跳过空行和注释行"""
        try:
            # 使用genfromtxt加载数据，跳过空行
            raw_data = np.genfromtxt(
                self.filepath,
                delimiter=',',
                dtype=str,
                # skip_header=1,  # 跳过标题行
                filling_values='',  # 空值填充为空字符串
                encoding='utf-8'
            )
            
            # 获取原始列名
            self.headers = raw_data[0, :].tolist()
            self.data = raw_data[1:, :]
            return self.data
            
        except Exception as e:
            print(f"加载CSV文件失败: {e}")
            raise
    
    def get_headers(self) -> List[str]:
        """获取原始列名"""
        return self.headers if self.headers is not None else []
    
    def get_standardized_headers(self) -> List[str]:
        """获取标准化后的列名"""
        return self.standardized_headers if self.standardized_headers is not None else []


class NamingService:
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or self._get_default_config()
        self.column_mapping = self.config.get('column_mapping', {})
    
    def _get_default_config(self) -> Dict[str, Any]:

        # return "configs/naming_standard.toml"

        """提供默认的列名映射配置"""
        return {
            'column_mapping': {
                '园林名称': 'garden_name',
                '园中园编号': 'sub_garden_id', 
                '园中园名称': 'sub_garden_name',
                '建筑编号': 'building_id',
                '建筑名称': 'building_name',
                '建筑形式': 'building_type',
                '出廊': 'corridor_type',
                '楹': 'bay_count',
                '描述1': 'description',
                '明间': 'main_bay_width',
                '次间': 'secondary_bay_width',
                '二次间': 'second_secondary_bay_width',
                '三次间': 'third_secondary_bay_width', 
                '四次间': 'fourth_secondary_bay_width',
                '通进深': 'total_depth',
                '檐步架': 'eave_step',
                '标注檐柱高': 'marked_eave_column_height',
                '标注柱径': 'marked_column_diameter',
                '标注台明高': 'marked_platform_height',
                '标注上出': 'marked_upper_overhang',
                '标注下出': 'marked_lower_overhang'
            },
            'data_type_rules': {
                'garden_name': 'string',
                'sub_garden_id': 'string', 
                'sub_garden_name': 'string',
                'building_id': 'string',
                'building_name': 'string',
                'building_type': 'string',
                'corridor_type': 'string',
                'bay_count': 'float',
                'description': 'string',
                'main_bay_width': 'float',
                'secondary_bay_width': 'float',
                'second_secondary_bay_width': 'float',
                'third_secondary_bay_width': 'float',
                'fourth_secondary_bay_width': 'float',
                'total_depth': 'float',
                'eave_step': 'float',
                'marked_eave_column_height': 'float',
                'marked_column_diameter': 'float',
                'marked_platform_height': 'float',
                'marked_upper_overhang': 'float',
                'marked_lower_overhang': 'float'
            }
        }
    
    def standardize_headers(self, original_headers: List[str]) -> List[str]:
        """标准化列名"""
        standardized = []
        for header in original_headers:
            # 处理空列名（CSV中的空列）
            if not header or header.strip() == '':
                standardized.append(f'unnamed_{len(standardized)}')
                continue
            
            # 应用映射规则
            standardized_header = self.column_mapping.get(header, header)
            standardized.append(standardized_header)
        
        return standardized
    
    def convert_data_types(self, data: np.ndarray, standardized_headers: List[str]) -> np.ndarray:
        """根据配置转换数据类型"""
        if data.size == 0:
            return data
        
        converted_data = []
        dtype_rules = self.config.get('data_type_rules', {})
        
        for i, header in enumerate(standardized_headers):
            column_data = data[:, i] if data.ndim > 1 else data
            
            # 获取数据类型规则
            data_type = dtype_rules.get(header, 'string')
            
            if data_type == 'float':
                # 转换为浮点数，无法转换的设为NaN
                converted_column = np.array([
                    float(x) if x and x.strip() and x != '-' else np.nan 
                    for x in column_data
                ])
            elif data_type == 'int':
                # 转换为整数
                converted_column = np.array([
                    int(float(x)) if x and x.strip() and x != '-' else -1 
                    for x in column_data
                ])
            else:
                # 保持字符串类型，清理数据
                converted_column = np.array([
                    x.strip() if x and x.strip() else '' 
                    for x in column_data
                ])
            
            converted_data.append(converted_column)
        
        # 转置回原始形状
        return np.column_stack(converted_data) if converted_data else data


class StandardizedDataLoader:
    """结合DataLoader和NamingService的标准化数据加载器"""
    
    def __init__(self, filepath: str, naming_service: NamingService):
        self.loader = DataLoader(filepath)
        self.naming_service = naming_service
        self.standardized_data = None
    
    def load_and_standardize(self) -> np.ndarray:
        """加载并标准化数据"""
        # 1. 加载原始数据
        raw_data = self.loader.load_csv()
        original_headers = self.loader.get_headers()
        
        # 2. 标准化列名
        standardized_headers = self.naming_service.standardize_headers(original_headers)
        self.loader.standardized_headers = standardized_headers
        
        # 3. 转换数据类型
        self.standardized_data = self.naming_service.convert_data_types(raw_data, standardized_headers)
        
        return self.standardized_data
    
    def print_formatted_output(self, max_rows: int = 10):
        """格式化输出数据"""
        if self.standardized_data is None:
            print("请先调用 load_and_standardize() 方法加载数据")
            return
        
        headers = self.loader.get_standardized_headers()
        data = self.standardized_data
        
        print("\n" + "="*80)
        print("标准化数据格式输出")
        print("="*80)
        
        # 打印列名
        header_line = " | ".join(f"{header:>20}" for header in headers)
        print(f"{'Index':>6} | {header_line}")
        print("-" * (6 + len(header_line) + 3 * len(headers)))
        
        # 打印数据行
        for i, row in enumerate(data[:max_rows]):
            row_values = []
            for j, value in enumerate(row):
                if isinstance(value, float) and np.isnan(value):
                    display_value = "NaN"
                elif isinstance(value, float):
                    display_value = f"{value:>8.3f}"
                else:
                    display_value = f"{str(value):>20}"[:20]
                row_values.append(display_value)
            
            row_line = " | ".join(row_values)
            print(f"{i:>6} | {row_line}")


# 使用示例
if __name__ == "__main__":
    # 创建命名服务（可以使用默认配置或自定义配置）
    naming_service = NamingService()
    
    # 创建标准化数据加载器
    loader = StandardizedDataLoader('data/data-2.csv', naming_service)
    
    # 加载并标准化数据
    data = loader.load_and_standardize()
    
    # 格式化输出
    loader.print_formatted_output()
    
    # 获取标准化后的列名
    print(f"\n标准化列名: {loader.loader.get_standardized_headers()}")
    
    # 查看数据形状和类型
    print(f"\n数据形状: {data.shape}")
    print(f"数据类型: {data.dtype}")
    # load=DataLoader('data/data-2.csv')
    # data=load.load_csv()
    # print(load.headers)
    # print(data)