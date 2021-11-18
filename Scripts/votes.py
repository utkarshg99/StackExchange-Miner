from utils import *


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
    totals = {k: 0 for k in range(0, 17)}
    deleted = {}
    undeleted = []
    spam = []
    offensive = []
    reopened = []
    accepted = []
    bounty = {}
    closed = {}
    favorite_post = {}
    favorite_user = {}
    for entry in votes:
        postid = int(entry["PostId"])
        voteid = int(entry["VoteTypeId"])
        totals[0] += 1
        totals[voteid] += 1
        if postid not in post_votes:
            post_votes[postid] = {}
        if voteid not in post_votes[postid]:
            post_votes[postid][voteid] = 0
        post_votes[postid][voteid] += 1
        if voteid == 1:
            accepted.append(postid)
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
        if voteid == 9:
            if postid not in bounty:
                bounty[postid] = {"start": 0, "close": 0, "start_amt": 0, "close_amt": 0}
            bounty[postid]["close"] += 1
            if "BountyAmount" in entry.keys():
                bounty[postid]["close_amt"] = int(entry["BountyAmount"])
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
    results["Total Votes"] = totals
    results["Votes by Post"] = post_votes

    voted_sort = list(sorted(post_votes.items(), key=lambda x: sum(x[1].values()), reverse=True))[:10]
    dv_sort = list(sorted(post_votes.items(), key=lambda x: x[1].get(3, 0), reverse=True))[:10]
    uv_sort = list(sorted(post_votes.items(), key=lambda x: x[1].get(2, 0), reverse=True))[:10]
    fav_sort = list(sorted(favorite_post.items(), key=lambda x: x[1], reverse=True))[:10]

    results["Most Voted"] = voted_sort
    results["Most Downvoted"] = dv_sort
    results["Most Upvoted"] = uv_sort
    results["Most Favourited"] = fav_sort

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
