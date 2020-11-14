import os
import subprocess as sp


def get_curr_dir():
    return os.path.dirname(os.path.abspath(os.path.expanduser(__file__)))


def get_reticle_dir():
    return os.path.abspath(os.path.join(get_curr_dir(), "..", "..", "reticle"))


def get_tcl_dir():
    return os.path.abspath(os.path.join(get_curr_dir(), "..", "tcl"))


def change_dir(path):
    os.chdir(path)


def make_dir(path):
    p = os.path.join(path)
    if not os.path.isdir(p):
        os.makedirs(p)


def create_path(dir, file):
    return os.path.abspath(os.path.join(dir, file))


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


def reticle_bin(name):
    return os.path.abspath(
        os.path.join(get_reticle_dir(), "target", "release", name)
    )


def compile_baseline(inp, out, use_dsp=False):
    cmd = []
    cmd.append(reticle_bin("reticle-translate"))
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
    cmd.append(reticle_bin("reticle-translate"))
    cmd.append("-b")
    cmd.append("reticle")
    cmd.append("-o")
    cmd.append(out)
    cmd.append(inp)
    cp = sp.run(cmd, check=True, stdout=sp.PIPE)
    return cp.stdout.decode("utf-8")


def reticle_to_asm(inp, out):
    cmd = []
    cmd.append(reticle_bin("reticle-translate"))
    cmd.append("-b")
    cmd.append("asm")
    cmd.append("-o")
    cmd.append(out)
    cmd.append(inp)
    cp = sp.run(cmd, check=True, stdout=sp.PIPE)
    return cp.stdout.decode("utf-8")


def reticle_to_asm_placed(inp, out):
    cmd = []
    cmd.append(reticle_bin("reticle-opt"))
    cmd.append("--asm")
    cmd.append("-o")
    cmd.append(out)
    cmd.append(inp)
    cp = sp.run(cmd, check=True, stdout=sp.PIPE)
    return cp.stdout.decode("utf-8")


def reticle_asm_to_verilog(inp, out):
    cmd = []
    cmd.append(reticle_bin("reticle-translate"))
    cmd.append("--asm")
    cmd.append("-o")
    cmd.append(out)
    cmd.append(inp)
    cp = sp.run(cmd, check=True, stdout=sp.PIPE)
    return cp.stdout.decode("utf-8")


def vivado(script, opts):
    synth_tcl = create_path(get_tcl_dir(), script)
    constraints = create_path(get_tcl_dir(), "constraints.xdc")
    cmd = []
    cmd.append("vivado")
    cmd.append("-mode")
    cmd.append("batch")
    cmd.append("-source")
    cmd.append(synth_tcl)
    cmd.append("-tclargs")
    cmd.append(constraints)
    cmd = cmd + opts
    cp = sp.run(cmd, check=True, stdout=sp.PIPE)
    return cp.stdout.decode("utf-8")
