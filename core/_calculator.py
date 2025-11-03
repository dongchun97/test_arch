class BaseCalculator:
    def __init__(self, config):
        self.config = config

    def compute(self, data):
        raise NotImplementedError


class HouseCalculator(BaseCalculator):
    def compute(self, data):
        num_bays = data["dimension_info"]["num_bays"]
        num_lin = data["dimension_info"]["num_lin"]
        scale = self.config["structure"]["num_bays_default"]
        return {
            "type": "房屋",
            "actual_bays": num_bays,
            "actual_lin": num_lin,
            "default_bays": scale,
        }


class PavilionCalculator(BaseCalculator):
    def compute(self, data):
        return {"type": "亭", "message": "亭类计算逻辑尚未实现"}
