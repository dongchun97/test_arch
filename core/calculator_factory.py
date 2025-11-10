# core/calculator_factory.py
import importlib
from pathlib import Path
from typing import Dict, Any, Type
import tomllib

from configs import ConfigManager
from .calculators import BaseCalculator


class CalculatorFactory:
    """增强的计算器工厂 - 支持专用配置文件"""

    def __init__(self, config_manager: ConfigManager = ConfigManager):
        self.config_manager = config_manager

    def create_calculator(self, building_data: Dict[str, Any]) -> BaseCalculator:
        """创建计算器实例（带专用配置）"""
        # 1. 获取计算器配置
        calculator_config = self._get_calculator_config(building_data)

        # 2. 加载专用配置文件
        dedicated_config = self._load_dedicated_config(calculator_config)

        # 3. 动态导入计算器类
        calculator_class = self._import_calculator_class(
            calculator_config["calculator_class"]
        )

        # 4. 准备完整的建筑配置
        building_config = self._prepare_building_config(building_data, dedicated_config)

        # 5. 创建计算器实例
        return calculator_class(building_config)

    def _get_calculator_config(self, building_data: Dict[str, Any]) -> Dict[str, Any]:
        """获取计算器配置"""
        category = building_data.get("category_info", {}).get(
            "building_category", "房屋"
        )

        # 从注册表获取配置
        calculator_config = self.config_manager.get_class_mapping(category)
        if calculator_config:
            return calculator_config

        # 智能推断配置
        return self._infer_calculator_config(building_data)

    def _load_dedicated_config(
        self, calculator_config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """加载计算器专用配置"""
        config_file = calculator_config.get("config_file")
        if not config_file:
            return {}

        config_path = Path("configs/calculators") / config_file

        try:
            with open(config_path, "rb") as f:
                return tomllib.load(f)
        except FileNotFoundError:
            print(f"警告: 专用配置文件不存在: {config_path}")
            return {}

    def _import_calculator_class(self, class_name: str) -> Type[BaseCalculator]:
        """动态导入计算器类"""
        try:
            module = importlib.import_module(f"core.calculators.{class_name.lower()}")
            return getattr(module, class_name)
        except (ImportError, AttributeError) as e:
            # 回退到默认计算器
            print(f"警告: 无法导入计算器类 {class_name}, 使用默认计算器: {e}")
            from .calculators.house_calculator import HouseCalculator

            return HouseCalculator

    def _prepare_building_config(
        self, building_data: Dict[str, Any], dedicated_config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """准备完整的建筑配置"""
        category_info = building_data.get("category_info", {})
        dimension_info = building_data.get("dimension_info", {})

        # 获取通用样式配置
        form_name = self._infer_building_form(category_info, dimension_info)
        style_config = self.config_manager.get_building_form(form_name)

        # 合并专用配置（专用配置优先级更高）
        merged_style_config = self._merge_configs(style_config, dedicated_config)

        return {
            "building_data": building_data,
            "style_config": merged_style_config,
            "dedicated_config": dedicated_config,
            "form_name": form_name,
        }

    def _merge_configs(self, base_config: Dict, override_config: Dict) -> Dict:
        """深度合并配置（override_config优先级更高）"""
        merged = base_config.copy()

        for key, value in override_config.items():
            if (
                key in merged
                and isinstance(merged[key], dict)
                and isinstance(value, dict)
            ):
                merged[key] = self._merge_configs(merged[key], value)
            else:
                merged[key] = value

        return merged

    def _infer_calculator_config(self, building_data: Dict[str, Any]) -> Dict[str, Any]:
        """智能推断计算器配置"""
        category = building_data.get("category_info", {}).get("building_category", "")
        sub_category = building_data.get("category_info", {}).get("sub_category", "")

        if "亭" in category or "亭" in sub_category:
            return {
                "calculator_class": "PavilionCalculator",
                "config_file": "pavilions/default.toml",
            }
        elif "楼" in category or "阁" in sub_category:
            return {
                "calculator_class": "TowerCalculator",
                "config_file": "towers/default.toml",
            }
        else:
            return {
                "calculator_class": "HouseCalculator",
                "config_file": "houses/default.toml",
            }


if __name__ == "__main__":
    from numpy import array

    data = {
        "basic_info": {
            "garden_name": "CC",
            "garden_id": "W01L_ABC",
            "building_id": "10",
            "building_name": "松篁深处",
        },
        "category_info": {
            "building_category": "房屋",
            "sub_category": "正房",
            "roof_forms": "歇山",
            "ridge_types": "卷棚",
            "construction_grades": "大式",
            "corridor": "无廊",
        },
        "precision_info": {"pricision": ""},
        "dimension_info": {
            "num_bays": 5,
            "bay_widths": array([1.0, 1.0, 1.0]),
            "depth_total": array(1.5),
            "eave_step": array(0.35),
        },
    }

    calc = CalculatorFactory()
    rst = calc.create_calculator(data)
    print(rst)
