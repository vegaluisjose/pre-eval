from util import *
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


def bench(name, out_dir, lengths):
    build_reticle()
    make_dir(out_dir)
    backends = ["base", "baseopt", "reticle"]
    data = {}
    for l in lengths:
        bench_name = "{}{}".format(name, l)
        reticle_file = create_path(out_dir, "{}.ret".format(bench_name))
        vadd(bench_name, l, reticle_file)
        for b in backends:
            print("Running {} backend with length={}".format(b, l))
            use_dsp = True if b == "baseopt" else False
            file_name = "{}_{}".format(bench_name, b)
            verilog_file = create_path(out_dir, "{}.v".format(file_name))
            reticle_asm_file = create_path(out_dir, "{}.rasm".format(file_name))
            reticle_asm_placed_file = create_path(
                out_dir, "{}_placed.rasm".format(file_name)
            )
            if b == "reticle":
                start = perf_counter()
                reticle_to_asm(reticle_file, reticle_asm_file)
                reticle_place_asm(reticle_asm_file, reticle_asm_placed_file)
                elapsed = perf_counter() - start
            else:
                compile_baseline(reticle_file, verilog_file, use_dsp)
                start = perf_counter()
                vivado("synth_place.tcl", [out_dir, file_name, bench_name])
                elapsed = perf_counter() - start
            data = update(data, b, l, elapsed)
    df = pd.DataFrame.from_dict(data)
    df.to_csv(create_path(out_dir, "{}.csv".format(name)), index=False)


if __name__ == "__main__":
    bench("vadd", "out", [64, 128, 256, 512])
