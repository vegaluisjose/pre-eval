from util import *
from tadd import tadd
from fsm import fsm
from time import perf_counter
import pandas as pd
import sys


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
        if name == "tadd":
            tadd(bench_name, l, reticle_file)
        elif name == "fsm":
            fsm(bench_name, l, reticle_file)
        else:
            sys.exit(1)
        for b in backends:
            print("Running {} backend with length={}".format(b, l))
            file_name = "{}_{}".format(bench_name, b)
            verilog_file = create_path(out_dir, "{}.v".format(file_name))
            if b == "reticle":
                asm_file = create_path(out_dir, "{}.rasm".format(file_name))
                placed_file = create_path(
                    out_dir, "{}_placed.rasm".format(file_name)
                )
                start = perf_counter()
                reticle_to_asm(reticle_file, asm_file)
                prim = "lut" if name == "fsm" else "dsp"
                reticle_place_asm(asm_file, placed_file, prim)
                elapsed = perf_counter() - start
            else:
                use_dsp = True if b == "baseopt" else False
                compile_baseline(reticle_file, verilog_file, use_dsp)
                start = perf_counter()
                vivado("synth_place.tcl", [out_dir, file_name, bench_name])
                elapsed = perf_counter() - start
            data = update(data, b, l, elapsed)
    df = pd.DataFrame.from_dict(data)
    df.to_csv(create_path(out_dir, "{}.csv".format(name)), index=False)


if __name__ == "__main__":
    # bench("tadd", "out", [64, 128, 256, 512])
    bench("fsm", "out", [2])
