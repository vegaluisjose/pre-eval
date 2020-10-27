import subprocess as sp
from util import get_tcl_dir, create_path


def synth(opts):
    synth_tcl = create_path(get_tcl_dir(), "synth.tcl")
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
