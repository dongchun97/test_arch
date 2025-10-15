import numpy as np

file = "./data/data-2.csv"

with open(file, "r", encoding="utf-8") as f:
    loadtxt = np.loadtxt(f, delimiter=",", dtype=str, encoding="utf-8")
    # fromtxt = np.fromstring(f.read(), dtype=str, sep=",")
    genfromtxt = np.genfromtxt(f, delimiter=",", encoding="utf-8")

# print(loadtxt[:3], type(loadtxt), loadtxt.dtype)
print(genfromtxt, type(genfromtxt), genfromtxt.dtype)
