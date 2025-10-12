class NamingService:
    """命名服务 - 统一管理所有命名规则和转换"""

    def __init__(self, config_loader):
        self.config_loader = config_loader
        self.naming_standard = self.config_loader.load_config("naming_standard")
        self.csv_mapping = self.config_loader.load_config("csv_mapping")

    # 1. 名称解析功能
    def get_english_name(self, chinese_name, category):
        """获取中文名称对应的英文名称"""
        category_map = self.naming_standard.get(category, {})
        for eng, chn in category_map.items():
            if chn == chinese_name:
                return eng
        return chinese_name  # 没找到返回原名称

    def get_chinese_name(self, english_name, category):
        """获取英文名称对应的中文名称"""
        category_map = self.naming_standard.get(category, {})
        return category_map.get(english_name, english_name)

    # 2. 建筑形式解析
    def resolve_building_form(self, form_name):
        """解析建筑形式名称"""
        # 先尝试从屋顶类型解析
        result = self.get_english_name(form_name, "building_forms")
        if result != form_name:
            return result
        return form_name

    # 3. CSV字段别名解析
    def get_field_alias(self, chinese_field_name):
        """获取CSV字段的英文别名"""
        aliases = self.csv_mapping.get("field_aliases", {})
        return aliases.get(chinese_field_name, chinese_field_name)

    # 4. 集合命名功能
    def generate_collection_name(self, level, row_data):
        """生成集合名称"""
        level_config = self.csv_mapping["csv_header_mapping"]["collection_levels"][
            level
        ]
        template = level_config["naming_template"]

        try:
            # 使用模板格式化
            return template.format(**row_data)
        except KeyError:
            # 如果模板失败，使用字段值拼接
            fields = level_config["fields"]
            values = [str(row_data.get(field, "")) for field in fields]
            return "COL_" + "_".join(filter(None, values))

    # 5. 构件命名功能
    def generate_component_name(self, component_type, params):
        """生成构件对象名称"""
        templates = {
            "pillar": "P_{garden}_{building}_{bay_type}_{position}",
            "beam": "B_{garden}_{building}_{beam_type}_{span}",
            "purlin": "PR_{garden}_{building}_{purlin_type}_{index}",
        }

        template = templates.get(component_type, "{component_type}_{id}")
        return template.format(component_type=component_type, **params)

    # 6. 网格命名功能（用于mesh池）
    def generate_mesh_name(self, component_type, dimensions):
        """生成网格名称（用于复用）"""
        mesh_templates = {
            "pillar": "MESH_P_{diameter}x{height}_{style}",
            "beam": "MESH_B_{length}x{width}x{height}_{type}",
            "purlin": "MESH_PR_{diameter}x{length}",
        }

        template = mesh_templates.get(component_type, "MESH_{component_type}")
        return template.format(component_type=component_type, **dimensions)
