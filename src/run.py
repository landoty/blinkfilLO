""" Main driver for BlinkfilLO """
# main.py

import os
import sys
import argparse
import json
from synthesizer import SynthDriver

input_data = [
    [
        "Mumbai, India",
        "Los Angeles, USA",
        "Newark, USA",
        "New York, USA",
        "Wellington, New Zeland"
    ]
]

output_data = [
    "India",
    "USA",
    "USA",
    "USA",
    "New Zeland"
]

def load_data(file: str) -> dict:
    """ Load I/O examples from file """
    if not os.path.exists(file):
        raise FileNotFoundError(f"Could not find: {file}")

    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)
        if "input" not in data:
            raise RuntimeError("data must have an \'input\' object")
        if "output" not in data:
            raise RuntimeError("data must have an \'output\' object")

        return data

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                        prog="run.py",
                        description="Run the BlinkFillLO CLI"
            )
    parser.add_argument(
                "--example",
                dest="example",
                action="store_true",
                help="Run a preset example"
            )
    parser.add_argument(
                "--data",
                dest="data",
                help="Data to run the synthesizer on"
            )
    parser.add_argument(
                "--input_cell",
                dest="input_cell",
                default="A1",
                help="Input cell from table (default: \'A1\')"
            )
    args = parser.parse_args()

    if args.data:
        try:
            data = load_data(args.data)
            input_data = data["input"]
            output_data = data["output"]
        except Exception as e:
            print(e)
            sys.exit(1)

    else:
        print("Running hard-coded example")

    synth = SynthDriver()
    IDG = synth.gen_input_data_graph(input_data)
    DAG = synth.gen_dag(input_data, output_data, IDG)
    formulas = synth.extract_formula(DAG)
    print(formulas.replace("<input>", args.input_cell))
