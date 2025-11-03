import tomllib


class ConfigLoader:
    def load_config(self, filename):
        path = f"configs/{filename}"
        with open(path, "rb") as f:
            return tomllib.load(f)
