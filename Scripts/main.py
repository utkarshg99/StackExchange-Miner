from badges import run_badges
from postlinks import run_postlinks
from votes import run_votes
from tags import run_tags
from comments import run_comments
from posts import run_posts
from users import run_users
from posthist import run_posthist
from utils import *

RESULTS_DIR = "../Results/"


def run(stack_name):
    # load_data(stack_name)
    resultdir = RESULTS_DIR + stack_name
    if not path.exists(resultdir):
        mkdir(resultdir)
    run_badges(stack_name, resultdir)
    run_postlinks(stack_name, resultdir)
    run_votes(stack_name, resultdir)
    run_tags(stack_name, resultdir)
    run_comments(stack_name, resultdir)
    run_posts(stack_name, resultdir)
    run_users(stack_name, resultdir)
    run_posthist(stack_name, resultdir)


if __name__ == "__main__":
    run("history.stackexchange.com")
