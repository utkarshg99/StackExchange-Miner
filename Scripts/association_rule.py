import json, sys, re
from pathlib import Path
from sklearn.preprocessing import OneHotEncoder
import numpy as np
import pandas as pd

from rpy2.robjects import pandas2ri
pandas2ri.activate()

import rpy2.robjects as ro
from rpy2.robjects.packages import importr

arules = importr("arules")


DATA_DIRECTORY = "../Data/Extracted"
RES_DIR = f"../Results/{sys.argv[1]}"
WORDS = 100
N_TOP = 10
Path(RES_DIR).mkdir(parents=True, exist_ok=True)

def tagsAsOE():
    fpath = f"{DATA_DIRECTORY}/{sys.argv[1]}/Posts.json"
    fpath2 = f"{RES_DIR}/Tags/tags.results.json"
    with open(fpath, "r", encoding="utf8") as datajs:
        data_arr = json.load(datajs)["data"]
    with open(fpath2, "r", encoding="utf8") as datajs:
        tags = json.load(datajs)["Tags"]
        tags = [[i] for i in tags]
    one_enc = OneHotEncoder(sparse= False)
    one_enc.fit(tags)
    tags_ = []
    tags_o = []
    for post in data_arr:
        ptags = re.findall('<(.*?)>', post.get("Tags", ""))
        tags_.append(ptags)
        # if len(ptags) == 0:
        #     continue
        inp__ = [[ptag] for ptag in ptags]
        trans = one_enc.transform(inp__).sum(axis= 0) if len(ptags) != 0 else np.zeros(len(tags))
        tags_o.append(trans)
    tags_o = np.array(tags_o, dtype=bool)
    return tags_o, [tag[0] for tag in tags]

def badgesAsOE():
    fpath = f"{DATA_DIRECTORY}/{sys.argv[1]}/Badges.json"
    fpath2 = f"{RES_DIR}/Badges/badges.results.json"
    with open(fpath, "r", encoding="utf8") as datajs:
        data_arr = json.load(datajs)["data"]
    with open(fpath2, "r", encoding="utf8") as datajs:
        badges = json.load(datajs)
        badges = {**badges["Gold Badges"], **badges["Silver Badges"], **badges["Bronze Badges"]}
        badges = [[i] for i in badges if i != i.lower()]
    one_enc = OneHotEncoder(sparse= False)
    one_enc.fit(badges)
    badges_o = []
    user_bdg = {}
    for badge in data_arr:
        if badge["Name"] == badge["Name"].lower():
            continue
        user_bdg[badge["UserId"]] = user_bdg.get("UserId", [])
        user_bdg[badge["UserId"]].append([badge["Name"]])
    for user in user_bdg:
        badges_o.append(one_enc.transform(user_bdg[user]).sum(axis= 0))
    badges_o = np.array(badges_o, dtype=bool)
    return badges_o, [badge[0] for badge in badges]

def arules_as_matrix(x, what = "items"):
    return ro.r('function(x) as(' + what + '(x), "matrix")')(x)

def arules_as_dict(x, what = "items"):
    l = ro.r('function(x) as(' + what + '(x), "list")')(x)
    l.names = [*range(0, len(l))]
    return dict(zip(l.names, map(list,list(l))))

def arules_quality(x):
    return x.slots["quality"]

def Miner(_inp_, tb):
    one_enc, c_header = _inp_
    df = pd.DataFrame(one_enc, columns= c_header)
    itsets = arules.apriori(df, parameter = ro.ListVector({"supp": 1e-3, "target": "frequent itemsets"}))
    arules.DATAFRAME(itsets).to_csv(f'{RES_DIR}/ARM_{tb}_fits.csv')
    rules = arules.apriori(df, parameter = ro.ListVector({"supp": 1e-3, "conf": 1e-2}))
    arules.DATAFRAME(rules).to_csv(f'{RES_DIR}/ARM_{tb}_mined.csv')

if __name__ == "__main__":
    Miner(tagsAsOE(), "tags")
    Miner(badgesAsOE(), "badges")