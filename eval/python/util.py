import os


def get_curr_dir():
    return os.path.dirname(os.path.abspath(os.path.expanduser(__file__)))


def get_reticle_dir():
    return os.path.abspath(os.path.join(get_curr_dir(), "..", "..", "reticle"))


def change_dir(path):
    os.chdir(path)
