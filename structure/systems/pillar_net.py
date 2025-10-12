# generators/foundation_generator.py
class FoundationGenerator:
    """基础生成器 - 柱网"""

    def generate_column_net(self):
        """生成柱网系统"""
        columns = []

        # 遍历开间和进深
        for bay in range(self.bays):
            for depth in range(self.depths):
                # 计算柱位
                position = self.coordinate_system.calculate_column_position(bay, depth)

                # 创建柱子
                column = self._create_column(bay, depth, position)
                columns.append(column)

        return ColumnNet(columns)


# generators/frame_generator.py
class FrameGenerator:
    """梁架生成器"""

    def generate_beam_frame(self, column_net):
        """在柱网上生成梁架"""
        beams = []

        # 根据柱网生成梁
        for column_row in column_net.get_rows():
            beam = self._create_beam_between_columns(column_row)
            beams.append(beam)

        return BeamFrame(beams)
