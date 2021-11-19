from matplotlib.pyplot import plot
from utils import *

vote_num_to_type = {
    "0": "Total",
    "1": "Answer Accepted by Originator",
    "2": "Upvote",
    "3": "Downvote",
    "4": "Offensive",
    "5": "Favorite",
    "6": "Close",
    "7": "Reopen",
    "8": "Bounty Start",
    "9": "Bounty Close",
    "10": "Delete",
    "11": "Undelete",
    "12": "Spam",
}


def run_votes(stack_name, resdir):
    print("Votes Data Analysis")

    votes = load_file(stack_name, "Votes.json")

    resdir = resdir + "/Votes"
    if path.exists(resdir):
        rmtree(resdir)
    mkdir(resdir)

    if not votes:
        print("Data not available")
        return

    post_votes = {}
    totals = {vote_num_to_type[k]: 0 for k in vote_num_to_type}

    deleted = {}
    undeleted = []
    spam = []
    offensive = []
    reopened = []
    accepted = []

    bounty = {}
    bounty_closes = 0
    bounty_sum = 0
    closed = {}
    favorite_post = {}
    favorite_user = {}

    fav_sum = 0
    up_sum = 0
    down_sum = 0

    for entry in votes:
        postid = int(entry["PostId"])
        if entry["VoteTypeId"] not in vote_num_to_type:
            continue
        voteid = int(entry["VoteTypeId"])
        votetype = vote_num_to_type[entry["VoteTypeId"]]
        totals["Total"] += 1
        totals[votetype] += 1
        if postid not in post_votes:
            post_votes[postid] = {}
        if votetype not in post_votes[postid]:
            post_votes[postid][votetype] = 0
        post_votes[postid][votetype] += 1
        if voteid == 1:
            accepted.append(postid)
        if voteid == 2:
            up_sum += 1
        if voteid == 3:
            down_sum += 1
        if voteid == 4:
            offensive.append(postid)
        if voteid == 5:
            if postid not in favorite_post:
                favorite_post[postid] = 0
            favorite_post[postid] += 1
            userid = int(entry["UserId"])
            if userid not in favorite_user:
                favorite_user[userid] = {"count": 0, "posts": []}
            favorite_user[userid]["count"] += 1
            favorite_user[userid]["posts"].append(postid)
            fav_sum += 1
        if voteid == 6:
            if postid not in closed:
                closed[postid] = {"close": 0, "reopen": 0}
            closed[postid]["close"] += 1
        if voteid == 7:
            if postid not in closed:
                closed[postid] = {"close": 0, "reopen": 0}
            closed[postid]["reopen"] += 1
            if postid not in reopened:
                reopened.append(postid)
        if voteid == 8:
            if postid not in bounty:
                bounty[postid] = {"start": 0, "close": 0, "start_amt": 0, "close_amt": 0}
            bounty[postid]["start"] += 1
            if "BountyAmount" in entry.keys():
                bounty[postid]["start_amt"] = int(entry["BountyAmount"])
                bounty_sum += int(entry["BountyAmount"])
        if voteid == 9:
            if postid not in bounty:
                bounty[postid] = {"start": 0, "close": 0, "start_amt": 0, "close_amt": 0}
            bounty[postid]["close"] += 1
            bounty_closes += 1
            if "BountyAmount" in entry.keys():
                bounty[postid]["close_amt"] = int(entry["BountyAmount"])
                bounty_sum += int(entry["BountyAmount"])
        if voteid == 10:
            if postid not in deleted:
                deleted[postid] = {"delete": 0, "undelete": 0}
            deleted[postid]["delete"] += 1
        if voteid == 11:
            if postid not in deleted:
                deleted[postid] = {"delete": 0, "undelete": 0}
            deleted[postid]["undelete"] += 1
            if postid not in undeleted:
                undeleted.append(postid)
        if voteid == 12:
            spam.append(postid)

    results = {}

    special_totals = {
        "spam": len(spam),
        "offensive": len(offensive),
        "deleted": len(deleted),
        "undeleted": len(undeleted),
        "closed": len(closed),
        "reopened": len(reopened),
        "favorited": len(favorite_post),
        "accepted": len(accepted),
    }

    results["Total Votes"] = totals
    results["Totals: Special Posts"] = special_totals

    results["Bounties"] = {"opened": len(bounty), "avg": round(bounty_sum / len(bounty), 2), "closed": bounty_closes}

    results["Average Favorites per User"] = round(fav_sum / len(favorite_user), 2)
    results["Average Favorites per Post"] = round(fav_sum / len(favorite_post), 2)
    results["Average Upvote per Post"] = round(up_sum / len(post_votes), 2)
    results["Average Downvote per Post"] = round(down_sum / len(post_votes), 2)

    voted_sort = list(sorted(post_votes.items(), key=lambda x: sum(x[1].values()), reverse=True))[:10]
    dv_sort = list(sorted(post_votes.items(), key=lambda x: x[1].get("Downvote", 0), reverse=True))[:10]
    uv_sort = list(sorted(post_votes.items(), key=lambda x: x[1].get("Upvote", 0), reverse=True))[:10]
    fav_sort = list(sorted(favorite_post.items(), key=lambda x: x[1], reverse=True))[:10]

    results["Most Voted"] = voted_sort
    results["Most Downvoted"] = dv_sort
    results["Most Upvoted"] = uv_sort
    results["Most Favourited"] = fav_sort

    results["Votes by Post"] = post_votes

    print("Writing Results...")
    resultfile = resdir + "/votes.results.json"
    with open(resultfile, "w+") as f:
        json.dump(results, f, indent="\t")

    resultfile = resdir + "/special.posts.json"
    results = {}
    results["Spam"] = spam
    results["Reopened"] = reopened
    results["Offensive"] = offensive
    results["Undeleted"] = undeleted
    results["Accepted"] = accepted
    with open(resultfile, "w+") as f:
        json.dump(results, f, indent="\t")

    resultfile = resdir + "/closed.json"
    with open(resultfile, "w+") as f:
        json.dump(closed, f, indent="\t")

    resultfile = resdir + "/spam.json"
    with open(resultfile, "w+") as f:
        json.dump(spam, f, indent="\t")

    resultfile = resdir + "/bounty.json"
    with open(resultfile, "w+") as f:
        json.dump(bounty, f, indent="\t")

    resultfile = resdir + "/deletion.json"
    with open(resultfile, "w+") as f:
        json.dump(deleted, f, indent="\t")

    resultfile = resdir + "/favorite.json"
    results = {}
    results["By Post"] = favorite_post
    results["By User"] = favorite_user
    with open(resultfile, "w+") as f:
        json.dump(results, f, indent="\t")

    totals.pop("Total")
    plot_bar_dict(totals).savefig(resdir + "/votes.png")
    plot_bar_dict(special_totals).savefig(resdir + "/posts.special.png")
