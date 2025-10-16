data = {"园林名称": "颐和园", "园中园编号": "A001", "园中园名称": "谐趣园"}


def generate_filename_v2(data):
    """使用 format() 方法"""
    template = "COL_{园林名称}_{园中园编号}_{园中园名称}"
    return template.format(**data)


print(generate_filename_v2(data))
