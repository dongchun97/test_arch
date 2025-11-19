# -----------------------------------------------------------------------------
# file: structure/utils.py
# -----------------------------------------------------------------------------
from typing import Callable
import bpy

# ================================================================
# Mesh 缓存 / 创建
# ================================================================

def get_or_create_mesh(mesh_key: str, create_func: Callable):
    """如果存在同名 mesh 则复用，否则调用 create_func 创建并返回 mesh 对象。
    create_func() 应返回一个 mesh-like 对象（Blender: bpy.data.meshes.new）
    """
    if mesh_key in bpy.data.meshes:
        return bpy.data.meshes[mesh_key]
    
    mesh = create_func()

    if mesh.name != mesh_key:
        mesh.name = mesh_key

    return mesh


# ================================================================
# Collection 操作
# ================================================================
def ensure_collection(name: str):
    
    """
    在 bpy.data.collections 中确保存在一个指定名称的 Collection。
    若不存在则创建。
    """

    if name in bpy.data.collections:
        return bpy.data.collections[name]

    return bpy.data.collections.new(name)

def link_child_collection(parent: bpy.types.Collection, child: bpy.types.Collection):
    """
    确保 child collection 被链接到 parent collection。
    （不会破坏原有链接）
    """
    if child.name not in parent.children:
        parent.children.link(child)


# ================================================================
# 生成三级 + 四级的集合层级
# ================================================================
DEFAULT_SUB_COLLECTIONS = {
    "platform": "台明",
    "main_body": "正身",
    "roof": "屋顶",
}


def ensure_sub_collections(parent_coll: bpy.types.Collection):
    """为建筑实例创建统一的三个子集合：platform / main_body / roof"""
    sub_colls = {}

    for en_name in DEFAULT_SUB_COLLECTIONS.keys():
        sub_name = f"{parent_coll.name}_{en_name}"
        sub_coll = ensure_collection(sub_name)

        link_child_collection(parent_coll, sub_coll)

        sub_colls[en_name] = sub_coll

    return sub_colls


# ================================================================
# 从数据初始化四级集合结构
# ================================================================
def ensure_hierarchy_from_data(info: dict):
    """
    根据 data_loader 输出初始化集合层级：
    1. garden_name
    2. garden_id
    3. building_id_building_name
    4. platform/main_body/roof

    输入 info 示例如下：
    {
        'basic_info': {
            'garden_name': 'CC',
            'garden_id': 'W01L_ABC',
            'building_id': '10',
            'building_name': '松篁深处'
        }
    }
    """

    basic = info.get("basic_info", {})

    garden_name = basic.get("garden_name", "Garden")
    garden_id   = basic.get("garden_id", "GID")
    building_id = basic.get("building_id", "00")
    building_name = basic.get("building_name", "Building")

    # 1 - 顶层园区
    coll_lv1 = ensure_collection(garden_name)

    # 2 - 园区 ID
    lv2_name = f"{garden_name}_{garden_id}"
    coll_lv2 = ensure_collection(lv2_name)
    link_child_collection(coll_lv1, coll_lv2)

    # 3 - 建筑 ID + 名称
    lv3_name = f"{building_id}_{building_name}"
    coll_lv3 = ensure_collection(lv3_name)
    link_child_collection(coll_lv2, coll_lv3)

    # 4 - 默认子集合
    sub_colls = ensure_sub_collections(coll_lv3)

    return {
        "garden": coll_lv1,
        "garden_id": coll_lv2,
        "building": coll_lv3,
        "subs": sub_colls,
    }


if __name__ == "__main__":
    info = {
    'basic_info': {
        'garden_name': 'CC',
        'garden_id': 'W01L_ABC',
        'building_id': '11',
        'building_name': '对清荫'
        }
    }

    hier = ensure_hierarchy_from_data(info)

    print(hier["building"].name)