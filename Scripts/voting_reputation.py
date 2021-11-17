import json, sys, time, math
from datetime import datetime
import matplotlib.pyplot as plt
from pathlib import Path

DATA_DIRECTORY = "../Data/Extracted"
RES_DIR = f"../Results/{sys.argv[1]}"
fpath = f"{DATA_DIRECTORY}/{sys.argv[1]}/Users.json"
N_BUCKETS = 10
Path(RES_DIR).mkdir(parents=True, exist_ok=True)

with open(fpath, "r", encoding="utf8") as datajs:
    data_arr = json.load(datajs)["data"]

REPBCKT = {}

for user in data_arr:
    REPBCKT[user["Reputation"]] = REPBCKT.get(user["Reputation"], {"up": 0, "dw": 0})
    REPBCKT[user["Reputation"]]["up"] += int(user["UpVotes"])
    REPBCKT[user["Reputation"]]["dw"] += int(user["DownVotes"])

REP_COUNT = [int(i) for i in REPBCKT]
max_rep = int(math.ceil(max(REP_COUNT)/100)*100)
buck_size = max_rep//N_BUCKETS
BUCKETS = {}

for i in range(N_BUCKETS):
    BUCKETS[str(i)] = {"uplim": (i+1)*buck_size, "dwlim": i*buck_size, "upv": 0, "dwv": 0, "upr": -1}
    for j in range(BUCKETS[str(i)]["dwlim"], BUCKETS[str(i)]["uplim"]):
        rep_buck = REPBCKT.get(str(j), {"up": 0, "dw": 0})
        BUCKETS[str(i)]["upv"] += rep_buck["up"]
        BUCKETS[str(i)]["dwv"] += rep_buck["dw"]
        BUCKETS[str(i)]["upr"] = BUCKETS[str(i)]["upv"]*100/(BUCKETS[str(i)]["upv"] + BUCKETS[str(i)]["dwv"]) if (BUCKETS[str(i)]["upv"] + BUCKETS[str(i)]["dwv"]) != 0 else 0

fig = plt.figure(figsize=(12,6))
reps = [f"{BUCKETS[i]['dwlim']}-{BUCKETS[i]['uplim']}" for i in BUCKETS]
up_rate = [BUCKETS[i]["upr"] for i in BUCKETS]
plt.bar(reps, up_rate)
plt.tight_layout(pad=0)
plt.savefig(f"{RES_DIR}/voting-reputation.png")
plt.show()
plt.clf()