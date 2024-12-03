""" Quick script to filter the correct benchmarks """
# eval/filter.py

import os
import shutil
import json

for benchmark in os.listdir("."):
    if not os.path.isdir(benchmark):
        continue

    meta = os.path.join(os.path.abspath(benchmark), "meta.json")
    remove = False
    with open(meta) as f:
        config = json.load(f)
        for ft in config["Features"]:
            if ft.lower() != "concatenation" and \
                ft.lower() != "multicolumn" and \
                ft.lower() != "substring":
                remove = True
                break

    if remove:
        shutil.rmtree(os.path.abspath(benchmark))
