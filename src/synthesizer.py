""" Main driver class Synthesizer for BlinkFilLO """
# src/synthesizer.py

from graphs.input_data_graph import InputDataGraph as IDG
from language.base_tokens import BaseTokens

from typing import Union
import re


class SynthDriver:
    """ Class that drives synthesis process

        Note: The definition of this class is not complete and will include
        additional logic as we complete the project
    """
    def __init__(self):
        # string to unique id mechanism
        self._sId = {}
        self._counter = 0

        # map of match id/occurrences by string & token
        self._mId = {}

    ### Private methods
    def _string2Id(self, s: str) -> int:
        if s not in self._sId:
            self._sId[s] = self._counter
            _id = self._counter
            self._counter += 1
            return _id
        else:
            return self._sId[s]

    def _match2Id(self, pat: Union[str, BaseTokens], string: str, idx: int) -> int:
        """ Return the ID of the pattern in string starting at index i """

        # pattern is a string => constant string
        if isinstance(pat, str):
            # worst-case -> search for occurrences of pat in string
            if pat not in self._mId:
                pat_re = re.compile(pat)
                self._mId[pat] = {}
                for i,m in enumerate(pat_re.finditer(string)):
                    self._mId[pat][m.start()+1] = i+1

            return self._mId[pat][idx]

        # pattern is a BaseToken
        elif isinstance(pat, BaseTokens):
            if pat.pattern not in self._mId:
                pass
            return self._mId[path][idx]

    def GenGraphStr(self, s: str) -> IDG:
        """ Generate a single IDG given an input string """
        # Init graph and get new unique string ID
        G = IDG()
        _id = self._string2Id(s)

        # label all the nodes
        for i in range(0, len(s) + 3):
            G.add_node(i)
            G.I(i, [(_id, i)])

        # label the start and end symbols
        G.L(
            (0,1),
            [(BaseTokens.StartT.name, 1)]
        )
        G.L(
            (len(s)+1, len(s)+2),
            [(BaseTokens.EndT.name, 1)]
        )

        for i in range(1, len(s) + 1):
            for j in range(i+1, len(s) + 2):
                idxL, idxR = i, j
                G.add_edge((idxL, idxR))
                substr = s[idxL-1:idxR-1]
                G.L((i,j), [(substr, self._match2Id(substr, s, i))])
        return G
