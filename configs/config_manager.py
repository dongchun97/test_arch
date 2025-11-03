from pathlib import Path
import tomllib


class ConfigManager:
    def __init__(self):
        self.config_dir = Path("configs")
        self.config = {}
        self._load_all_configs()

    def _load_all_configs(self):
        for file in self.config_dir.glob("*.toml"):
            name = file.stem
            with open(file, "rb") as f:
                self.config[name] = tomllib.load(f)

            # 临时测试可删除
            import json
            with open ("configs/data_json.json", "w", encoding="utf-8") as f:
                json.dump(self.config, f)


if __name__ == "__main__":
    config_manager = ConfigManager()
    print(config_manager.config)

    
