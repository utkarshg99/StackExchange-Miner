from utils import *
import networkx as nx
from pyvis.network import Network

"""
More results:
Link creation chronology
Count Duplicates
Most Duplicated questions
"""


def vis_graph(adj):
    G = nx.Graph()
    for u in adj:
        for v in adj[u]["related"]:
            G.add_edge(u, v["id"], color="blue")
        for v in adj[u]["duplicate"]:
            G.add_edge(u, v["id"], color="red")
    net = Network("2000px", "2000px")
    net.from_nx(G)
    net.save_graph("static_graph.html")


def run_postlinks(stack_name, resdir):
    print("PostLinks Data Analysis")

    postlinks = load_file(stack_name, "PostLinks.json")

    resdir = resdir + "/PostLinks"
    if path.exists(resdir):
        rmtree(resdir)
    mkdir(resdir)

    if not postlinks:
        print("Data not available")
        return

    link_graph = {}

    for entry in postlinks:
        if int(entry["PostId"]) not in link_graph:
            link_graph[int(entry["PostId"])] = {"related": [], "duplicate": []}

        date = " ".join(entry["CreationDate"].split(".")[0].split("T"))
        if entry["LinkTypeId"] == "1":
            link_graph[int(entry["PostId"])]["related"].append({"id": int(entry["RelatedPostId"]), "date": date})
        else:
            link_graph[int(entry["PostId"])]["duplicate"].append({"id": int(entry["RelatedPostId"]), "date": date})

    resultfile = resdir + "/post.graph.json"
    with open(resultfile, "w+") as f:
        json.dump(link_graph, f, indent="\t")

    vis_graph(link_graph)
    move("static_graph.html", resdir + "/static_graph.html")
