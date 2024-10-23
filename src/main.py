""" Main driver for BlinkfilLO """
# main.py

from synthesizer import SynthDriver

if __name__ == "__main__":
    data = [["1 lb", "23 g"]]
    synth = SynthDriver()
    IDG = synth.GenInpDataGraph(data)
    print(IDG)
