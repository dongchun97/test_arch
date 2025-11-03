from pathlib import Path
import tomllib


class ConfigManager:
    def __init__(self, config_dir):
        self.config_dir = Path(config_dir)
        self.config = {}
        self._load_all_configs()

    def _load_all_configs(self):
        for file in self.config_dir.glob("*.toml"):
            name = file.stem
            with open(file, "rb") as f:
                self.config[name] = tomllib.load(f)


if __name__ == "__main__":
    config_manager = ConfigManager("configs")
    print(config_manager.config)
