import os
import json

CACHE_DIR=os.path.join(os.path.expanduser("~"), ".cfn-docgen", "gui")
LOG_FILE=os.path.join(os.path.expanduser("~"), ".cfn-docgen", "log", "cfn-docgen.log")

os.makedirs(CACHE_DIR, exist_ok=True)
CACHE_FILE=os.path.join(CACHE_DIR, "config.json")

if not os.path.exists(CACHE_FILE):
    with open(CACHE_FILE, "w") as fp:
        json.dump(
            {
                "OpenDirIfSuccess": True,
                "OpenLogIfFail": True,
                "PrevDir": "~",
                "PrevFmt": "xlsx"    
            },
            fp,
        )

def cache_manager():

    cache:dict = None
    def manage_cache(key:str=None, val:str=None) -> dict:
        nonlocal cache
        if cache is None:
            with open(CACHE_FILE, "r") as fp:
                cache = json.load(fp)

        if key is not None:
            cache[key] = val
            with open(CACHE_FILE, "w") as fp:
                json.dump(cache, fp)

        return cache
    
    return manage_cache

