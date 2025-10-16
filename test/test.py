from dataclasses import dataclass


@dataclass
class Person:
    name: str
    age: int = 0


# 创建对象
person = Person(name="Alice")

# 输出对象信息
print(person)
