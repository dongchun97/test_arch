class MeshPool:
    """网格对象池 - 复用网格数据"""

    def __init__(self):
        self._pool = {}
        self._hit_count = 0
        self._miss_count = 0

    def get_mesh(self, component_type, parameters, context_params=None):
        """
        获取网格 - 集成命名服务

        Args:
            component_type: 构件类型
            parameters: 几何参数（用于mesh命名）
            context_params: 上下文参数（园林、建筑信息，用于对象命名）
        """
        # 生成mesh名称（用于复用）
        mesh_name = NamingService.format_mesh_name(component_type, **parameters)

        # 如果提供了上下文参数，也生成对象名称（用于调试）
        object_name = None
        if context_params:
            object_name = NamingService.format_object_name(
                component_type, **{**parameters, **context_params}
            )

        # 从池中获取或创建网格
        cache_key = self._generate_cache_key(component_type, parameters)

        if cache_key in self._pool:
            mesh = self._pool[cache_key].copy()
            if object_name:
                mesh.name = object_name + "_Mesh"
            else:
                mesh.name = mesh_name
            return mesh
        else:
            # 创建新网格...
            self._miss_count += 1
            new_mesh = self._create_new_mesh(mesh_type, parameters, mesh_name)
            self._pool[cache_key] = new_mesh
            return new_mesh

    def _generate_cache_key(self, mesh_type, parameters):
        """生成缓存键"""
        # 对参数字典进行标准化处理，确保相同的参数生成相同的键
        sorted_params = tuple(sorted(parameters.items()))
        return f"{mesh_type}_{hash(sorted_params)}"

    def _create_new_mesh(self, mesh_type, parameters, mesh_name):
        """创建新的网格数据"""
        if mesh_name is None:
            mesh_name = f"{mesh_type}_mesh_{len(self._pool)}"

        mesh = bpy.data.meshes.new(mesh_name)

        # 这里可以调用具体的几何创建函数
        # 或者由调用者创建几何，这里只管理池

        return mesh

    def clear_unused_meshes(self):
        """清理未被使用的网格"""
        meshes_to_remove = []
        for key, mesh in self._pool.items():
            if mesh.users == 0:  # 没有用户使用这个网格
                meshes_to_remove.append(key)

        for key in meshes_to_remove:
            mesh = self._pool.pop(key)
            bpy.data.meshes.remove(mesh)

    def get_stats(self):
        """获取缓存统计信息"""
        return {
            "total_meshes": len(self._pool),
            "hit_count": self._hit_count,
            "miss_count": self._miss_count,
            "hit_rate": (
                self._hit_count / (self._hit_count + self._miss_count)
                if (self._hit_count + self._miss_count) > 0
                else 0
            ),
        }
