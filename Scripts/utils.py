import matplotlib.pyplot as plt
import json
from os import path, mkdir


DATA_DIR = "Data/Extracted/"


def plot_bar_dict(d):
    fig, ax = plt.subplots(nrows=1, ncols=1)
    ax.bar(list([v.replace(" ", "\n") for v in d.keys()]), list(d.values()))
    ax.tick_params(axis="x", labelrotation=20, labelsize=6)
    return fig


def load_file(stack, filename):
    print("Loading {} for {}".format(filename, stack))
    json_dir = DATA_DIR + str(stack)

    filepath = json_dir + "/" + filename
    if path.isfile(filepath):
        with open(filepath, "r") as f:
            dump = json.load(f)
            return dump["data"]
    else:
        return []
