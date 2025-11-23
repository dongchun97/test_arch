from .base_component import BaseComponentCalculator
from .dataclasses import ComponentResult


class BeamCalculator(BaseComponentCalculator):
    def calculate(self, params: dict) -> ComponentResult:
        """
        输入：
            start_pos, end_pos       : Point3D
            section                  : str ("rect" | "moon" | "octagon"...)
            width, height            : float
            camber_ratio             : float  # 月梁起翘比例
        """
        # 1. 生成中心路径（可带月梁起翘曲线）
        path = self._generate_camber_path(
            params["start_pos"], params["end_pos"], params.get("camber_ratio", 0)
        )
        # 2. 生成截面轮廓
        profile = self._make_section_profile(
            params["section"], params["width"], params["height"]
        )
        # 3. 扫掠得到顶点/面（用 numpy 快速计算）
        verts, faces = sweep_profile_along_path(profile, path, close_ends=True)

        return ComponentResult(
            name=params["name"],
            type="beam",
            vertices=verts.tolist(),
            faces=faces,
            profile=profile,
            path=path,
            metadata={...},
        )
