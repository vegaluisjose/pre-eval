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


def compiler_slowdown(prog):
    file = "{}.csv".format(prog)
    data = pd.read_csv(os.path.join("data", "compiler", file))
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


def runtime_speedup(prog):
    file = "{}.csv".format(prog)
    data = pd.read_csv(os.path.join("data", "runtime", file))
    data = data.sort_values(by=["length"])
    ret = get_values(data, "backend", "reticle")
    length = []
    backend = []
    speedup = []
    for b in ["baseopt", "reticle"]:
        old = get_time_values(data, "base")
        new = get_time_values(data, b)
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
    compiler = compiler_slowdown("vadd")
    runtime = runtime_speedup("vadd")
    lut = calculate_util("lut", "vadd")
    dsp = calculate_util("dsp", "vadd")
    fig, axes = plt.subplots(1, 4, figsize=(15, 3))
    compiler_colors = ["#cccccc", "#999999"]
    runtime_colors = ["#999999", "#666666"]
    util_colors = ["#cccccc", "#999999", "#666666"]
    sns.set_palette(sns.color_palette(compiler_colors))
    sns.barplot(
        ax=axes[0], x="length", y="speedup", hue="backend", data=compiler
    )
    sns.set_palette(sns.color_palette(runtime_colors))
    sns.barplot(
        ax=axes[1], x="length", y="speedup", hue="backend", data=runtime
    )
    sns.set_palette(sns.color_palette(util_colors))
    sns.barplot(ax=axes[2], x="length", y="number", hue="backend", data=lut)
    sns.set_palette(sns.color_palette(util_colors))
    sns.barplot(ax=axes[3], x="length", y="number", hue="backend", data=dsp)
    axes[0].set_xlabel("Length")
    axes[1].set_xlabel("Length")
    axes[2].set_xlabel("Length")
    axes[3].set_xlabel("Length")
    axes[0].set_ylabel("Compiler slowdown")
    axes[1].set_ylabel("Runtime speedup")
    axes[2].set_ylabel("LUTs used")
    axes[3].set_ylabel("DSPs used")
    axes[0].get_legend().remove()
    axes[1].get_legend().remove()
    axes[2].get_legend().remove()
    new_labels = ["base", "hint", "reticle"]
    handles, _ = axes[3].get_legend_handles_labels()
    axes[3].legend(
        handles,
        new_labels,
        fontsize="12",
        loc="center left",
        bbox_to_anchor=(1, 0.5),
        title="Lang",
    )
    plt.tight_layout()
    plt.savefig("vadd.pdf")
