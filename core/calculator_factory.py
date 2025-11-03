from calculators import HouseCalculator, PavilionCalculator


class CalculatorFactory:
    @staticmethod
    def create(class_name, config):
        mapping = {
            "HouseCalculator": HouseCalculator,
            "PavilionCalculator": PavilionCalculator,
        }
        if class_name not in mapping:
            raise ValueError(f"未知的计算器类型: {class_name}")
        return mapping[class_name](config)
