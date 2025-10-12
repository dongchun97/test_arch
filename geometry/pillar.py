# geometry/pillar.py
from core.calculator import ArchitectureCalculator

class PillarGeometry:
    def __init__(self):
        self.calculator = ArchitectureCalculator()
    
    def create_pillar(self, pillar_data):
        """根据calculator提供的数据创建柱子"""
        dimensions = self.calculator.get_component_dimensions('pillar', {
            'bay_width': pillar_data['bay_width'],
            'eave_height': pillar_data.get('eave_height')
        })
        
        # 使用bmesh创建几何体
        return self._create_bmesh_cylinder(
            diameter=dimensions['diameter'],
            height=dimensions['height']
        )

# structure/assembler.py
from core.calculator import ArchitectureCalculator

class BuildingAssembler:
    def __init__(self):
        self.calculator = ArchitectureCalculator()
    
    def assemble_building(self, csv_row):
        """组装完整建筑"""
        # 获取完整的3D结构数据
        structure_data = self.calculator.generate_3d_structure(csv_row)
        
        # 创建几何对象
        pillar_objs = self._create_pillars(structure_data['pillars'])
        beam_objs = self._create_beams(structure_data['beams'])
        
        # 组装到集合
        return self._assemble_to_collections(pillar_objs, beam_objs)