import tomllib, json
from pathlib import Path
from copy import deepcopy

TOML_CONFIG_DIR = Path("configs/rules/")
JSON_CONFIG_FILE = Path("configs/class_mapping.json")


class ClassRegistry:
    def __init__(self, json_config_file: Path = JSON_CONFIG_FILE):
        self.json_config_file = json_config_file
        self.mapping = {}
        self._load_json()

    def _load_json(self):
        with open(self.json_config_file, "r", encoding="utf-8") as f:
            self.mapping = json.load(f)

    def get_calculator_class(self, building_category: str) -> str:
        return self.mapping.get(building_category)

    def get_all_categories(self):
        return list(self.mapping.keys())

    def get_class_mapping(
        self, category: str, class_type: str = "calculator_class"
    ) -> str:
        category_config = self.mapping.get(category)
        if isinstance(category_config, dict):
            return category_config.get(class_type)
        return category_config

    def reload_json(self):
        self._load_json()


class RuleManager:
    def __init__(self, toml_config_dir: Path = TOML_CONFIG_DIR):
        self.toml_config_dir = toml_config_dir
        self.rules = {}
        self._load_toml_rules()

    def _load_toml_rules(self):
        """递归读取 rules 目录下所有 TOML 文件"""
        for path in TOML_CONFIG_DIR.glob("*.toml"):
            with open(path, "rb") as f:
                data = tomllib.load(f)
                self.rules[path.stem] = data

    def get_rule(self, category: str, key: str = None):
        """按规则文件类别和键名获取定义"""
        return self.rules.get(category, {}).get(category.rstrip("s"), {}).get(key)

    def resolve_ref(self, ref: str):
        """
        将 'roof_types.roll_shed' 形式的引用解析为具体规则。
        """
        category, key = ref.split(".", 1)
        return self.get_rule(category, key)

    def merge_rules(self, base: dict, override: dict) -> dict:
        """
        深度合并：override 覆盖 base 的同名项。
        """
        merged = deepcopy(base)
        for k, v in override.items():

            if isinstance(v, dict) and k in merged:
                merged[k] = self.merge_rules(merged[k], v)
            else:
                merged[k] = v
        return merged

    def get_building_form(self, form_name: str) -> dict:
        """
        获取综合建筑规则（带继承机制）。
        """
        forms = self.rules.get("building_forms", {}).get("building_form", {})
        form = deepcopy(forms.get(form_name))
        if not form:
            raise ValueError(f"未找到形态定义：{form_name}")

        final_rule = {}

        # 处理继承链
        if "inherit" in form:
            for ref in form.pop("inherit"):

                parent_rule = self.resolve_ref(ref)
                if parent_rule:
                    final_rule = self.merge_rules(final_rule, parent_rule)

        # 最后合并当前形态本身定义（覆盖父级）
        final_rule = self.merge_rules(final_rule, form)
        return final_rule

    def reload(self):
        self._load_toml_rules()


#  统一调用RuleManager和ClassRegistry方法
class ConfigManager:
    def __init__(
        self,
        toml_config_dir: str = TOML_CONFIG_DIR,
        json_config_file: str = JSON_CONFIG_FILE,
    ):

        self.rule_manager = RuleManager(toml_config_dir)
        self.class_registry = ClassRegistry(json_config_file)

    # rules规则管理方法
    # def get_rule(self, category: str, key: str = None):
    #     return self.rule_manager.get_rule(category, key)

    def get_building_form(self, form_name: str) -> dict:
        return self.rule_manager.get_building_form(form_name)

    # def get_resolve_inference(self, ref: str):
    #     return self.rule_manager.resolve_ref(ref)

    # json类映射方法
    def get_calculator_class(self, building_category: str) -> dict:
        return self.class_registry.get_calculator_class(building_category)

    def get_all_categories(self):
        return self.class_registry.get_all_categories()

    def get_class_mapping(
        self, category: str, class_type: str = "calculator_class"
    ) -> str:
        return self.class_registry.get_class_mapping(category, class_type)

    def reload(self):
        self.rule_manager.reload()
        self.class_registry.reload_json()


if __name__ == "__main__":
    # rm = RuleManager()
    # print(rm.rules)

    # form_rule = rm.get_building_form("四檩卷棚小式")

    # for k, v in form_rule.items():
    #     print(f"{k}: {v}")

    # cr=ClassRegistry()
    # print(cr.get_calculator_class("房屋"))
    # print(cr.get_class_mapping("房屋"))

    config_mgr = ConfigManager()
    # print(config_mgr.get_building_form("四檩卷棚小式"))
    print(config_mgr.get_calculator_class("房屋"))
    print(config_mgr.get_class_mapping("房屋"))
