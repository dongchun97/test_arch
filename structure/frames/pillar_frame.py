"""
structure/systems/pillar_net.py
-------------------------------
柱网系统层：
- 调用 components/timber/pillar.py 中的 PillarNet 类生成柱子对象
- 接受坐标列表或计算器输出数据
- 处理系统层逻辑（命名、集合、分层）
"""

from structure.components.timber.pillar import PillarNet
import bpy


class PillarGridSystem:
    """
    柱网系统
    """

    def __init__(
        self, coords_list, D=0.3, H=3.0, taper_ratio=1.0, name_prefix="Pillar"
    ):
        """
        coords_list: [(x, y, z), ...] 柱子位置列表
        """
        self.coords_list = coords_list
        self.D = D
        self.H = H
        self.taper_ratio = taper_ratio
        self.name_prefix = name_prefix

        self.collection = None
        self.pillar_net = None
        self.objects = []

        self.create_collection()
        self.build_pillar_net()

    def create_collection(self):
        """
        创建一个集合，将柱子统一管理
        """
        coll_name = "PillarGrid"
        if coll_name in bpy.data.collections:
            self.collection = bpy.data.collections[coll_name]
        else:
            self.collection = bpy.data.collections.new(coll_name)
            bpy.context.scene.collection.children.link(self.collection)

    def build_pillar_net(self):
        """
        调用 PillarNet 类生成柱子对象
        """
        self.pillar_net = PillarNet(
            coords_list=self.coords_list,
            D=self.D,
            H=self.H,
            taper_ratio=self.taper_ratio,
            name_prefix=self.name_prefix,
        )

        # 将柱子对象移动到集合
        for obj in self.pillar_net.objects:
            # 从默认集合移除
            bpy.context.collection.objects.unlink(obj)
            self.collection.objects.link(obj)
            self.objects.append(obj)

        print(f"✅ 柱网系统已生成 {len(self.objects)} 根柱子")
