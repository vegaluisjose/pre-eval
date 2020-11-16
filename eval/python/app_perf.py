from util import *
from tadd import tadd
from fsm import fsm
from time import perf_counter
import pandas as pd
import re
from os import path
import sys


def build_util_pattern(start, end):
    return r".*{}\s+\|\s+(\b\d+\b)\s+\|\s+{}.*".format(start, end)


def build_util_pattern_map():
    pat = {}
    for i in range(1, 7):
        pat["lut{}".format(i)] = build_util_pattern("LUT{}".format(i), "CLB")
    pat["dsp"] = build_util_pattern("DSP48E2", "Arithmetic")
    comp = {}
    for k, v in pat.items():
        comp[k] = re.compile(v)
    return comp


def build_runtime_pattern():
    return re.compile(r"Data Path Delay:\s+(\d+\.\d+).*")


def count(data, types):
    num = 0
    for t in types:
        if t in data:
            num += data[t]
    return num


def update_util(data, length, backend, number, primitive):
    if data:
        data["backend"].append(backend)
        data["length"].append(length)
        data["number"].append(number)
        data["primitive"].append(primitive)
    else:
        data["backend"] = [backend]
        data["length"] = [length]
        data["number"] = [number]
        data["primitive"] = [primitive]
    return data


def update_runtime(data, length, backend, time):
    if data:
        data["backend"].append(backend)
        data["length"].append(length)
        data["time"].append(time)
    else:
        data["backend"] = [backend]
        data["length"] = [length]
        data["time"] = [time]
    return data


def parse_util(data, name, dirname, length, backend):
    filename = "{}{}_{}_utilization.txt".format(name, length, backend)
    file = path.join(dirname, filename)
    input = {}
    with open(file, "r") as file:
        for f in file:
            for k, pat in build_util_pattern_map().items():
                m = re.search(pat, f)
                if m is not None:
                    input[k] = int(m.group(1))
    num = {}
    num["lut"] = count(input, ["lut{}".format(i) for i in range(1, 7)])
    num["dsp"] = count(input, ["dsp"])
    for k, v in num.items():
        data = update_util(data, length, backend, v, k)
    return data


def parse_runtime(data, name, dirname, length, backend):
    pat = build_runtime_pattern()
    filename = "{}{}_{}_timing.txt".format(name, length, backend)
    file = path.join(dirname, filename)
    with open(file, "r") as file:
        for f in file:
            m = re.search(pat, f)
            if m is not None:
                runtime = float(m.group(1))
                data = update_runtime(data, length, backend, runtime)
    return data


def bench(name, out_dir, lengths):
    build_reticle()
    make_dir(out_dir)
    backends = ["base", "baseopt", "reticle"]
    runtime = {}
    util = {}
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
                reticle_to_asm(reticle_file, asm_file)
                prim = "lut" if name == "fsm" else "dsp"
                reticle_place_asm(asm_file, placed_file, prim)
                reticle_asm_to_verilog(placed_file, verilog_file)
                vivado("reticle.tcl", [out_dir, file_name, bench_name])
            else:
                use_dsp = True if b == "baseopt" else False
                compile_baseline(reticle_file, verilog_file, use_dsp)
                vivado("baseline.tcl", [out_dir, file_name, bench_name])
            runtime = parse_runtime(runtime, name, out_dir, l, b)
            util = parse_util(util, name, out_dir, l, b)
    runtime_df = pd.DataFrame.from_dict(runtime)
    util_df = pd.DataFrame.from_dict(util)
    runtime_df.to_csv(
        create_path(out_dir, "{}_runtime.csv".format(name)), index=False
    )
    util_df.to_csv(
        create_path(out_dir, "{}_util.csv".format(name)), index=False
    )


if __name__ == "__main__":
    # bench("tadd", "out", [64, 128, 256, 512])
    bench("fsm", "out", [2])
