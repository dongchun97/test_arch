# core/calculators/components/pillar.py
from .base_component import BaseComponentCalculator
from .dataclasses import ComponentResult
import math
import numpy as np


class PillarCalculator(BaseComponentCalculator):
    def calculate(self, params: dict) -> ComponentResult:
        """
        必要输入参数（由屋顶/柱网计算器提供）：
            height          : float    # 柱子总高（到檐口或梁底）
            base_diameter   : float
            top_diameter    : float    # 收分后顶部直径
            position        : Point3D  # 柱心世界坐标
            segments        : int = 24 # 圆柱面数
            shoufen_rule    : str = "song"  # 宋式/清式收分曲线
            pillar_type     : str = "eave"|"gold"|"melon"|"tong"
        """
        h = params["height"]
        d0 = params["base_diameter"]
        d1 = params["top_diameter"]
        pos = params["position"]
        seg = params.get("segments", 24)

        # 收分曲线（宋式为抛物线，清式为直线+卷杀）
        if params.get("shoufen_rule") == "song":
            radii = self._song_shoufen_curve(h, d0, d1)
        else:
            radii = np.linspace(d0 / 2, d1 / 2, 20)

        verts, faces = [], []
        for i, r in enumerate(radii):
            z = i / (len(radii) - 1) * h
            for j in range(seg):
                theta = 2 * math.pi * j / seg
                x = r * math.cos(theta)
                y = r * math.sin(theta)
                verts.append((x + pos[0], y + pos[1], z + pos[2]))

        # 生成边和面（圆柱）
        edges, faces = self._cylinder_topology(len(radii), seg)

        return ComponentResult(
            name=f"{params.get('pillar_type','pillar')}_{params.get('id','')}",
            type="pillar",
            vertices=verts,
            edges=edges,
            faces=faces,
            metadata={
                "pillar_type": params.get("pillar_type"),
                "base_diameter": d0,
                "top_diameter": d1,
                "height": h,
            },
        )
