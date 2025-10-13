import tomllib, json


with open("./configs/csv_mapping.toml", "rb") as f:
    config = tomllib.load(f)


with open("./configs/csv_mapping.json", "w", encoding="utf-8") as f:
    json.dump(config, f, ensure_ascii=False)


field = config["mapping"]["garden"]["fields"]

*_, c = field

print(c)
