from utils import *


close_reasons = {
    "1": "Duplicate",
    "2": "Off-topic",
    "3": "Subjective",
    "4": "Not a question",
    "7": "Localized",
    "10": "General Reference",
    "20": "Pointless",
    "101": "Duplicate",
    "102": "Off-topic",
    "103": "Unclear",
    "104": "Too broad",
    "105": "Opinion-based",
}

hist_num_to_type = {
    "4": "Edit Title",
    "5": "Edit Body",
    "6": "Edit Tags",
    "7": "Rollback Title",
    "8": "Rollback Body",
    "9": "Rollback Tags",
    "10": "Post Closed",
    "11": "Post Reopened",
    "12": "Post Deleted",
    "13": "Post Undeleted",
    "14": "Post Locked",
    "15": "Post Unlocked",
    "16": "Community Owned",
    "17": "Post Migrated",
    "19": "Post Protected",
    "20": "Post Unprotected",
    "25": "Post Tweeted",
    "35": "Post Migrated to Other SEs",
    "36": "Post Migrated from Other SEs",
    "37": "Post Merge Source",
    "38": "Post Merge Destination",
    "52": "Marked as Highly Active",
    "53": "Unmarked as Highly Active",
}


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
    closed_type = {k: 0 for k in set(close_reasons.values())}

    edit_nums = {"title": [], "body": [], "tags": []}
    roll_nums = {"title": [], "body": [], "tags": []}

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
        histid = int(entry["PostHistoryTypeId"])

        if entry["PostHistoryTypeId"] not in hist_num_to_type:
            continue

        histtype = hist_num_to_type[entry["PostHistoryTypeId"]]

        if histtype not in posthist:
            posthist[histtype] = 0
        posthist[histtype] += 1

        if histid == 4:
            if postid not in edits:
                edits[postid] = {"title": 0, "body": 0, "tags": 0}
            edits[postid]["title"] += 1
            if postid not in edit_nums["title"]:
                edit_nums["title"].append(postid)

        elif histid == 5:
            if postid not in edits:
                edits[postid] = {"title": 0, "body": 0, "tags": 0}
            edits[postid]["body"] += 1
            if postid not in edit_nums["body"]:
                edit_nums["body"].append(postid)

        elif histid == 6:
            if postid not in edits:
                edits[postid] = {"title": 0, "body": 0, "tags": 0}
            edits[postid]["tags"] += 1
            if postid not in edit_nums["tags"]:
                edit_nums["tags"].append(postid)

        elif histid == 7:
            if postid not in rollbacks:
                rollbacks[postid] = {"title": 0, "body": 0, "tags": 0}
            rollbacks[postid]["title"] += 1
            if postid not in roll_nums["title"]:
                roll_nums["title"].append(postid)

        elif histid == 8:
            if postid not in rollbacks:
                rollbacks[postid] = {"title": 0, "body": 0, "tags": 0}
            rollbacks[postid]["body"] += 1
            if postid not in roll_nums["body"]:
                roll_nums["body"].append(postid)

        elif histid == 9:
            if postid not in rollbacks:
                rollbacks[postid] = {"title": 0, "body": 0, "tags": 0}
            rollbacks[postid]["tags"] += 1
            if postid not in roll_nums["tags"]:
                roll_nums["tags"].append(postid)

        elif histid == 10:
            if postid not in closed:
                closed[postid] = {"reason": "", "reopen": 0}
            closed[postid]["reason"] = close_reasons[entry["Comment"]]
            closed_type[close_reasons[entry["Comment"]]] += 1

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

    results = {}

    results["Totals by Event Type"] = posthist
    results["Posts Closed by Reason"] = closed_type
    results["Average Edits per Post"] = {
        "title": round(posthist["Edit Title"] / len(edit_nums["title"]), 2),
        "body": round(posthist["Edit Body"] / len(edit_nums["body"]), 2),
        "tags": round(posthist["Edit Tags"] / len(edit_nums["tags"]), 2),
    }
    results["Average Rollbacks per Post"] = {
        "title": round(posthist["Rollback Title"] / len(roll_nums["title"]), 2),
        "body": round(posthist["Rollback Body"] / len(roll_nums["body"]), 2),
        "tags": round(posthist["Rollback Tags"] / len(roll_nums["tags"]), 2),
    }

    print("Writing Results...")
    resultfile = resdir + "/posthist.results.json"
    with open(resultfile, "w+") as f:
        json.dump(results, f, indent="\t")

    resultfile = resdir + "/tweeted.json"
    with open(resultfile, "w+") as f:
        json.dump(tweeted, f, indent="\t")

    resultfile = resdir + "/migrated.json"
    with open(resultfile, "w+") as f:
        json.dump({"from": mig_from, "to": mig_to}, f, indent="\t")

    resultfile = resdir + "/merged.json"
    with open(resultfile, "w+") as f:
        json.dump({"src": merge_src, "dst": merge_dst}, f, indent="\t")

    resultfile = resdir + "/closed.json"
    with open(resultfile, "w+") as f:
        json.dump(closed, f, indent="\t")

    resultfile = resdir + "/special.json"
    with open(resultfile, "w+") as f:
        json.dump(special, f, indent="\t")

    plot_bar_dict(closed_type).savefig(resdir + "/close.type.png")
    plot_bar_dict(posthist).savefig(resdir + "/event.type.png")
