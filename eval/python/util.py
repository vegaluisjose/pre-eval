import os


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
