# core/calculators/dataclasses.py
from dataclasses import dataclass, field
from typing import List, Tuple, Optional, Dict, Any

Point3D = Tuple[float, float, float]
Vector3D = Tuple[float, float, float]


@dataclass
class ComponentResult:
    """
    所有构件计算器的最终返回值
    """

    name: str  # 构件唯一名，如 "eave_column_01"
    type: str  # "pillar" | "beam" | "purlin" | "rafter" ...
    vertices: List[Point3D]  # 世界坐标顶点列表
    edges: List[Tuple[int, int]]  # 边
    faces: List[List[int]]  # 面（可选，实体才需要）
    profile: Optional[List[Point3D]] = None  # 截面轮廓（用于扫掠路径的梁、檩等）
    path: Optional[List[Point3D]] = None  # 扫掠路径（梁、檩、飞檐等）
    center_line: Optional[List[Point3D]] = None  # 中心轴线（用于后续对齐）
    metadata: Dict[str, Any] = field(
        default_factory=dict
    )  # 斗栱类型、收分比例、材质标记等
