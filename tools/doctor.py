
import os, sys
from tools.self_test import check_imports, check_yaml

def main():
    print("== archive-hunter doctor ==")
    check_imports()
    check_yaml()
    for var in ["DISCORD_WEBHOOK_DEFAULT"]:
        if not os.environ.get(var):
            print(f"warn: {var} is not set")
    print("doctor OK")

if __name__ == "__main__":
    main()
