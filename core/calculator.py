import math

def generate_frame_geometry(num_lintels, num_bays, bay_widths, depth_total, eave_step, D, symmetry=True):
    """
    根据建筑基本参数生成平面柱网与梁枋坐标。
    支持左右对称、输出梁枋长度与定位数据。

    参数:
        num_lintels (int): 檩数（进深方向柱列数）
        num_bays (int): 楹数（面阔方向柱列数）
        bay_widths (list[float]): 开间宽度数组（从明间起）
        depth_total (float): 通进深（不含檐步架）
        eave_step (float): 檐步架尺寸
        D (float): 檐柱径
        symmetry (bool): 是否对称展开（默认True）

    返回:
        dict: 包含x_grid, y_grid, pillar_coords, beam_data
    """

    # 1️⃣ 面阔方向坐标
    if symmetry:
        # 假设 bay_widths 中第一个是明间宽度，后续依次是次间宽度
        half_bays = bay_widths[::-1]  # 反转后方便对称
        full_bays = half_bays + bay_widths[1:]
    else:
        full_bays = bay_widths

    x_grid = [0.0]
    for w in full_bays:
        x_grid.append(x_grid[-1] + w)

    # 中心归零对齐
    x_mid = (x_grid[-1] - x_grid[0]) / 2
    x_grid = [x - x_mid for x in x_grid]

    # 2️⃣ 进深方向坐标
    if num_lintels == 6:
        depth_segments = [eave_step, 0.5, D * 3, 0.5, eave_step]
    else:
        inner_depth = depth_total - 2 * eave_step
        seg = inner_depth / (num_lintels - 2)
        depth_segments = [eave_step] + [seg] * (num_lintels - 2) + [eave_step]

    y_grid = [0.0]
    for d in depth_segments:
        y_grid.append(y_grid[-1] + d)

    # 同样中心对齐
    y_mid = (y_grid[-1] - y_grid[0]) / 2
    y_grid = [y - y_mid for y in y_grid]

    # 3️⃣ 柱坐标
    pillar_coords = [(x, y) for x in x_grid for y in y_grid]

    # 4️⃣ 梁、枋长度与坐标线
    # 面阔梁：沿x方向（前后檩之间）
    beam_x = []
    for yi in y_grid:
        for i in range(len(x_grid) - 1):
            beam_x.append({
                "start": (x_grid[i], yi),
                "end": (x_grid[i + 1], yi),
                "length": x_grid[i + 1] - x_grid[i],
                "dir": "x"
            })

    # 进深梁：沿y方向（左右楹之间）
    beam_y = []
    for xi in x_grid:
        for j in range(len(y_grid) - 1):
            beam_y.append({
                "start": (xi, y_grid[j]),
                "end": (xi, y_grid[j + 1]),
                "length": y_grid[j + 1] - y_grid[j],
                "dir": "y"
            })

    return {
        "x_grid": x_grid,
        "y_grid": y_grid,
        "pillar_coords": pillar_coords,
        "beam_data": {
            "x_beams": beam_x,
            "y_beams": beam_y
        }
    }




if __name__=="__main__":
    result = generate_frame_geometry(
        num_lintels=6,
        num_bays=5,
        bay_widths=[1.2, 1.0, 1.0],
        depth_total=2.3,
        eave_step=0.4,
        D=0.1,
        symmetry=True
    )

    print("X坐标:", result["x_grid"])
    print("Y坐标:", result["y_grid"])
    print("柱数:", len(result["pillar_coords"]))
    print("面阔梁数:", len(result["beam_data"]["x_beams"]))
    print("进深梁数:", len(result["beam_data"]["y_beams"]))
