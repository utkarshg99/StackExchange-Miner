from utils import *

"""
More results:
Link creation chronology
"""


def run_postlinks(stack_name, resdir):
    print("PostLinks Data Analysis")

    postlinks = load_file(stack_name, "PostLinks.json")

    resdir = resdir + "/PostLinks"
    if not path.exists(resdir):
        mkdir(resdir)

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

    resultfile = resdir + "/post.graph.json"
    with open(resultfile, "w+") as f:
        json.dump(link_graph, f, indent="\t")
