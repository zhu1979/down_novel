import os.path


def _set_dir(path):
    if not os.path.exists(path):
        os.mkdir(path)
