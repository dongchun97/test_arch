from abc import ABC, abstractmethod
from typing import Dict, Any, List
from configs import ConfigManager


class BaseCalculator(ABC):
    """计算器基类 - 定义统一接口"""

    def __init__(self, building_data: Dict, config_manager: ConfigManager):
        self.building_data = building_data
        self.config_manager = config_manager

    def load_configmanager(self, form_name: str):
        """加载某一建筑形态的完整规则"""
        self.config_manager = self.config_manager.get_building_form(form_name)

    def validate_inputs(self):
        """统一输入接口校验"""
        pass

    @abstractmethod
    def compute_basic_grid(self):
        """
        通用柱网基础信息：
        - num_bays
        - bay_widths
        - depth_total
        - eave_step
        """
        info = self.data["dimension_info"]
        return {
            "num_bays": info["num_bays"],
            "bay_widths": info["bay_widths"],
            "depth_total": info["depth_total"],
            "eave_step": info["eave_step"],
        }

    @abstractmethod
    def compute_geometry(self):
        pass

    @abstractmethod
    def compute_structure(self):
        pass
