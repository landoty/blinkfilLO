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

    def _GenGraphColumn(self, data: list) -> IDG:
        """ Generate the input data graph for a spreadsheet column """
        G = IDG.GenGraphStr(data[0], self.string2Id(data[0]))
        for i in range(1, len(data)):
            G = IDG.intersect(
                G,
                IDG.GenGraphStr(
                    data[i],
                    self.string2Id(data[i])
                )
            )
        return G

    def GenInpDataGraph(self, data: list[list]) -> IDG:
        """ Generate the input data graph for the spreadsheet """
        # TODO do GenGraphColumn and intersect
        for i in range(len(data)):
            for j in range(len(data[i])):
                return self._GenGraphColumn(data[0])
