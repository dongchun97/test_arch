import json


class RuleManager:
    def __init__(self, rule_file):
        with open(rule_file, "r", encoding="utf-8") as f:
            self.rules = json.load(f)

    def get_calculator_class(self, building_type):
        return self.rules.get(building_type, {}).get("calculator_class")

    def list_building_types(self):
        return list(self.rules.keys())


if __name__ == "__main__":
    rule_file = "configs/rules.json"
    rule = RuleManager(rule_file)
    result = rule.get_calculator_class("房屋")
    print(result)

    print(rule.list_building_types())
