import json
from os import link, path, mkdir
from tqdm import tqdm
from shutil import rmtree
from plot_utils import *
import matplotlib.pyplot as plt

DATA_DIR = "Data/Extracted/"
RESULTS_DIR = "Results/"

DATA = {
    "Badges": [],
    "Comments": [],
    "PostHistory": [],
    "PostLinks": [],
    "Posts": [],
    "Tags": [],
    "Users": [],
    "Votes": [],
}


def load_data(stack_name):
    print("Loading data...")
    json_dir = DATA_DIR + str(stack_name)

    for file in tqdm(DATA):
        filepath = json_dir + "/" + file + ".json"
        if path.isfile(filepath):
            with open(filepath, "r") as f:
                dump = json.load(f)
                # print(len(dump["data"]))
                DATA[file] = dump["data"]


"""
More results:
Link creation chronology
"""


def run_postlinks(resdir):
    print("PostLinks Data Analysis")

    postlinks = DATA["PostLinks"]
    if not postlinks:
        print("Data not available")
        return

    link_graph = {}

    for entry in postlinks:
        if int(entry["PostId"]) not in link_graph:
            link_graph[int(entry["PostId"])] = {"related": [], "duplicate": []}
        if entry["LinkTypeId"] == "1":
            link_graph[int(entry["PostId"])]["related"].append(
                {"id": int(entry["RelatedPostId"]), "date": entry["CreationDate"]}
            )
        else:
            link_graph[int(entry["PostId"])]["duplicate"].append(
                {"id": int(entry["RelatedPostId"]), "date": entry["CreationDate"]}
            )


"""
More results:
Users with more number of badges
Badge award chronology
"""


def run_badges(resdir):
    print("Badge Data Analysis")
    badges = DATA["Badges"]

    resdir = resdir + "/Badges"
    if not path.exists(resdir):
        mkdir(resdir)

    if not badges:
        print("Data not available")
        return

    gold_badges = {}
    silver_badges = {}
    bronze_badges = {}
    user_badges = {}

    for entry in badges:
        level = int(entry["Class"])
        if level == 1:
            if entry["Name"] not in gold_badges:
                gold_badges[entry["Name"]] = 0
            gold_badges[entry["Name"]] += 1
        elif level == 2:
            if entry["Name"] not in silver_badges:
                silver_badges[entry["Name"]] = 0
            silver_badges[entry["Name"]] += 1
        elif level == 3:
            if entry["Name"] not in bronze_badges:
                bronze_badges[entry["Name"]] = 0
            bronze_badges[entry["Name"]] += 1
        if entry["UserId"] not in user_badges:
            user_badges[int(entry["UserId"])] = []
        user_badges[int(entry["UserId"])].append({"name": entry["Name"], "time": entry["Date"][:7]})

    awarded_once = []
    badge_totals = {"gold": 0, "silver": 0, "bronze": 0}
    badges_sort = {}
    for badge in gold_badges:
        badge_totals["gold"] += gold_badges[badge]
        if gold_badges[badge] == 1:
            awarded_once.append(badge)
        badges_sort[badge] = gold_badges[badge]
    for badge in silver_badges:
        badge_totals["silver"] += silver_badges[badge]
        if silver_badges[badge] == 1:
            awarded_once.append(badge)
        badges_sort[badge] = silver_badges[badge]
    for badge in bronze_badges:
        badge_totals["bronze"] += bronze_badges[badge]
        if bronze_badges[badge] == 1:
            awarded_once.append(badge)
        badges_sort[badge] = bronze_badges[badge]

    sorted_badges = dict(sorted(badges_sort.items(), key=lambda x: x[1], reverse=True))
    top_ten = list(sorted_badges.keys())[:10]

    total_stats = {
        "total": len(badges),
        "gold": badge_totals["gold"],
        "silver": badge_totals["silver"],
        "bronze": badge_totals["bronze"],
    }

    results = {}
    results["Total Awarded"] = total_stats
    results["Gold Badges"] = gold_badges
    results["Silver Badges"] = silver_badges
    results["Bronze Badges"] = bronze_badges
    results["Top Ten Badges"] = top_ten
    results["Awarded Once"] = awarded_once

    print("Writing Results...")
    resultfile = resdir + "/badges.results.json"
    with open(resultfile, "w+") as f:
        json.dump(results, f, indent="\t")

    print("Generating Plots...")
    plot_bar_dict(total_stats).savefig(resdir + "/total_stats.png")
    plot_bar_dict(dict(list(sorted(gold_badges.items(), key=lambda x: x[1], reverse=True))[:10])).savefig(
        resdir + "/gold_stats.png"
    )
    plot_bar_dict(dict(list(sorted(silver_badges.items(), key=lambda x: x[1], reverse=True))[:10])).savefig(
        resdir + "/silver_stats.png"
    )
    plot_bar_dict(dict(list(sorted(bronze_badges.items(), key=lambda x: x[1], reverse=True))[:10])).savefig(
        resdir + "/bronze_stats.png"
    )


def run(stack_name):
    load_data(stack_name)
    resultdir = RESULTS_DIR + stack_name
    if path.exists(resultdir):
        rmtree(resultdir)
    mkdir(resultdir)
    run_badges(resultdir)


if __name__ == "__main__":
    run("history.stackexchange.com")
