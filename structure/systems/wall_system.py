# wall_system.py
from geometry.wall import WallGeometry


class WallBase:
    """下碱、压头、基座等"""

    def __init__(self, params):
        self.params = params

    def compute(self):
        # 计算下碱、基座几何尺寸
        pass


class WallBody:
    """墙体主体"""

    def __init__(self, params):
        self.params = params

    def compute(self):
        # 计算墙厚、开洞位置、封檩高度
        pass


class WallRoofJoint:
    """与屋顶衔接部分（老檐枋、山花、签尖）"""

    def __init__(self, params):
        self.params = params

    def compute(self):
        # 计算老檐枋、山花、签尖
        pass


class Wall(WallBase, WallBody, WallRoofJoint):
    """完整山墙系统"""

    def __init__(self, params):
        WallBase.__init__(self, params)
        WallBody.__init__(self, params)
        WallRoofJoint.__init__(self, params)
        self.geometry = WallGeometry(params)

    def assemble(self):
        base = self.compute_base()
        body = self.compute_body()
        roofjoint = self.compute_roofjoint()
        return self.geometry.build(base, body, roofjoint)


class YingShanWall(Wall):
    """硬山墙"""

    def compute_roofjoint(self):
        # 无挑檐，与屋面平齐
        pass


class XuanShanWall(Wall):
    """悬山墙"""

    def compute_roofjoint(self):
        # 檐椽挑出墙外，计算挑檐长度与签尖
        pass


class XieShanWall(Wall):
    """歇山墙"""

    def compute_roofjoint(self):
        # 前后坡屋面 + 博风板交界，增加脊部构件
        pass
