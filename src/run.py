""" Main driver for BlinkfilLO """
# main.py
import pdb
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

def load_data(data: str) -> dict:
    """ Load I/O examples from file or command line """
    if os.path.exists(data):
        with open(data, "r", encoding="utf-8") as f:
            raw_data = json.load(f)
    else:
        try:
            raw_data = json.loads(data)
        except:
            raise RuntimeError("Input data is not JSON-formatted. Accepts either file or stdin")


    data = {"input": [], "output": []}
    examples = raw_data["Examples"]
    for ex in examples:
        data["input"] += ex["Input"]
        data["output"].append(ex["Output"])

    # the idg generation process expects a 2d-list
    data["input"] = [data["input"]]
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

    try:
        synth = SynthDriver()
        IDG = synth.gen_input_data_graph(input_data)
        DAG = synth.gen_dag(input_data, output_data, IDG)

        formula = synth.extract_formula(DAG)
        formula = formula.replace("<input>", args.input_cell)
        print(formula)

    except Exception as e:
        print(f"error: {e}")
        sys.exit(1)
