from core import DataLoader
from core import FormInferencer
from configs import ConfigManager
from core import CalculatorFactory


class Generator:

    _cfg = ConfigManager()

    def __init__(self, raw_csv_path: str, row: int):
        self.csv_loader = DataLoader(raw_csv_path)
        self.calcfactory = CalculatorFactory()

        self.row = row

    def run(self):
        # Step 1: 数据加载和预处理（infer）
        raw_building_data = self.csv_loader.get_complete_building_data(self.row)
        inferencer = FormInferencer(raw_building_data)
        building_data = inferencer.run()
        # print(building_data)

        # Step 2: 读取规则（infered_data → rules）
        form_name = building_data["category_info"]["form_name"]
        form_rule = self._cfg.get_building_rules(form_name)
        # print(form_name)
        print(form_rule)

        # Step 3: 创建计算器（factory）
        calc = CalculatorFactory.create_calculator(building_data)
        # print(calc.calculate_grid())
        # print(calc.calculate())
        # print(calc.dim)
        # print(calc.main_bay)
        # print(calc.rule)
        print(calc.calculate_all())

        """
        # Step 3: 根据建筑类型，获取计算器配置
        # -----------------------------------------------------------------------------
        # 更换写法,待完善
        # -----------------------------------------------------------------------------
        basic_info, structure_info, description_info, dimension_info, structure_name = data_loader.load(id)
        config = config_manager.get(structure_name)
        calc_result = component_calculator.compute(dimension_info, config)

        pillar_obj = pillar.create(calc_result['eave_diameter'], calc_result['eave_height'])
        beam_obj = beam.create(calc_result['beam_size'], ...)
        roof_obj = roof.create(calc_result['roof_params'])

        assembler.assemble_building(
            components={"pillar": pillar_obj, "beam": beam_obj, "roof": roof_obj},
            coords=calc_result,
            description_info=description_info,
            collection=main_collection
        )
        """

        # Step 2: 获取建筑数据
        # basic_info = building_data["basic_info"]
        # category_info = building_data["category_info"]
        # dimension_info = building_data["dimension_info"]

        # category = category_info["building_category"]

        # Step 3: 根据规则表查询对应配置
        # rule = self.config_mgr.get_class_mapping(category)
        # config = self.config_loader.load_config(rule["config_file"])

        # # Step 4: 创建正确的计算器实例
        # calculator = CalculatorFactory.create(rule["calculator_class"], config)

        # # Step 5: 执行计算
        # result = calculator.compute(building_data)
        # return result


if __name__ == "__main__":
    raw_csv_path = "data/data.csv"
    gen = Generator(raw_csv_path, row=1)
    gen.run()

    # from pathlib import Path
    # from configs.config_mgr import ConfigManager
    # from core.calculator_factory import CalculatorFactory

    # config_mgr = ConfigManager(Path("configs/rules"))
    # factory = CalculatorFactory(config_mgr)

    # calculator = factory.create("house")
    # result = calculator.compute("四檩卷棚小式")

    # print("\n计算结果：")
    # for k, v in result.items():
    #     print(f"{k}: {v}")
