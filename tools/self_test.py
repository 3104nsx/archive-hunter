
import importlib, yaml, sys

def check_imports():
    for mod in ["requests","lxml","cssselect","fastapi","uvicorn","yaml","PIL","imagehash"]:
        importlib.import_module(mod)
    print("imports OK")

def check_yaml():
    for path in ["config.eu.yaml","config.jp.yaml"]:
        with open(path,"r",encoding="utf-8") as f:
            yaml.safe_load(f)
    print("yaml OK")

if __name__ == "__main__":
    check_imports()
    check_yaml()
