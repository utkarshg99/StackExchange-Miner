import json
from datetime import datetime
import matplotlib.pyplot as plt
from networkx.drawing.nx_pylab import draw_circular
from utils import *
from utils import load_file
from collections import OrderedDict

def run_fastestgun(stack_name, resdir):
    print("Fastest gun in the west analysis")

    data_arr = load_file(stack_name, "Posts.json")

    resdir = resdir + "/Fastestgun"
    if path.exists(resdir):
        rmtree(resdir)
    mkdir(resdir)

    if not data_arr:
        print("Data not available")
        return

    POST_TIME_MAPPING = {}
    POST_ACC_ANS_TIME = {}
    POST_ACC_ANS_RANK = {}

    def isQuestion(post):
        return ("PostTypeId" in post and post["PostTypeId"] == "1")

    def isAnswer(post):
        return ("PostTypeId" in post and post["PostTypeId"] == "2")

    for post in data_arr:
        tme = datetime.strptime(post["CreationDate"][:-4], "%Y-%m-%dT%H:%M:%S") 
        POST_TIME_MAPPING[post["Id"]] = tme

    for post in data_arr:
        tme = datetime.strptime(post["CreationDate"][:-4], "%Y-%m-%dT%H:%M:%S") 
        if isQuestion(post):
            if "AcceptedAnswerId" in post:
                POST_ACC_ANS_TIME[post["Id"]] = POST_TIME_MAPPING[post["AcceptedAnswerId"]]

    for post in data_arr:
        tme = datetime.strptime(post["CreationDate"][:-4], "%Y-%m-%dT%H:%M:%S") 
        if isAnswer(post):
            if "ParentId" in post:
                if post["ParentId"] not in POST_ACC_ANS_RANK:
                    POST_ACC_ANS_RANK[post["ParentId"]] = 1
                
                if post["ParentId"] in POST_ACC_ANS_TIME:
                    POST_ACC_ANS_RANK[post["ParentId"]] += (POST_ACC_ANS_TIME[post["ParentId"]] >= tme)

    acc_rank_count = {}

    for k, v in POST_ACC_ANS_RANK.items():
        if v not in acc_rank_count:
            acc_rank_count[v] = 0
        acc_rank_count[v] += 1

    res_dict = dict()
    res_dict['Count'] = OrderedDict(sorted(acc_rank_count.items()))

    rank, count = zip(*(sorted(acc_rank_count.items())))
    tot = sum(count)
    perc = [ 100 * x / tot for x in count ]
    perc_dict = dict(zip(rank, perc))
    
    res_dict['Percentage'] = OrderedDict(sorted(perc_dict.items()))

    resultfile = resdir + "/fastestgun.json"
    with open(resultfile, "w+") as f:
        json.dump(res_dict, f, indent="\t")
    

    fig = plt.plot(rank, perc)
    plt.xlabel("Accepted Answer Rank")
    plt.ylabel("Percentange")
    plt.savefig(f"{resdir}/fastestgun.png")
    plt.clf()