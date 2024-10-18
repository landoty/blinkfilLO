""" Main driver for BlinkfilLO """
# main.py

from synthesizer import SynthDriver

if __name__ == "__main__":
    data = [["Mumbai, India"]]
    synth = SynthDriver()
    IDG = synth.GenInpDataGraph(data)
    print(IDG)
