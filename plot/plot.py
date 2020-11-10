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


def calculate_util(prim, prog):
    file = "{}.csv".format(prog)
    data = pd.read_csv(os.path.join("data", "util", file))
    data = data.sort_values(by=["length"])
    ret = get_values(data, "backend", "reticle")
    ret = get_values(ret, "primitive", "lut")
    length = []
    backend = []
    number = []
    for b in ["base", "baseopt", "reticle"]:
        for n in get_prim_values(data, b, prim):
            backend.append(b)
            number.append(n)
        length += list(ret["length"].to_numpy())
    res = {}
    res["backend"] = backend
    res["length"] = length
    res["number"] = number
    return pd.DataFrame.from_dict(res)


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
    lut = calculate_util("lut", "vadd")
    dsp = calculate_util("dsp", "vadd")
    fig, axes = plt.subplots(1, 4, figsize=(15, 3))
    fig.suptitle("Add")
    # print(lut)
    sns.barplot(
        ax=axes[0], x="length", y="speedup", hue="backend", data=compiler
    )
    sns.barplot(
        ax=axes[1], x="length", y="speedup", hue="backend", data=runtime
    )
    sns.barplot(ax=axes[2], x="length", y="number", hue="backend", data=lut)
    sns.barplot(ax=axes[3], x="length", y="number", hue="backend", data=dsp)
    axes[0].set(xlabel="Length", ylabel="Compiler speedup")
    axes[1].set(xlabel="Length", ylabel="Runtime speedup")
    axes[2].set(xlabel="Length", ylabel="LUTs used")
    axes[3].set(xlabel="Length", ylabel="DSPs used")
    plt.tight_layout()
    plt.savefig("vadd.pdf")
