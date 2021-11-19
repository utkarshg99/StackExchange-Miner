from utils import *


def run_users(stack_name, resdir):
    print("Users Data Analysis")

    user_data = load_file(stack_name, "Users.json")

    resdir = resdir + "/Users"
    if path.exists(resdir):
        rmtree(resdir)
    mkdir(resdir)

    if not user_data:
        print("Data not available")
        return

    users = {}
    profiles = {}
    linkify = LinkifyIt()

    for entry in user_data:
        if "AccountId" not in entry:
            continue
        id = int(entry["AccountId"])
        reps = int(entry["Reputation"])
        if id < 0:
            continue
        if id not in users:
            users[id] = {}
            profiles[id] = {}
        users[id]["rep"] = reps
        users[id]["age"] = int(entry.get("Age", -1))
        users[id]["up"] = int(entry["UpVotes"])
        users[id]["down"] = int(entry["DownVotes"])
        users[id]["u/d"] = float(entry["UpVotes"]) / float(entry["DownVotes"]) if float(entry["DownVotes"]) > 0 else 0
        users[id]["created"] = entry["CreationDate"][:7]
        users[id]["last_acc"] = entry["LastAccessDate"][:7]

        profiles[id]["name"] = entry["DisplayName"]
        profiles[id]["email"] = entry.get("EmailHash", "")
        profiles[id]["site"] = entry.get("WebsiteUrl", "")
        profiles[id]["age"] = int(entry.get("Age", -1))
        profiles[id]["location"] = entry.get("Location", "")
        about = entry.get("AboutMe", "")
        profiles[id]["about"] = about
        urls = []
        if len(about) > 0:
            if linkify.test(about):
                links = linkify.match(about)
                for link in links:
                    urls.append(link.url)
        profiles[id]["links"] = urls
        profiles[id]["photo"] = entry.get("ProfileImageUrl", "")

    results = {}
    print("Writing Results...")
    resultfile = resdir + "/users.results.json"
    with open(resultfile, "w+") as f:
        json.dump(users, f, indent="\t")

    resultfile = resdir + "/profiles.results.json"
    with open(resultfile, "w+") as f:
        json.dump(profiles, f, indent="\t")
