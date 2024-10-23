""" Main driver for BlinkfilLO """
# main.py

from synthesizer import SynthDriver

if __name__ == "__main__":
    data = [["1 lb", "23 g", "7 oz"]]
    synth = SynthDriver()
    IDG = synth.GenInpDataGraph(data)
    print(IDG)
