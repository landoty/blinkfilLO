""" Main driver class Synthesizer for BlinkFilLO """
# src/synthesizer.py

from graphs.input_data_graph import InputDataGraph as IDG
from language.base_tokens import BaseTokens

class SynthDriver:
    """ Class that drives synthesis process

        Note: The definition of this class is not complete and will include
        additional logic as we complete the project
    """
    def __init__(self):
        # string to unique id mechanism
        self._sId = {}
        self._counter = 0

    def string2Id(self, s: str) -> int:
        if s not in self._sId:
            self._sId[s] = self._counter
            _id = self._counter
            self._counter += 1
            return _id
        else:
            return self._sId[s]

    def GenInpDataGraph(self, data: list[list]) -> IDG:
        """ Generate the input data graph for the spreadsheet """
        # TODO do GenGraphColumn and intersect
        for i in range(len(data)):
            for j in range(len(data[i])):
                s = data[i][j]
                return IDG.GenGraphStr(s, self.string2Id(s))
