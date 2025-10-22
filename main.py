import sys
import os

# 如果有你自己的模块（如 utils/），把它加入 sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)


from generator import Generator


def main():
    gen = Generator(csv_data)
    gen.run(row)
    print(gen.calc_results.get("pillars_coords"))


if __name__ == "__main__":
    csv_data = "data/data-2.csv"
    row = 2
    main()
