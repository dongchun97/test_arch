import tomllib, json
from pathlib import Path
from copy import deepcopy

TOML_CONFIG_DIR = Path("configs/rules/")
JSON_CONFIG_FILE = Path("configs/class_mapping.json")

class ClassRegistry:
    """
    负责 JSON 类映射加载（全局加载一次）
    """

    _mapping = None
    _json_file = JSON_CONFIG_FILE

    @classmethod
    def _initialize(cls, json_config_file: Path = None):
        if cls._mapping is not None:
            return

        if json_config_file:
            cls._json_file = json_config_file

        with open(cls._json_file, "r", encoding="utf-8") as f:
            cls._mapping = json.load(f)

    @classmethod
    def get_class_mapping(cls, class_type: str) -> str:
        if cls._mapping is None:
            cls._initialize()

        form_config = cls._mapping.get("roof_forms")
        if isinstance(form_config, dict):
            return form_config.get(class_type)

        return cls._mapping.get(class_type)


class RuleManager:
    """
    负责加载所有规则（全局加载一次，缓存到类属性）
    """

    _rules = {}
    _initialized = False
    _toml_dir = TOML_CONFIG_DIR

    @classmethod
    def _initialize(cls, toml_config_dir: Path = None):

        if cls._initialized:
            return

        if toml_config_dir:
            cls._toml_dir = toml_config_dir

        # 加载所有 toml
        for path in cls._toml_dir.glob("*.toml"):
            with open(path, "rb") as f:
                data = tomllib.load(f)
                cls._rules[path.stem] = data

        cls._initialized = True

    # ---------------- API  ----------------

    @classmethod
    def get_rule(cls, category: str, key: str = None):
        cls._initialize()
        return cls._rules.get(category, {}) \
               .get(category.rstrip("s"), {}) \
               .get(key)

    @classmethod
    def resolve_ref(cls, ref: str):
        category, key = ref.split(".", 1)
        return cls.get_rule(category, key)

    @classmethod
    def merge_rules(cls, base: dict, override: dict) -> dict:
        merged = deepcopy(base)
        for k, v in override.items():
            if isinstance(v, dict) and k in merged:
                merged[k] = cls.merge_rules(merged[k], v)
            else:
                merged[k] = v
        return merged

    @classmethod
    def get_building_form(cls, form_name: str) -> dict:
        cls._initialize()

        forms = cls._rules.get("building_forms", {}).get("building_form", {})
        form = deepcopy(forms.get(form_name))
        if not form:
            raise ValueError(f"未找到形态定义：{form_name}")

        final_rule = {}

        if "inherit" in form:
            for ref in form.pop("inherit"):
                parent_rule = cls.resolve_ref(ref)
                if parent_rule:
                    final_rule = cls.merge_rules(final_rule, parent_rule)

        return cls.merge_rules(final_rule, form)


class ConfigManager:

    @staticmethod
    def _initialize(
        toml_config_dir: Path = TOML_CONFIG_DIR,
        json_config_file: Path = JSON_CONFIG_FILE,
    ):
        RuleManager._initialize(toml_config_dir)
        ClassRegistry._initialize(json_config_file)

    # ----- 对外统一调用 API -----

    @staticmethod
    def get_building_form(form_name: str) -> dict:
        return RuleManager.get_building_form(form_name)

    @staticmethod
    def get_class_mapping(roof_form_name: str) -> str:
        return ClassRegistry.get_class_mapping(roof_form_name)



if __name__ == "__main__":

    config_mgr = ConfigManager()
    print(config_mgr.get_building_form("四檩卷棚小式"))
    print(config_mgr.get_class_mapping("歇山"))
