# BlinkfilLO - A Blinkfill Extension for LibreOffice (LO)

This project is an alternative implementation of BlinkFill, a Program-
ming by Example (PBE) tool for spreadsheet string transformations
in the Microsoft Office application Excel. Introduced in 2016 as a
successor to the renowned FlashFill, BlinkFill makes a number of
enhancements to provide improved quality of results as well as
performance. Despite the widespread use of FlashFill, and its likely
integration of BlinkFill, there exists no comparable utility for Libre-
Office Calc, an open-source alternative to Excel. As such, our work
aims to fill this gap by implementing BlinkFilLO, an open-source
Calc extension for automatic programming of spreadsheet string
transformation formulas.

## Requirements

BlinkFilLO provides both a command-line interface (mostly for development) and a plug-in extension for LibreOffice (under development). The synthesis driver is written in pure Python3 and requires no third-party dependencies. Any standard Python3 installation should be able to execute the synthesis tool without installing any additional packages.

## Usage

```bash
usage: run.py [-h] [--example] [--data DATA] [--input_cell INPUT_CELL]

Run the BlinkFillLO CLI

options:
  -h, --help            show this help message and exit
  --example             Run a preset example
  --data DATA           Data to run the synthesizer on
  --input_cell INPUT_CELL
                        Input cell from table (default: 'A1')
```

From the CLI, invoke `run.py` to run the synthesizer, providing a json-formatted specification. We utilized the [PROSE benchmarks](https://github.com/microsoft/prose-benchmarks) for evaluation, so BlinkFilLO expects a specification to adhere to the form utilized in this dataset. When providing data on the command line, utiliez the following form:

```json
{
  "Examples": [
    {
      "Input": [
        "Landen, Doty"
      ],
      "Output": "LD"
    },
    {
      "Input": [
        "Jaxon, Avena"
      ],
      "Output": "JA"
    },
    {
      "Input": [
        "John, Smith"
      ],
      "Output": "JS"
    },
    {
      "Input": [
        "Vince, Carter"
      ],
      "Output": "VC"
    },
    {
      "Input": [
        "Samantha, Burke"
      ],
      "Output": "SB"
    }
  ]
}
```

BlinkFilLO will, by default, fill in the input cell as if it were filling in a formula within the spreadsheet. You may override this functionality with the `input_cell` option.

## Contributing and Debugging

This tool was developed as the final project for [EECS700 - Introduction to Program Synthesis](https://sankhs.com/eecs700) at the University of Kansas. As such, it will not be actively maintained following the conclusion of the semester. However, we have provided a simple debugging interface, primarily for visualizing the state of the underlying data structures used by BlinkFilLO. The two primary graphs - the Input Data Graph and DAG - are defined in ![](./src/graphs/input_data_graph.py) and ![](./src/graphs/dag.py). Both of these classes define a `to_dot` method that will produce a [Graphviz](https://graphviz.org/) formatted `.dot` file for a current IDG or DAG. We utilize this for the graphs included in our report and were helpful during development. Feel free to use this for any additional development. 

##### Convert .dot to .png
`dot -Tpng input.dot > output.png`

## Read Our Report!

Our report is included [here](./report/report.pdf) and the running example in the paper is provided [here](./report/example-spec.json)

Link to our video demo -> [DEMO](https://www.youtube.com/watch?v=8Bhyw_EuHWE)
