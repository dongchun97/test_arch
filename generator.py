# 生成建筑的逻辑
def generate_building_from_csv(row):
    # 1. 识别建筑类型
    building_type = identify_building_type(row['建筑形式'], row['描述1'])
    
    # 2. 获取配置
    type_config = loader.load_building_type(building_type)
    roof_config = loader.load_roof_system(row['建筑形式'])
    structural_rules = loader.load_structural_rules('qing_dynasty')
    
    # 3. 计算尺寸（基于面阔比例）
    dimensions = calculate_dimensions(
        row['明间'], row['次间'], row['通进深'],
        type_config, structural_rules
    )
    
    # 4. 生成建筑
    return assembler.assemble(type_config, roof_config, dimensions)