""" Main driver for BlinkfilLO """
# main.py

from synthesizer import SynthDriver

if __name__ == "__main__":
    synth = SynthDriver()
    G = synth.GenGraphStr("1 lb") # example string from BlinkFill paper
    print(G)
