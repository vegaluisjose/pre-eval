import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd


def get_values(data, backend):
    indices = data["backend"] == backend
    return data[indices]


if __name__ == "__main__":
    data = pd.read_csv("compiler_perf_vadd.csv")
    print(get_values(data, "reticle"))
