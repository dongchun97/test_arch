import tomllib,json
from pathlib import Path
from copy import deepcopy

toml_config_dir = Path("configs/rules/")
json_config_file = Path("configs/rules.json")

class RuleManager:
    def __init__(self):
        self.rules = {}
        self.json_mapping = {}
        self._load_toml()
        self._load_json()

    def _load_toml(self):
        """递归读取 rules 目录下所有 TOML 文件"""
        for path in toml_config_dir.glob("*.toml"):
            with open(path, "rb") as f:
                data = tomllib.load(f)
                self.rules[path.stem] = data

    def _load_json(self):
        with open(json_config_file, "r", encoding="utf-8") as f:
            self.json_mapping=json.load(f)

    def get_rule_class_from_json(self, category: str):
        """获取类别对应规则（如‘房屋’→HouseCalculator）"""
        return self.json_mapping.get(category)

    def get_category_and_key(self, category: str, key: str):
        """按规则文件类别和键名获取定义"""
        return self.rules.get(category, {}).get(category.rstrip("s"), {}).get(key)

    def resolve_ref(self, ref: str):
        """
        将 'roof_types.roll_shed' 形式的引用解析为具体规则。
        """
        category, key = ref.split(".", 1)
        return self.get_category_and_key(category, key)

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

    def get_form_by_construction_name(self, form_name: str) -> dict:
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


if __name__ == "__main__":
    rm = RuleManager()
    # print(rm.rules)

    form_rule = rm.get_form_by_construction_name("四檩卷棚小式")

    with open("test/test_rule_manager_output.json", "w", encoding="utf-8") as f:
        json.dump(form_rule, f, ensure_ascii=False)

    for k, v in form_rule.items():
        print(f"{k}: {v}")

    print(rm.get_rule_class_from_json("房屋"))
