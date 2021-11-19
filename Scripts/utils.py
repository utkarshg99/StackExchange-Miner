import matplotlib.pyplot as plt
import numpy as np
import json
from os import path, mkdir
from shutil import rmtree, move, copyfile
import matplotlib.pyplot as plt
import re
from linkify_it import LinkifyIt
from wordcloud import WordCloud
import networkx as nx
from pyvis.network import Network

DATA_DIR = "../Data/Extracted/"


def plot_bar_dict(d, angle=20):
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(10, 10), dpi=300)
    ax.bar(list([v.replace(" ", "\n") for v in d.keys()]), list(d.values()))
    ax.tick_params(axis="x", labelrotation=angle, labelsize=6)
    return fig


def plot_sparse(d, angle):
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(10, 10), dpi=300)
    ax.plot(list([v.replace(" ", "\n") for v in d.keys()]), list(d.values()))
    ax.set_xticks(ax.get_xticks()[::4])
    ax.tick_params(axis="x", labelrotation=angle, labelsize=6)
    return fig


def load_file(stack, filename):
    print("Loading {} for {}".format(filename, stack))
    json_dir = DATA_DIR + str(stack)

    filepath = json_dir + "/" + filename
    if path.isfile(filepath):
        with open(filepath, "r", encoding="utf8") as f:
            dump = json.load(f)
            return dump["data"]
    else:
        return []


def make_wordcloud(freq_dict):
    wc = WordCloud(width=640, height=640, prefer_horizontal=1, max_words=100).generate_from_frequencies(freq_dict)
    fig = plt.figure(frameon=False, figsize=(6.4, 6.4))
    plt.axis("off")
    plt.imshow(wc, interpolation="bilinear")
    return fig
