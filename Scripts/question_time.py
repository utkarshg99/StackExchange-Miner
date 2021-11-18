import json, sys, time
from datetime import datetime
import matplotlib.pyplot as plt
from pathlib import Path

DATA_DIRECTORY = "../Data/Extracted"
RES_DIR = f"../Results/{sys.argv[1]}"
fpath = f"{DATA_DIRECTORY}/{sys.argv[1]}/Posts.json"
Path(RES_DIR).mkdir(parents=True, exist_ok=True)

with open(fpath, "r", encoding="utf8") as datajs:
    data_arr = json.load(datajs)["data"]

BUCKETS = {str(i): {
    "n_posts": 0, 
    "t_viewcounts": 0,
    "t_answers": 0,
    "t_comments": 0,
    "t_favs": 0
    } for i in range(0, 24)}

for post in data_arr:
    tme = datetime.strptime(post["CreationDate"][:-4], "%Y-%m-%dT%H:%M:%S")
    BUCKETS[str(tme.hour)]["n_posts"] += 1
    BUCKETS[str(tme.hour)]["t_viewcounts"] += int(post.get("ViewCount", 0))
    BUCKETS[str(tme.hour)]["t_answers"] += int(post.get("AnswerCount", 0))
    BUCKETS[str(tme.hour)]["t_comments"] += int(post.get("CommentCount", 0))
    BUCKETS[str(tme.hour)]["t_favs"] += int(post.get("FavouriteCount", 0))

to_dump = {
    "buckets": BUCKETS
}

with open(f'{RES_DIR}/question_time.json', "w") as qtjs:
    json.dump(to_dump, qtjs, indent="\t")

fig = plt.figure(figsize=(12,6))
hours = [i for i in BUCKETS]
posts = [BUCKETS[i]["n_posts"] for i in BUCKETS]
answers = [BUCKETS[i]["t_answers"] for i in BUCKETS]
comments = [BUCKETS[i]["t_comments"] for i in BUCKETS]
plt.barh(hours, comments, label="Number of Comments")
plt.barh(hours, posts, label="Number of Posts")
plt.barh(hours, answers, label="Number of Answers")
plt.legend()
plt.tight_layout(pad=0)
plt.savefig(f"{RES_DIR}/question-time.png")
plt.show()
plt.clf()