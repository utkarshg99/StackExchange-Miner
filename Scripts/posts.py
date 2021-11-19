from utils import *


def vis_post(adj):
    G = nx.Graph()
    for u in adj:
        G.add_nodes_from([(u, {"color": "green"})])
        for v in adj[u]["ans"]:
            G.add_nodes_from([(v, {"color": "blue"})])
            G.add_edge(u, v)
        if "acc_ans" in adj[u]:
            v = adj[u]["acc_ans"]
            G.add_nodes_from([(v, {"color": "red"})])
            G.add_edge(u, v)
    net = Network("8000px", "8000px")
    net.from_nx(G)
    net.save_graph("static_graph.html")


def vis_user(adj):
    G = nx.Graph()
    for u in adj:
        G.add_nodes_from([(u, {"color": "green"})])
        for v in adj[u]["post"]:
            G.add_nodes_from([(v, {"color": "blue"})])
            G.add_edge(u, v)
        for v in adj[u]["ans"]:
            G.add_nodes_from([(v, {"color": "red"})])
            G.add_edge(u, v)
    net = Network("8000px", "8000px")
    net.from_nx(G)
    net.save_graph("static_graph.html")


def run_posts(stack_name, resdir):
    print("Posts Data Analysis")

    post_data = load_file(stack_name, "Posts.json")

    resdir = resdir + "/Posts"
    if path.exists(resdir):
        rmtree(resdir)
    mkdir(resdir)

    if not post_data:
        print("Data not available")
        return

    posts = {}
    posts_text = {}
    comm_posts = {}
    orphan_ans = {}
    user_posts = {}

    post_graph = {}
    user_graph = {}

    num_closed = 0
    num_ans = 0
    num_posts = 0

    linkify = LinkifyIt()

    for entry in post_data:
        id = int(entry["Id"])
        ptype = int(entry["PostTypeId"])
        if not ptype == 1:
            continue
        num_posts += 1
        if id not in posts:
            posts[id] = {}
            posts_text[id] = {}
            post_graph[id] = {"ans": []}
        if "AcceptedAnswerId" in entry:
            posts[id]["acc_ans"] = int(entry["AcceptedAnswerId"])
            post_graph[id]["acc_ans"] = posts[id]["acc_ans"]
        posts[id]["score"] = int(entry["Score"])
        posts[id]["views"] = int(entry["ViewCount"])
        posts[id]["num_ans"] = int(entry["AnswerCount"])
        posts[id]["num_comm"] = int(entry["CommentCount"])
        posts[id]["num_fav"] = int(entry.get("FavoriteCount", 0))
        posts[id]["created"] = entry["CreationDate"]
        if "ClosedDate" in entry:
            num_closed += 1
            posts[id]["closed"] = entry["ClosedDate"]
        posts[id]["tags"] = entry["Tags"]
        posts[id]["title"] = entry["Title"]
        posts_text[id]["tags"] = entry["Tags"]
        posts_text[id]["title"] = entry["Title"]
        posts_text[id]["body"] = entry["Body"]
        urls = []
        if len(entry["Body"]) > 0:
            if linkify.test(entry["Body"]):
                links = linkify.match(entry["Body"])
                for link in links:
                    urls.append(link.url)
        posts_text[id]["links"] = urls
        posts[id]["answers"] = {}
        posts_text[id]["answers"] = {}
        if "CommunityOwnedDate" in entry:
            comm_posts[id] = entry["CommunityOwnedDate"]
        if "OwnerUserId" in entry:
            userid = int(entry["OwnerUserId"])
            if userid not in user_posts:
                user_posts[userid] = {"num_posts": 0, "num_ans": 0, "posts": [], "ans": []}
                user_graph[userid] = {"post": [], "ans": []}
            user_posts[userid]["num_posts"] += 1
            user_posts[userid]["posts"].append(id)
            user_graph[userid]["post"].append(id)

    for entry in post_data:
        id = int(entry["Id"])
        ptype = int(entry["PostTypeId"])
        if not ptype == 2:
            continue
        num_ans += 1
        postid = int(entry["ParentId"])
        if postid not in posts:
            if postid not in orphan_ans:
                orphan_ans[postid] = []
            orphan_ans[postid].append(id)
        else:
            answer = {}
            answer_text = {}
            answer["create_date"] = entry["CreationDate"]
            answer["score"] = int(entry["Score"])
            answer["num_comm"] = int(entry["CommentCount"])
            answer["created"] = entry["CreationDate"]

            answer_text["body"] = entry["Body"]
            urls = []
            if len(entry["Body"]) > 0:
                if linkify.test(entry["Body"]):
                    links = linkify.match(entry["Body"])
                    for link in links:
                        urls.append(link.url)
            answer_text["links"] = urls

            posts[postid]["answers"][id] = answer
            posts_text[postid]["answers"][id] = answer_text
        if "OwnerUserId" in entry:
            userid = int(entry["OwnerUserId"])
            if userid not in user_posts:
                user_posts[userid] = {"num_posts": 0, "num_ans": 0, "posts": [], "ans": []}
                user_graph[userid] = {"post": [], "ans": []}
            user_posts[userid]["num_ans"] += 1
            user_posts[userid]["ans"].append(id)
            user_graph[userid]["ans"].append(id)
        post_graph[postid]["ans"].append(id)

    results = {}
    results["Total Posts"] = num_posts
    results["Total Answers"] = num_ans
    results["Total Closed"] = num_closed
    results["Total Open"] = num_posts - num_closed
    results["Posts"] = posts

    print("Writing Results...")
    resultfile = resdir + "/posts.json"
    with open(resultfile, "w+") as f:
        json.dump(results, f, indent="\t")

    resultfile = resdir + "/posts.text.json"
    with open(resultfile, "w+") as f:
        json.dump(posts_text, f, indent="\t")

    resultfile = resdir + "/posts.users.json"
    with open(resultfile, "w+") as f:
        json.dump(user_posts, f, indent="\t")

    resultfile = resdir + "/comm.posts.json"
    with open(resultfile, "w+") as f:
        json.dump(comm_posts, f, indent="\t")

    if len(orphan_ans) > 0:
        resultfile = resdir + "/orphan.answers.json"
        with open(resultfile, "w+") as f:
            json.dump(orphan_ans, f, indent="\t")

    posts_srt_ = dict(sorted(posts.items(), key=lambda item: item[1]["views"], reverse=True))
    keys = list(posts_srt_.keys())[:10]
    posts_srt = {str(key): posts[key]["views"] for key in keys}
    plt.figure(figsize=(12, 6))
    plt.bar(posts_srt.keys(), posts_srt.values())
    plt.title("Top 10 Most Viewed Posts")
    plt.tight_layout(pad=0)
    plt.savefig(f"{resdir}/MostViewed.10.png")
    plt.clf()

    posts_srt_ = dict(sorted(posts.items(), key=lambda item: item[1]["num_ans"], reverse=True))
    keys = list(posts_srt_.keys())[:10]
    posts_srt = {str(key): posts[key]["num_ans"] for key in keys}
    plt.figure(figsize=(12, 6))
    plt.bar(posts_srt.keys(), posts_srt.values())
    plt.title("Top 10 Most Answered Posts")
    plt.tight_layout(pad=0)
    plt.savefig(f"{resdir}/MostAnswered.10.png")
    plt.clf()

    posts_srt_ = dict(sorted(posts.items(), key=lambda item: item[1]["num_comm"], reverse=True))
    keys = list(posts_srt_.keys())[:10]
    posts_srt = {str(key): posts[key]["num_comm"] for key in keys}
    plt.figure(figsize=(12, 6))
    plt.bar(posts_srt.keys(), posts_srt.values())
    plt.title("Top 10 Most Commented Posts")
    plt.tight_layout(pad=0)
    plt.savefig(f"{resdir}/MostCommented.10.png")
    plt.clf()

    posts_srt_ = dict(sorted(posts.items(), key=lambda item: item[1]["num_fav"], reverse=True))
    keys = list(posts_srt_.keys())[:10]
    posts_srt = {str(key): posts[key]["num_fav"] for key in keys}
    plt.figure(figsize=(12, 6))
    plt.bar(posts_srt.keys(), posts_srt.values())
    plt.title("Top 10 Most Favorited Posts")
    plt.tight_layout(pad=0)
    plt.savefig(f"{resdir}/MostFavorited.10.png")
    plt.clf()

    posts_srt_ = dict(sorted(posts.items(), key=lambda item: item[1]["score"], reverse=True))
    keys = list(posts_srt_.keys())[:10]
    posts_srt = {str(key): posts[key]["score"] for key in keys}
    plt.figure(figsize=(12, 6))
    plt.bar(posts_srt.keys(), posts_srt.values())
    plt.title("Top 10 Most Scoring Posts")
    plt.tight_layout(pad=0)
    plt.savefig(f"{resdir}/MostScoring.10.png")
    plt.clf()

    posts_srt_ = dict(sorted(user_posts.items(), key=lambda item: item[1]["num_posts"], reverse=True))
    keys = list(posts_srt_.keys())[:10]
    posts_srt = {str(key): user_posts[key]["num_posts"] for key in keys}
    plt.figure(figsize=(12, 6))
    plt.bar(posts_srt.keys(), posts_srt.values())
    plt.title("Top 10 Users with most Posts")
    plt.tight_layout(pad=0)
    plt.savefig(f"{resdir}/UsersPosts.10.png")
    plt.clf()

    posts_srt_ = dict(sorted(user_posts.items(), key=lambda item: item[1]["num_ans"], reverse=True))
    keys = list(posts_srt_.keys())[:10]
    posts_srt = {str(key): user_posts[key]["num_ans"] for key in keys}
    plt.figure(figsize=(12, 6))
    plt.bar(posts_srt.keys(), posts_srt.values())
    plt.title("Top 10 Users with most Answers")
    plt.tight_layout(pad=0)
    plt.savefig(f"{resdir}/UsersAnswers.10.png")
    plt.clf()

    print("Building Graphs")

    vis_post(post_graph)
    move("static_graph.html", resdir + "/post_graph.html")

    vis_user(user_graph)
    move("static_graph.html", resdir + "/user_graph.html")
