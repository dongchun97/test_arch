import tomllib
from pathlib import Path

class GeometryConfig:
    def __init__(self, config_path="configs/geometry_ratio.toml"):
        with open(Path(config_path), "rb") as f:
            self.config = tomllib.load(f)

    def get_pillar_diameter(self, style: str):
        """
        根据建筑类型（大式/中式/小式）返回柱径D
        """
        pillar_cfg = self.config["pillar"]
        if style == "大式":
            return pillar_cfg["dashi_diameter"]
        elif style == "小式":
            return pillar_cfg["xiaoshi_diameter"]
        else:
            raise ValueError(f"未知建筑类型: {style}")

    def get_pillar_height(self, D: float):
        """柱高按比例计算"""
        ratio = self.config["pillar"]["height_ratio"]
        return round(D * ratio, 3)
    

if __name__ == "__main__":
    
    
    config = GeometryConfig()
    print(config.get_pillar_diameter("小式"))
    # print(config.get_pillar_height(0.3))
