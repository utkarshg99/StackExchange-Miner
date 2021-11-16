import json
from badges import run_badges
from postlinks import run_postlinks
from os import path, mkdir
from shutil import rmtree

RESULTS_DIR = "Results/"


def run(stack_name):
    # load_data(stack_name)
    resultdir = RESULTS_DIR + stack_name
    if path.exists(resultdir):
        rmtree(resultdir)
    mkdir(resultdir)
    run_badges(stack_name, resultdir)
    run_postlinks(stack_name, resultdir)


if __name__ == "__main__":
    run("history.stackexchange.com")
