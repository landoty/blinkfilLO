""" Definition for the DAG used in synthesis """
# graphs/dag.py

from .input_data_graph import InputDataGraph
import language.expressions as EXPRS

class DAG:
    def __init__(self, num_nodes: int):
        self._nodes = set(i for i in range(num_nodes+1))
        self._start_node = 0
        self._final_node = num_nodes
        self._edges = {}
        self._mapping = {} # mapping edges to substring expresssions

    def __repr__(self):
        """ A better repr for a DAG """
        return str(f"{self._nodes}\n\n{self._edges}\n\n{self._mapping}")

    def learn(self, input_data: list, output: str, IDG: InputDataGraph):
        """ Learn the mapping function on input/output example """
        for i in range(len(output)):
            for j in range(i+1, len(output)+1):
                # init edges
                if i in self._edges:
                    self._edges[i].add(j)
                else:
                    self._edges[i] = set([j])

                # learn
                if i not in self._mapping:
                    self._mapping[i] = {}

                self._mapping[i][j] = EXPRS.ConstStringExpr(output[i:j])
