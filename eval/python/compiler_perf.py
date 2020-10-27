from util import make_dir, create_path, build_reticle, compile_reticle, compile_baseline, vivado
from vadd import vadd
from time import perf_counter
import pandas as pd


def update(data, backend, length, time):
    if data:
        data["backend"].append(backend)
        data["length"].append(length)
        data["time"].append(time)
    else:
        data["backend"] = [backend]
        data["length"] = [length]
        data["time"] = [time]
    return data


def bench_vadd(name, out_dir, lengths):
    build_reticle()
    make_dir(out_dir)
    backends = ["base", "baseopt", "reticle"]
    data = {}
    for l in lengths:
        bench_name = "{}{}".format(name, l)
        reticle_file = create_path(out_dir, "{}.ret".format(bench_name))
        vadd(bench_name, l, reticle_file)
        for b in backends:
            use_dsp = True if b == "baseopt" else False
            verilog_name = "{}_{}".format(bench_name, b)
            verilog_file = create_path(out_dir, "{}.v".format(verilog_name))
            if b == "reticle":
                start = perf_counter()
                compile_reticle(reticle_file, verilog_file)
                elapsed = perf_counter() - start
            else:
                compile_baseline(reticle_file, verilog_file, use_dsp)
                start = perf_counter()
                vivado("synth.tcl", [out_dir, verilog_name, bench_name])
                elapsed = perf_counter() - start
            data = update(data, b, l, elapsed)
    df = pd.DataFrame.from_dict(data)
    df.to_csv("compiler_perf_vadd.csv", index=False)


if __name__ == "__main__":
    bench_vadd("vadd", "out", [128])
