import subprocess as sp
import os
from util import get_curr_dir, get_reticle_dir, change_dir


def build_reticle():
    curr_dir = get_curr_dir()
    reticle_dir = get_reticle_dir()
    change_dir(reticle_dir)
    cmd = []
    cmd.append("cargo")
    cmd.append("build")
    cmd.append("--release")
    cp = sp.run(cmd, check=True, stdout=sp.PIPE)
    change_dir(curr_dir)
    return cp.stdout.decode("utf-8")


def translate_bin():
    return os.path.abspath(
        os.path.join(
            get_reticle_dir(), "target", "release", "reticle-translate"
        )
    )


def compile_baselinec(inp, out, use_dsp=False):
    cmd = []
    cmd.append(translate_bin())
    cmd.append("-b")
    cmd.append("verilog")
    if use_dsp:
        cmd.append("--use-dsp")
    cmd.append("-o")
    cmd.append(out)
    cmd.append(inp)
    cp = sp.run(cmd, check=True, stdout=sp.PIPE)
    return cp.stdout.decode("utf-8")


def compile_reticle(inp, out):
    cmd = []
    cmd.append(translate_bin())
    cmd.append("-b")
    cmd.append("reticle")
    cmd.append("-o")
    cmd.append(out)
    cmd.append(inp)
    cp = sp.run(cmd, check=True, stdout=sp.PIPE)
    return cp.stdout.decode("utf-8")


if __name__ == "__main__":
    build_reticle()
