from utils import *

"""
More results:
Link creation chronology
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
    related = {}
    duplicate = {}
    rel_num = 0
    dup_num = 0

    for entry in postlinks:
        if int(entry["PostId"]) not in link_graph:
            link_graph[int(entry["PostId"])] = {"related": [], "duplicate": []}

        date = " ".join(entry["CreationDate"].split(".")[0].split("T"))
        if entry["LinkTypeId"] == "1":
            link_graph[int(entry["PostId"])]["related"].append({"id": int(entry["RelatedPostId"]), "date": date})
            rel_num += 1
            if int(entry["PostId"]) not in related:
                related[int(entry["PostId"])] = 0
            related[int(entry["PostId"])] += 1
        else:
            link_graph[int(entry["PostId"])]["duplicate"].append({"id": int(entry["RelatedPostId"]), "date": date})
            dup_num += 1
            if int(entry["PostId"]) not in duplicate:
                duplicate[int(entry["PostId"])] = 0
            duplicate[int(entry["PostId"])] += 1

    sort_rel = list(sorted(related.items(), key=lambda x: x[1], reverse=True))[:10]
    sort_dup = list(sorted(duplicate.items(), key=lambda x: x[1], reverse=True))[:10]

    results = {}
    results["Number of Posts with Related posts"] = len(related)
    results["Average number of Related posts"] = round(rel_num / len(related), 2)
    results["Number of Posts with Duplicates"] = len(duplicate)
    results["Number of Duplicates"] = dup_num
    results["Top 10 Posts with Most Related Posts"] = sort_rel
    results["Top 10 Posts with Duplicates"] = sort_dup
    results["Number of Related Posts"] = related
    results["Number of Duplicate Posts"] = duplicate

    resultfile = resdir + "/postlinks.results.json"
    with open(resultfile, "w+") as f:
        json.dump(results, f, indent="\t")

    resultfile = resdir + "/postrel.graph.json"
    with open(resultfile, "w+") as f:
        json.dump(link_graph, f, indent="\t")

    vis_graph(link_graph)
    move("static_graph.html", resdir + "/static_graph.html")

    plot_bar_dict({str(k[0]): k[1] for k in sort_rel}).savefig(resdir + "/post.top10rel.png")
    plot_bar_dict({str(k[0]): k[1] for k in sort_dup}).savefig(resdir + "/post.top10dups.png")
