import bpy
import bmesh
from mathutils import Vector
from collections import defaultdict


class BuildingCollectionManager:
    """建筑集合管理器 - 专门用于建筑生成器的内部集合管理"""

    def __init__(self, base_collection_name="BuildingProject"):
        self.base_name = base_collection_name
        self.collection_hierarchy = {}
        self.initialize_collections()

    def initialize_collections(self):
        """初始化建筑项目集合结构"""
        # 创建或获取主集合
        self.main_collection = self._get_or_create_collection(self.base_name)

        # 创建标准建筑层级集合
        self.building_levels = {}
        self._create_standard_structure()

        print(f"建筑集合管理器已初始化: {self.base_name}")

    def _get_or_create_collection(self, name, parent=None):
        """获取或创建集合"""
        if name in bpy.data.collections:
            collection = bpy.data.collections[name]
        else:
            collection = bpy.data.collections.new(name)
            if parent:
                parent.children.link(collection)
            else:
                bpy.context.scene.collection.children.link(collection)

        return collection

    def _create_standard_structure(self):
        """创建标准的建筑层级结构"""
        # 第一级：建筑组件
        self.components_collection = self._get_or_create_collection(
            f"{self.base_name}_Components", self.main_collection
        )

        # 第二级：按建筑元素分类
        self.structure_collection = self._get_or_create_collection(
            "Structure", self.components_collection
        )
        self.facade_collection = self._get_or_create_collection(
            "Facade", self.components_collection
        )
        self.interior_collection = self._get_or_create_collection(
            "Interior", self.components_collection
        )
        self.details_collection = self._get_or_create_collection(
            "Details", self.components_collection
        )

        # 第三级：结构细分
        self.foundation_collection = self._get_or_create_collection(
            "Foundation", self.structure_collection
        )
        self.walls_collection = self._get_or_create_collection(
            "Walls", self.structure_collection
        )
        self.floors_collection = self._get_or_create_collection(
            "Floors", self.structure_collection
        )
        self.roof_collection = self._get_or_create_collection(
            "Roof", self.structure_collection
        )

        # 第三级：立面细分
        self.windows_collection = self._get_or_create_collection(
            "Windows", self.facade_collection
        )
        self.doors_collection = self._get_or_create_collection(
            "Doors", self.facade_collection
        )
        self.balconies_collection = self._get_or_create_collection(
            "Balconies", self.facade_collection
        )
        self.decorations_collection = self._get_or_create_collection(
            "Decorations", self.facade_collection
        )

        # 更新层级记录
        self.collection_hierarchy = {
            "main": self.main_collection,
            "components": self.components_collection,
            "structure": {
                "main": self.structure_collection,
                "foundation": self.foundation_collection,
                "walls": self.walls_collection,
                "floors": self.floors_collection,
                "roof": self.roof_collection,
            },
            "facade": {
                "main": self.facade_collection,
                "windows": self.windows_collection,
                "doors": self.doors_collection,
                "balconies": self.balconies_collection,
                "decorations": self.decorations_collection,
            },
            "interior": self.interior_collection,
            "details": self.details_collection,
        }

    def create_building_level(self, level_name, level_number=None):
        """创建建筑楼层集合"""
        if level_number is not None:
            level_key = f"Level_{level_number:02d}_{level_name}"
        else:
            level_key = f"Level_{level_name}"

        level_collection = self._get_or_create_collection(
            level_key, self.main_collection
        )

        # 为每个楼层创建标准子集合
        level_structure = self._get_or_create_collection("Structure", level_collection)
        level_facade = self._get_or_create_collection("Facade", level_collection)
        level_interior = self._get_or_create_collection("Interior", level_collection)

        self.building_levels[level_key] = {
            "main": level_collection,
            "structure": level_structure,
            "facade": level_facade,
            "interior": level_interior,
        }

        return level_collection

    def add_object_to_collection(self, obj, collection_path, custom_name=None):
        """将对象添加到指定集合路径"""
        target_collection = self._get_collection_by_path(collection_path)

        if target_collection:
            # 从原有集合中移除
            for coll in obj.users_collection:
                coll.objects.unlink(obj)

            # 添加到目标集合
            target_collection.objects.link(obj)

            # 可选：重命名对象
            if custom_name:
                obj.name = custom_name

            return True
        return False

    def _get_collection_by_path(self, path):
        """根据路径获取集合"""
        path_parts = path.split(".")
        current_level = self.collection_hierarchy

        for part in path_parts:
            if part in current_level:
                current_level = current_level[part]
            else:
                print(f"警告: 集合路径 '{path}' 不存在")
                return None

        return (
            current_level if isinstance(current_level, bpy.types.Collection) else None
        )

    def create_building_component(
        self, name, mesh_data, collection_path, location=(0, 0, 0)
    ):
        """创建建筑组件并添加到指定集合"""
        # 创建网格和对象
        mesh = bpy.data.meshes.new(name)
        obj = bpy.data.objects.new(name, mesh)

        # 创建几何体
        bm = bmesh.new()

        # 这里可以根据mesh_data创建具体的几何形状
        # 示例：创建立方体
        if mesh_data.get("type") == "cube":
            size = mesh_data.get("size", (1, 1, 1))
            bmesh.ops.create_cube(bm, size=1)
            bm.transform(
                [
                    [size[0], 0, 0, 0],
                    [0, size[1], 0, 0],
                    [0, 0, size[2], 0],
                    [0, 0, 0, 1],
                ]
            )

        elif mesh_data.get("type") == "plane":
            size = mesh_data.get("size", (1, 1))
            bmesh.ops.create_grid(bm, x_segments=1, y_segments=1, size=1)
            bm.transform(
                [[size[0], 0, 0, 0], [0, size[1], 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
            )

        # 更新网格
        bm.to_mesh(mesh)
        bm.free()

        # 设置位置
        obj.location = location

        # 添加到集合
        if self.add_object_to_collection(obj, collection_path):
            print(f"建筑组件 '{name}' 已创建并添加到 '{collection_path}'")
            return obj
        else:
            print(f"错误: 无法将 '{name}' 添加到 '{collection_path}'")
            bpy.data.meshes.remove(mesh)
            return None

    def organize_existing_objects(self):
        """将场景中现有对象按类型组织到建筑集合中"""
        object_types = {
            "wall": ["wall", "墙体", "墙壁"],
            "window": ["window", "窗户", "窗"],
            "door": ["door", "门", "门户"],
            "floor": ["floor", "地板", "地面"],
            "roof": ["roof", "屋顶", "天花板"],
            "stair": ["stair", "楼梯", "阶梯"],
            "column": ["column", "柱子", "柱"],
        }

        organized_count = 0

        for obj in bpy.data.objects:
            obj_name_lower = obj.name.lower()

            # 根据对象名称判断类型
            for obj_type, keywords in object_types.items():
                if any(keyword in obj_name_lower for keyword in keywords):
                    collection_path = self._get_collection_path_for_type(obj_type)
                    if collection_path and self.add_object_to_collection(
                        obj, collection_path
                    ):
                        organized_count += 1
                        break

        print(f"已组织 {organized_count} 个对象到建筑集合中")
        return organized_count

    def _get_collection_path_for_type(self, obj_type):
        """根据对象类型返回对应的集合路径"""
        type_to_path = {
            "wall": "structure.walls",
            "window": "facade.windows",
            "door": "facade.doors",
            "floor": "structure.floors",
            "roof": "structure.roof",
            "stair": "details",
            "column": "structure.walls",
        }
        return type_to_path.get(obj_type)

    def set_visibility_by_category(self, category, visible):
        """按类别设置集合可见性"""
        categories = {
            "structure": ["structure"],
            "facade": ["facade"],
            "interior": ["interior"],
            "details": ["details"],
            "all": ["structure", "facade", "interior", "details"],
        }

        if category in categories:
            for cat in categories[category]:
                if cat in self.collection_hierarchy:
                    self._set_collection_visibility_recursive(
                        self.collection_hierarchy[cat], visible
                    )

    def _set_collection_visibility_recursive(self, collection_data, visible):
        """递归设置集合可见性"""
        if isinstance(collection_data, bpy.types.Collection):
            collection_data.hide_viewport = not visible
            collection_data.hide_render = not visible
        elif isinstance(collection_data, dict):
            for key, value in collection_data.items():
                self._set_collection_visibility_recursive(value, visible)

    def get_collection_stats(self):
        """获取集合统计信息"""
        stats = {
            "total_collections": 0,
            "total_objects": 0,
            "collections_by_category": {},
            "objects_by_category": {},
        }

        def count_collections(collection_data):
            if isinstance(collection_data, bpy.types.Collection):
                stats["total_collections"] += 1
                stats["total_objects"] += len(collection_data.objects)
                return len(collection_data.objects)
            elif isinstance(collection_data, dict):
                object_count = 0
                for key, value in collection_data.items():
                    object_count += count_collections(value)
                return object_count
            return 0

        for category, collection_data in self.collection_hierarchy.items():
            if category != "main":
                stats["objects_by_category"][category] = count_collections(
                    collection_data
                )

        return stats

    def cleanup_empty_collections(self):
        """清理空集合"""
        empty_collections = []

        def find_empty_collections(collection_data):
            if isinstance(collection_data, bpy.types.Collection):
                if (
                    len(collection_data.objects) == 0
                    and len(collection_data.children) == 0
                ):
                    empty_collections.append(collection_data)
            elif isinstance(collection_data, dict):
                for value in collection_data.values():
                    find_empty_collections(value)

        find_empty_collections(self.collection_hierarchy)

        for coll in empty_collections:
            # 只删除非核心集合
            if coll.name not in [
                self.main_collection.name,
                self.components_collection.name,
            ]:
                bpy.data.collections.remove(coll)
                print(f"已删除空集合: {coll.name}")

        return len(empty_collections)

    def print_hierarchy(self):
        """打印集合层级结构"""
        print(f"\n=== 建筑集合层级结构 ===")

        def print_collection(collection_data, indent=0):
            prefix = "  " * indent

            if isinstance(collection_data, bpy.types.Collection):
                visible = "可见" if not collection_data.hide_viewport else "隐藏"
                obj_count = len(collection_data.objects)
                print(
                    f"{prefix}📁 {collection_data.name} ({obj_count} 对象) [{visible}]"
                )

                for child in collection_data.children:
                    print_collection(child, indent + 1)

            elif isinstance(collection_data, dict):
                for key, value in collection_data.items():
                    if key != "main":
                        print(f"{prefix}📂 {key}")
                    print_collection(value, indent + 1 if key != "main" else indent)

        print_collection(self.collection_hierarchy)


# 使用示例
def demo_building_collection_manager():
    """演示建筑集合管理器的使用"""

    # 创建管理器实例
    building_manager = BuildingCollectionManager("MyBuildingProject")

    # 创建一些建筑楼层
    building_manager.create_building_level("GroundFloor", 0)
    building_manager.create_building_level("FirstFloor", 1)
    building_manager.create_building_level("SecondFloor", 2)
    building_manager.create_building_level("Roof", 3)

    # 创建建筑组件
    wall_data = {"type": "cube", "size": (10, 0.2, 3)}
    building_manager.create_building_component(
        "MainWall_01", wall_data, "structure.walls", location=(0, 0, 0)
    )

    window_data = {"type": "cube", "size": (1.2, 0.1, 1.5)}
    building_manager.create_building_component(
        "Window_01", window_data, "facade.windows", location=(2, 0, 1.2)
    )

    # 打印层级结构
    building_manager.print_hierarchy()

    # 显示统计信息
    stats = building_manager.get_collection_stats()
    print(f"\n集合统计:")
    print(f"总集合数: {stats['total_collections']}")
    print(f"总对象数: {stats['total_objects']}")

    return building_manager


# 在建筑生成器中的典型用法
if __name__ == "__main__":
    # 初始化建筑集合管理器
    building_manager = BuildingCollectionManager("ArchitectureProject")

    # 生成建筑时使用
    # building_manager.create_building_component(...)
    # building_manager.add_object_to_collection(...)

    # 组织现有对象
    # building_manager.organize_existing_objects()

    # 控制可见性
    # building_manager.set_visibility_by_category('structure', True)
    # building_manager.set_visibility_by_category('facade', False)

    # 清理和统计
    # building_manager.cleanup_empty_collections()
    # stats = building_manager.get_collection_stats()


# 应用
# # 初始化
# building_manager = BuildingCollectionManager("MyBuilding")

# # 生成过程中添加组件
# building_manager.create_building_component(
#     "外墙_01",
#     wall_data,
#     "structure.walls",
#     location=position
# )

# # 或者将现有对象添加到集合
# building_manager.add_object_to_collection(existing_obj, "facade.windows")
