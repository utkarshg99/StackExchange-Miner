import matplotlib.pyplot as plt


def plot_bar_dict(d):
    fig, ax = plt.subplots(nrows=1, ncols=1)
    ax.bar(list([v.replace(" ", "\n") for v in d.keys()]), list(d.values()))
    ax.tick_params(axis="x", labelrotation=20, labelsize=6)
    return fig
