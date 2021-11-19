from utils import *


def run_posthist(stack_name, resdir):
    print("Post History Data Analysis")

    posthist_data = load_file(stack_name, "PostHistory.json")

    resdir = resdir + "/PostHistory"
    if path.exists(resdir):
        rmtree(resdir)
    mkdir(resdir)

    if not posthist_data:
        print("Data not available")
        return

    posthist = {}
    edits = {}
    rollbacks = {}
    closed = {}
    tweeted = {}

    special = {
        "deleted": [],
        "undeleted": [],
        "locked": [],
        "unlocked": [],
        "comm": [],
        "prot": [],
        "unprot": [],
        "hot": [],
    }

    mig_from = {}
    mig_to = {}

    merge_src = {}
    merge_dst = {}

    for entry in posthist_data:
        postid = int(entry["PostId"])
        if postid not in posthist:
            posthist[postid] = {}
        histid = int(entry["PostHistoryTypeId"])

        if histid == 4:
            if postid not in edits:
                edits[postid] = {"title": 0, "body": 0, "tags": 0}
            edits[postid]["title"] += 1

        elif histid == 5:
            if postid not in edits:
                edits[postid] = {"title": 0, "body": 0, "tags": 0}
            edits[postid]["body"] += 1

        elif histid == 6:
            if postid not in edits:
                edits[postid] = {"title": 0, "body": 0, "tags": 0}
            edits[postid]["tags"] += 1

        elif histid == 7:
            if postid not in rollbacks:
                rollbacks[postid] = {"title": 0, "body": 0, "tags": 0}
            rollbacks[postid]["title"] += 1

        elif histid == 8:
            if postid not in rollbacks:
                rollbacks[postid] = {"title": 0, "body": 0, "tags": 0}
            rollbacks[postid]["body"] += 1

        elif histid == 9:
            if postid not in rollbacks:
                rollbacks[postid] = {"title": 0, "body": 0, "tags": 0}
            rollbacks[postid]["tags"] += 1

        elif histid == 10:
            if postid not in closed:
                closed[postid] = {"reason": 0, "reopen": 0}
            closed[postid]["reason"] = int(entry["Comment"])

        elif histid == 11:
            if postid not in closed:
                closed[postid] = {"reason": 0, "reopen": 0}
            closed[postid]["reopen"] = 1

        elif histid == 12:
            special["deleted"].append(postid)
        elif histid == 13:
            special["undeleted"].append(postid)
        elif histid == 14:
            special["locked"].append(postid)
        elif histid == 15:
            special["unlocked"].append(postid)
        elif histid == 16:
            special["comm"].append(postid)
        elif histid == 19:
            special["prot"].append(postid)
        elif histid == 20:
            special["unprot"].append(postid)
        elif histid == 25:
            if postid not in tweeted:
                tweeted[postid] = entry["Comment"]

        elif histid == 35:
            if postid not in mig_to:
                mig_to[postid] = entry["Comment"][3:]
        elif histid == 36:
            if postid not in mig_from:
                mig_from[postid] = entry["Comment"][5:]
        elif histid == 37:
            if postid not in merge_src:
                merge_src[postid] = entry["Comment"][3:]
        elif histid == 38:
            if postid not in merge_dst:
                merge_dst[postid] = entry["Comment"][5:]
        elif histid == 52:
            special["hot"].append(postid)
        elif histid == 53:
            if postid in special["hot"]:
                special["hot"].remove(postid)

    print("Writing Results...")
    resultfile = resdir + "/posthist.results.json"
    with open(resultfile, "w+") as f:
        json.dump(posthist, f, indent="\t")

    resultfile = resdir + "/tweeted.json"
    with open(resultfile, "w+") as f:
        json.dump(tweeted, f, indent="\t")

    resultfile = resdir + "/migrated.json"
    with open(resultfile, "w+") as f:
        json.dump({"from": mig_from, "to": mig_to}, f, indent="\t")

    resultfile = resdir + "/merged.json"
    with open(resultfile, "w+") as f:
        json.dump({"src": merge_src, "dst": merge_dst}, f, indent="\t")

    resultfile = resdir + "/special.json"
    with open(resultfile, "w+") as f:
        json.dump(special, f, indent="\t")

    resultfile = resdir + "/closed.json"
    with open(resultfile, "w+") as f:
        json.dump(closed, f, indent="\t")

    resultfile = resdir + "/special.json"
    with open(resultfile, "w+") as f:
        json.dump(special, f, indent="\t")
