from utils import *

"""
Bubble visualization
"""


def run_tags(stack_name, resdir):
    print("Tags Data Analysis")

    tags = load_file(stack_name, "Tags.json")

    resdir = resdir + "/Tags"
    if path.exists(resdir):
        rmtree(resdir)
    mkdir(resdir)

    if not tags:
        print("Data not available")
        return

    wikis = {}
    excerpts = {}
    counts = {}
    tag_names = []

    for entry in tags:
        tag = entry["TagName"]
        tag_names.append(tag)
        counts[tag] = int(entry["Count"])
        if "ExcerptPostId" in entry:
            excerpts[tag] = int(entry["ExcerptPostId"])
        if "WikiPostId" in entry:
            wikis[tag] = int(entry["WikiPostId"])

    sort_count = list(sorted(counts.items(), key=lambda x: x[1], reverse=True))[:10]

    results = {}
    results["Total Tags"] = len(tag_names)
    results["Top Ten Tags"] = sort_count
    results["Tags"] = tag_names
    results["Count"] = counts
    results["Wiki Posts"] = wikis
    results["Excerpt Posts"] = excerpts

    print("Writing Results...")
    resultfile = resdir + "/tags.results.json"
    with open(resultfile, "w+") as f:
        json.dump(results, f, indent="\t")

    with open(resdir + "/counts.csv", "w+") as f:
        f.write("id,value\n")
        for (k, v) in counts.items():
            f.write(",".join([str(k), str(v)]) + "\n")

    plot_bar_dict(dict(sort_count)).savefig(resdir + "/tags.10.png")
