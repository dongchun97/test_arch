import bpy, bmesh
from mathutils import Vector
from core import DataLoader
from utils import generate_frame_geometry

# import os, sys

# sys.path.append(os.path.dirname(os.path.dirname(__file__)))


# result = generate_frame_geometry(
#     num_lintels=6,
#     num_bays=5,
#     bay_widths=[1.2, 1.0, 1.0],
#     depth_total=2.3,
#     eave_step=0.4,
#     D=0.1,
#     symmetry=True,
# )

bm = bmesh.new()
for x, y in result["pillar_coords"]:
    v = bmesh.ops.create_vert(bm, co=Vector((x, y, 0)))

for beam in result["beam_data"]["x_beams"]:
    v1 = Vector((*beam["start"], 0))
    v2 = Vector((*beam["end"], 0))
    bmesh.ops.create_edge(bm, verts=[bm.verts.new(v1), bm.verts.new(v2)])
