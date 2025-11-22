from generator import Generator

def main():
    csv_path = "data/data2.csv"
    generator = Generator(csv_path)

    # 假设CSV中每一行是一个建筑
    for i in range(generator.get_row_count()):
        try:
            result = generator.run(i)
            print(f"成功生成第 {i+1} 个建筑：{result['building_name']}")
        except Exception as e:
            print(f"第 {i+1} 个建筑生成失败：{e}")


if __name__ == "__main__":
    main()
