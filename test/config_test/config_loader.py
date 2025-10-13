import json

# # 读取基础配置
with open("./test/config1.json", "r") as f:
    base_config = json.load(f)

# # 读取项目配置
# with open("./test/config2.json", "r") as f:
#     project_config = json.load(f)

# # 合并配置
# merged_config = {**base_config, **project_config["additional"]}

# print(merged_config)
print(base_config)


# import yaml

# # 读取基础配置
# with open("./test/config1.yaml", "r") as f:
#     base_config = yaml.safe_load(f)

# # 读取项目配置
# with open("./test/config2.yaml", "r") as f:
#     project_config = yaml.safe_load(f)

# # 合并配置
# merged_config = {**base_config, **project_config["additional"]}

# print(merged_config)


# -*- coding: utf-8 -*-
# import tomllib, pathlib, pprint


# def load_merge(base_path, project_path):
#     def _load(p):
#         with p.open("rb") as f:
#             return tomllib.load(f)

#     base = _load(base_path)
#     proj = _load(project_path)

#     # 简单的深层合并函数
#     def deep_update(d, u):
#         for k, v in u.items():
#             if isinstance(v, dict) and k in d and isinstance(d[k], dict):
#                 deep_update(d[k], v)
#             else:
#                 d[k] = v
#         return d

#     # 如果有 _base 字段，先读基础文件
#     if "_base" in proj:
#         base_file = project_path.parent / proj.pop("_base")
#         base = load_merge(base_path.parent / base_file, base_file)  # 递归支持链式继承

#     return deep_update(base, proj)


# cfg = load_merge(
#     pathlib.Path("./test/config1.toml"), pathlib.Path("./test/config2.toml")
# )

# pprint.pp(cfg)
