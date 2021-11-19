import json, sys, time, math
from datetime import datetime
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt
from pathlib import Path

DATA_DIRECTORY = "../Data/Extracted"
RES_DIR = f"../Results/{sys.argv[1]}"
fpath = f"{DATA_DIRECTORY}/{sys.argv[1]}/Users.json"
Path(RES_DIR).mkdir(parents=True, exist_ok=True)

with open(fpath, "r", encoding="utf8") as datajs:
    data_arr = json.load(datajs)["data"]

DATES_DAT_C = {}
DATES_DAT_L = {}
DATES_STR = []
for user in data_arr:
    c = datetime.strptime(user["CreationDate"][:10], "%Y-%m-%d")
    l = datetime.strptime(user["LastAccessDate"][:10], "%Y-%m-%d")
    if l < c:
        continue
    DATES_STR.append(user["CreationDate"][:10])
    DATES_STR.append(user["LastAccessDate"][:10])
    DATES_DAT_L[user["LastAccessDate"][:10]] = DATES_DAT_C.get(user["LastAccessDate"][:10], 0) + 1
    DATES_DAT_C[user["CreationDate"][:10]] = DATES_DAT_L.get(user["CreationDate"][:10], 0) + 1
DATES_STR = list(set(DATES_STR))
DATES = [datetime.strptime(d, "%Y-%m-%d") for d in DATES_STR]
DATES.sort()
start_date = DATES[0]
l_date = start_date
u_date = start_date

BUCKETS = {}
i_ = 0
while True:
    l_date = u_date
    if l_date > DATES[-1]:
        break
    u_date = l_date + relativedelta(months=+1)
    BUCKETS[i_] = {
        "ulim": u_date.strftime("%Y-%m-%d"),
        "llim": l_date.strftime("%Y-%m-%d"),
        "n_act": 0,
        "t_new": 0,
        "t_dea": 0,
        "t_act": BUCKETS[i_-1]["t_act"] if i_ != 0 else 0
    }
    curr_d = l_date
    while curr_d < u_date:
        BUCKETS[i_]["n_act"] += DATES_DAT_C.get(curr_d.strftime("%Y-%m-%d"), 0) - DATES_DAT_L.get(curr_d.strftime("%Y-%m-%d"), 0)
        BUCKETS[i_]["t_new"] += DATES_DAT_C.get(curr_d.strftime("%Y-%m-%d"), 0)
        BUCKETS[i_]["t_dea"] += DATES_DAT_L.get(curr_d.strftime("%Y-%m-%d"), 0)
        curr_d = curr_d + relativedelta(days=+1)
    BUCKETS[i_]["t_act"] += BUCKETS[i_]["n_act"]
    i_ += 1

to_dump = {
    "all_dates": DATES_STR,
    "c_dates": DATES_DAT_C,
    "l_dates": DATES_DAT_L,
    "buckets": BUCKETS
}

with open(f'{RES_DIR}/active_users.json', "w") as aujs:
    json.dump(to_dump, aujs, indent="\t")

fig = plt.figure(figsize=(12,6))
buckets = [i for i in BUCKETS]
# buckets = [f'{BUCKETS[i]["llim"]}to{BUCKETS[i]["llim"]}' for i in BUCKETS]
nd_users = [BUCKETS[i]["n_act"] for i in BUCKETS]
new_users = [BUCKETS[i]["t_new"] for i in BUCKETS]
dea_users = [BUCKETS[i]["t_dea"] for i in BUCKETS]
plt.plot(buckets, new_users, label = "New Activations")
plt.plot(buckets, dea_users, label = "Deactivations")
plt.plot(buckets, nd_users, label= "New Activations - Deactivations")
plt.legend()
plt.tight_layout(pad=0)
plt.savefig(f"{RES_DIR}/active-users.png")
plt.show()
plt.clf()