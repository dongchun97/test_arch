# structure/assembler.py
from structure.systems.pillar_net import PillarNetSystem

# from structure.systems.beam_frame import BeamFrameSystem
# from structure.systems.roof_system import RoofSystem
# from structure.systems.wall_system import WallSystem
# from structure.collection import CollectionManager
# from structure.placement import PlacementManager


class Assembler:
    """
    负责整个建筑构件系统的装配协调。
    - 读取 FrameGeometryCalculator 输出的几何信息
    - 调用各系统（柱网、梁架、屋顶、山墙）生成模型对象
    - 管理集合与层级结构
    """

    def __init__(self, calc_result):
        self.calc_result = calc_result
        # self.collection = CollectionManager()
        # self.placement = PlacementManager()

        # 系统实例
        self.pillar_net = None
        self.beam_frame = None
        self.roof_system = None
        self.wall_system = None

    # -------------------- 系统生成流程 -------------------- #
    def build_pillar_net(self):
        self.pillar_net = PillarNetSystem(self.calc_result["pillars"])
        self.pillar_net.generate()
        self.collection.add("柱网系统", self.pillar_net.objects)

    # def build_beam_frame(self):
    #     self.beam_frame = BeamFrameSystem(self.calc_result["beams"])
    #     self.beam_frame.generate()
    #     self.collection.add("梁架系统", self.beam_frame.objects)

    # def build_roof_system(self):
    #     self.roof_system = RoofSystem(self.calc_result)
    #     self.roof_system.generate()
    #     self.collection.add("屋顶系统", self.roof_system.objects)

    # def build_wall_system(self):
    #     self.wall_system = WallSystem(self.calc_result)
    #     self.wall_system.generate()
    #     self.collection.add("山墙系统", self.wall_system.objects)

    # -------------------- 主控制流程 -------------------- #
    def assemble_all(self):
        # """
        # 执行完整装配流程（按层次生成）
        # """
        # self.build_pillar_net()
        # self.build_beam_frame()
        # self.build_roof_system()
        # self.build_wall_system()

        # # 父子关系与位置
        # self.placement.link(self.pillar_net, self.beam_frame)
        # self.placement.link(self.beam_frame, self.roof_system)
        # self.placement.link(self.pillar_net, self.wall_system)

        # print("✅ 所有系统已装配完成。")
        # return self.collection
        return "test"


if __name__ == "__main__":
    import sys, pathlib

    sys.path.append(str(pathlib.Path(__file__).parent.parent))
    from structure.systems.pillar_net import PillarNetSystem

    assembl = Assembler()
    assembl.build_pillar_net()
