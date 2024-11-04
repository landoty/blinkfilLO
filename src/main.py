""" Main driver for BlinkfilLO """
# main.py

from synthesizer import SynthDriver

if __name__ == "__main__":
    #data = [["1 lb", "23 g", "7 oz", "12 kg"]]
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

    synth = SynthDriver()
    IDG = synth.GenInpDataGraph(input_data)
    print(IDG)
    DAG = synth.GenDag(input_data[0], output_data[0], IDG)
    print(DAG)
