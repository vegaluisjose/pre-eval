import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os


def get_values(data, column, value):
    indices = data[column] == value
    return data[indices]


def get_prim_values(data, backend, prim):
    df = get_values(data, "primitive", prim)
    df = get_values(df, "backend", backend)
    return df["number"].to_numpy()


def get_time_values(data, backend):
    df = get_values(data, "backend", backend)
    return df["time"].to_numpy()


def get_length_values(data):
    df = get_values(data, "primitive", "lut")
    df = get_values(df, "backend", "base")
    return df["length"].to_numpy()


def calculate_util_ratio():
    util = pd.read_csv("data/util/vadd.csv")
    length = get_length_values(util)
    for backend in ["base", "baseopt"]:
        for prim in ["lut", "dsp"]:
            old = get_prim_values(util, backend, prim)
            new = get_prim_values(util, "reticle", prim)
            # ratio = [n / o for (n,o) in zip(new, old)]
            print("old:{} new:{}".format(old, new))


def calculate_speedup(metric, prog):
    file = "{}.csv".format(prog)
    data = pd.read_csv(os.path.join("data", metric, file))
    data = data.sort_values(by=["length"])
    ret = get_values(data, "backend", "reticle")
    length = []
    backend = []
    speedup = []
    for b in ["base", "baseopt"]:
        old = get_time_values(data, b)
        new = get_time_values(data, "reticle")
        for (n, o) in zip(new, old):
            backend.append(b)
            speedup.append(o / n)
        length += list(ret["length"].to_numpy())
    res = {}
    res["backend"] = backend
    res["length"] = length
    res["speedup"] = speedup
    return pd.DataFrame.from_dict(res)


if __name__ == "__main__":
    sns.set_theme(style="whitegrid")
    compiler = calculate_speedup("compiler", "vadd")
    runtime = calculate_speedup("runtime", "vadd")
    fig, axes = plt.subplots(1, 4, figsize=(15, 5))
    fig.suptitle("Add")
    sns.barplot(
        ax=axes[0], x="length", y="speedup", hue="backend", data=compiler
    )
    sns.barplot(
        ax=axes[1], x="length", y="speedup", hue="backend", data=runtime
    )
    axes[0].set(ylabel="compiler speedup")
    axes[1].set(ylabel="runtime speedup")
    plt.tight_layout()
    plt.savefig("plot.pdf")
