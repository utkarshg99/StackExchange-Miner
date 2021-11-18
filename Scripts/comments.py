from matplotlib.pyplot import plot
from utils import *

# Fix graph formatting
def run_comments(stack_name, resdir):
    print("Comments Data Analysis")

    comments = load_file(stack_name, "Comments.json")

    resdir = resdir + "/Comments"
    if path.exists(resdir):
        rmtree(resdir)
    mkdir(resdir)

    if not comments:
        print("Data not available")
        return

    scores = {}
    post_com = {}
    user_com = {}
    months = {}
    years = {}

    for entry in comments:
        cid = int(entry["Id"])
        postid = int(entry["PostId"])
        score = int(entry["Score"])
        if "UserId" in entry:
            userid = int(entry["UserId"])
        date = entry["CreationDate"][:7]
        if postid not in post_com:
            post_com[postid] = 0
        post_com[postid] += 1
        if userid not in user_com:
            user_com[userid] = 0
        user_com[userid] += 1
        if cid not in scores:
            scores[cid] = score
        if date not in months:
            months[date] = 0
        months[date] += 1
        if date[:4] not in years:
            years[date[:4]] = 0
        years[date[:4]] += 1

    sort_user = list(sorted(user_com.items(), key=lambda x: x[1], reverse=True))[:10]
    sort_post = list(sorted(post_com.items(), key=lambda x: x[1], reverse=True))[:10]
    sort_score = list(sorted(scores.items(), key=lambda x: x[1], reverse=True))[:10]

    results = {}
    results["Users with Most Comments"] = sort_user
    results["Posts with Most Comments"] = sort_post
    results["Highest scored Comments"] = sort_score
    results["Comment Scores"] = scores
    results["Posts"] = post_com
    results["Users"] = user_com
    results["Month Totals"] = months
    results["Year Totals"] = years

    print("Writing Results..")
    resultfile = resdir + "/comments.results.json"
    with open(resultfile, "w+") as f:
        json.dump(results, f, indent="\t")
    plot_sparse(months, angle=90).savefig(resdir + "/comments.month.png")
    plot_bar_dict(years).savefig(resdir + "/comments.year.png")
