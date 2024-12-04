""" Run the suite of benchmarks """
# eval/evaluate.py

import os
import sys
import time
import json
import signal
import argparse
import numpy as np
import pandas as pd

import pdb

sys.path.append("../src")
from synthesizer import SynthDriver

def timeout(sig, frame):
    raise TimeoutError("benchmark timeout")

def load_data(data: str) -> dict:
    with open(data, "r", encoding="utf-8") as f:
        raw_data = json.load(f)

    data = {"input": [], "output": []}
    examples = raw_data["Examples"]
    for ex in examples:
        data['input'] += ex["Input"]
        data['output'].append(ex["Output"])

    data["input"] = [data["input"]]
    return data

def run_bench(benchmark: str) -> list:
    """ run a benchmark """
    # load spec data
    spec = load_data(benchmark)

    # set signal handler
    signal.signal(signal.SIGALRM, timeout)

    # setup time and timer
    status = None
    end = -1
    signal.alarm(2)
    start = time.time()
    try:
        synth = SynthDriver()
        idg = synth.gen_input_data_graph(spec['input'])
        dag = synth.gen_dag(spec['input'], spec['output'], idg)
        formula = synth.extract_formula(dag)
        end = time.time() - start
        status = 'success'
    except TimeoutError as e:
        status = 'timeout'
    except Exception as e:
        status = 'fail'

    return (status, end)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                        prog="evaluate.py",
                        description="Run the BlinkFilLO Benchmarks"
            )
    parser.add_argument(
                "--benchmarks",
                dest="bench",
                required=True,
                help="Directory with benchmarks"
    )
    parser.add_argument(
                "--csv",
                dest="csv",
                default="benchmark.csv",
                help="Filename (csv) to save benchmark results to"
    )
    args = parser.parse_args()

    if os.path.isdir(args.bench):
        print(f"[+] Benchmark path: {os.path.abspath(args.bench)}")
        benchmark_results = []
        for bench in os.listdir(args.bench):
            # each benchmark should be a directory
            # with spec.json and meta.json
            # https://github.com/microsoft/prose-benchmarks
            if not os.path.isdir(bench):
                continue

            if "spec.json" in os.listdir(os.path.join(args.bench, bench)):
                print(f"[+] {bench}")
                status, delay = run_bench(os.path.join(args.bench, bench, "spec.json"))
                benchmark_results.append([bench, status, delay])

        # use a dataframe for analysis
        df = pd.DataFrame(
                    np.array(benchmark_results),
                    columns=["Benchmark", "Result", "Time"]
            )
        df["Time"] = pd.to_numeric(df["Time"])

        # pull out distinct trial sets
        successful = df[df['Result'] == 'success']
        failed = df[df['Result'] == 'fail']
        timeout = df[df['Result'] == 'timeout']

        # print results
        print(f"[+] Successful Benchmarks: {len(successful)}")
        print(f"[+] Average Time of Successful: {successful['Time'].mean()}")
        print(f"[+] Failed Benchmarks: {len(failed)}")
        print(f"[+] Timed Out Benchmarks: {len(timeout)}")
        print(f"[+] Saving results to: {args.csv}")
        df.to_csv(args.csv, index=True)

    else:
        print("Provide a directory with the benchmarks")
