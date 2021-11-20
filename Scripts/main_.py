import os, sys

if __name__ == "__main__":
    os.system(f"python3 main.py {sys.argv[1]}")
    os.system(f"python3 map_reduce.py {sys.argv[1]}")
    os.system(f"python3 question_time.py {sys.argv[1]}")
    os.system(f"python3 voting_reputation.py {sys.argv[1]}")
    os.system(f"python3 active_users.py {sys.argv[1]}")
    os.system(f"python3 association_rule.py {sys.argv[1]}")
