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
    IDG = synth.gen_input_data_graph(input_data)
    print(IDG)
    DAG = synth.gen_dag(input_data, output_data, IDG)
    print(DAG)
