class BasicPlanCalculator:
    def __init__(self, config_loader):
        self.base_rules = config_loader.load_config("base_rules")
    
    def generate_basic_column_network(self, csv_data):
        """生成基本柱网"""
        # 从CSV数据获取
        columns_count = csv_data['config']['columns_count']  # 楹数
        beam_count = self._detect_beam_count(csv_data['config']['building_form'])  # 檩数
        main_bay = csv_data['geometry']['main_bay']  # 明间
        total_depth = csv_data['geometry']['total_depth']  # 通进深
        
        # 1. 生成开间方向柱位
        bay_columns = self._generate_bay_columns(columns_count, main_bay)
        
        # 2. 生成进深方向柱位
        depth_columns = self._generate_depth_columns(beam_count, total_depth)
        
        # 3. 组合成立体柱网
        return self._combine_3d_network(bay_columns, depth_columns)
    
    def _generate_bay_columns(self, columns_count, main_bay):
        """生成开间方向柱位"""
        # 简单的等分计算，实际应该用开间比例
        total_columns = columns_count + 1  # 柱子数 = 开间数 + 1
        column_positions = []
        
        for i in range(total_columns):
            position_x = i * main_bay  # 简化计算
            column_type = self._get_bay_column_type(i, columns_count)
            column_positions.append({
                'type': column_type,
                'position_x': position_x,
                'is_corner': i == 0 or i == total_columns - 1
            })
        
        return column_positions
    
    def _generate_depth_columns(self, beam_count, total_depth):
        """生成进深方向柱位"""
        beam_system = self.base_rules['basic_plan']['depth_system']['beam_systems'][str(beam_count)]
        column_sequence = beam_system['column_sequence']
        
        step_length = total_depth / (beam_count - 1)  # 步架长度
        column_positions = []
        
        for i, column_type in enumerate(column_sequence):
            position_y = i * step_length
            column_config = self.base_rules['basic_plan']['column_types'][column_type]
            
            column_positions.append({
                'type': column_type,
                'name': column_config['name'],
                'position_y': position_y,
                'is_grounded': column_config['is_grounded'],
                'is_melon_column': column_config['is_melon_column']
            })
        
        return column_positions
    
    def _combine_3d_network(self, bay_columns, depth_columns):
        """组合成立体柱网"""
        all_columns = []
        
        for bay_col in bay_columns:
            for depth_col in depth_columns:
                column_3d = {
                    'name': f"{depth_col['name']}_{bay_col['position_x']}",
                    'type': depth_col['type'],
                    'position': (bay_col['position_x'], depth_col['position_y'], 0),
                    'is_grounded': depth_col['is_grounded'],
                    'is_melon_column': depth_col['is_melon_column'],
                    'is_corner': bay_col['is_corner']
                }
                all_columns.append(column_3d)
        
        return all_columns