# # configs/rule_manager.py
# import tomllib
# from pathlib import Path

# class RuleManager:
#     def __init__(self, rule_path: Path):
#         self.rules = tomllib.loads(rule_path.read_text(encoding='utf-8'))
    
#     def find_form(self, purlin_count: int, roof_type: str, grade: str):
#         for name, form in self.rules.items():
#             if isinstance(form, dict) and \
#                form.get('purlin_count') == purlin_count and \
#                form.get('roof_type') == roof_type and \
#                form.get('construction_grade') == grade:
#                 return name, form
#         return None, None

# rule_manager = RuleManager(Path("configs/building_forms.toml"))

# name, form_rule = rule_manager.find_form(
#     purlin_count=5,
#     roof_type="chuan_tang",
#     grade="large_style"
# )

# if form_rule:
#     print(f"Matched rule: {name}")
#     print(form_rule['description'])

# print(rule_manager.rules)

# configs/rule_manager.py

import tomllib
from pathlib import Path
from copy import deepcopy

class RuleManager:
    def __init__(self, rules_dir: Path):
        self.rules_dir = rules_dir
        self.rules = {}
        self.load_rules()

    def load_rules(self):
        """递归读取 rules 目录下所有 TOML 文件"""
        for path in self.rules_dir.glob("*.toml"):
            with open(path, "rb") as f:
                data = tomllib.load(f)
                self.rules[path.stem] = data

    def get(self, category: str, key: str):
        """按规则文件类别和键名获取定义"""
        return self.rules.get(category, {}).get(key) or self.rules.get(category.rstrip('s'), {}).get(key)

    def resolve_ref(self, ref: str):
        """
        将 'roof_types.roll_shed' 形式的引用解析为具体规则。
        """
        category, key = ref.split(".", 1)
        return self.get(category, key)

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

    def get_form(self, form_name: str) -> dict:
        """
        获取综合建筑规则（带继承机制）。
        """
        forms = self.rules.get("building_forms", {}).get("forms", {})
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

rm = RuleManager(Path("configs/rules"))

# form_rule = rm.get_form("四檩卷棚小式")

# for k, v in form_rule.items():
#     print(f"{k}: {v}")

# print(rm.rules.get("roof_types"))
rst=rm.get("roof_types","roof_forms")
# print(rm.rules.get("roof_types"))
print(rst)


