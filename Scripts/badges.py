from utils import *


def run_badges(stack_name, resdir):
    print("Badge Data Analysis")
    badges = load_file(stack_name, "Badges.json")

    resdir = resdir + "/Badges"
    if path.exists(resdir):
        rmtree(resdir)
    mkdir(resdir)

    if not badges:
        print("Data not available")
        return

    gold_badges = {}
    silver_badges = {}
    bronze_badges = {}
    user_badges = {}

    for entry in badges:
        if entry["Name"] == entry["Name"].lower():
            continue
        level = int(entry["Class"])
        if level == 1:
            if entry["Name"] not in gold_badges:
                gold_badges[entry["Name"]] = 0
            gold_badges[entry["Name"]] += 1
        elif level == 2:
            if entry["Name"] not in silver_badges:
                silver_badges[entry["Name"]] = 0
            silver_badges[entry["Name"]] += 1
        elif level == 3:
            if entry["Name"] not in bronze_badges:
                bronze_badges[entry["Name"]] = 0
            bronze_badges[entry["Name"]] += 1
        if entry["UserId"] not in user_badges:
            user_badges[int(entry["UserId"])] = []
        user_badges[int(entry["UserId"])].append({"name": entry["Name"], "time": entry["Date"][:7]})

    awarded_once = []
    badge_totals = {"gold": 0, "silver": 0, "bronze": 0}
    badges_sort = {}
    for badge in gold_badges:
        badge_totals["gold"] += gold_badges[badge]
        if gold_badges[badge] == 1:
            awarded_once.append(badge)
        badges_sort[badge] = gold_badges[badge]
    for badge in silver_badges:
        badge_totals["silver"] += silver_badges[badge]
        if silver_badges[badge] == 1:
            awarded_once.append(badge)
        badges_sort[badge] = silver_badges[badge]
    for badge in bronze_badges:
        badge_totals["bronze"] += bronze_badges[badge]
        if bronze_badges[badge] == 1:
            awarded_once.append(badge)
        badges_sort[badge] = bronze_badges[badge]

    sorted_badges = dict(sorted(badges_sort.items(), key=lambda x: x[1], reverse=True))
    top_ten = list(sorted_badges.keys())[:10]

    total_stats = {
        "total": len(badges),
        "gold": badge_totals["gold"],
        "silver": badge_totals["silver"],
        "bronze": badge_totals["bronze"],
    }

    results = {}
    results["Total Awarded"] = total_stats
    results["Gold Badges"] = gold_badges
    results["Silver Badges"] = silver_badges
    results["Bronze Badges"] = bronze_badges
    results["Top Ten Badges"] = top_ten
    results["Awarded Once"] = awarded_once

    print("Writing Results...")
    resultfile = resdir + "/badges.results.json"
    with open(resultfile, "w+") as f:
        json.dump(results, f, indent="\t")

    print("Generating Plots...")
    plot_bar_dict(total_stats).savefig(resdir + "/total_stats.png")
    plot_bar_dict(dict(list(sorted(gold_badges.items(), key=lambda x: x[1], reverse=True))[:10])).savefig(
        resdir + "/gold_stats.png"
    )
    plot_bar_dict(dict(list(sorted(silver_badges.items(), key=lambda x: x[1], reverse=True))[:10])).savefig(
        resdir + "/silver_stats.png"
    )
    plot_bar_dict(dict(list(sorted(bronze_badges.items(), key=lambda x: x[1], reverse=True))[:10])).savefig(
        resdir + "/bronze_stats.png"
    )

    make_wordcloud(gold_badges).savefig(resdir + "/gold.badges.png")
    make_wordcloud(silver_badges).savefig(resdir + "/silver.badges.png")
    make_wordcloud(bronze_badges).savefig(resdir + "/bronze.badges.png")
