""" Definition for the DAG used in synthesis """
# graphs/dag.py
import pdb
from .input_data_graph import InputDataGraph
import language.expressions as EXPRS

class DAG:
    """ Directed Acyclic Graph to compactly store expressions in the language """
    def __init__(self, num_nodes: int, string_to_id):
        self._nodes = set(i for i in range(num_nodes+1))
        self._start_node = 0
        self._final_node = num_nodes
        self._edges = {}
        self._mapping = {} # mapping edges to substring expresssions

        self.string_to_id = string_to_id # function poiinter to string map

    def __repr__(self):
        """ A better repr for a DAG """
        return str(f"{self._nodes}\n\n{self._edges}\n\n{self._mapping}")

    @property
    def edges(self) -> dict:
        """ get the edges of the DAG """
        return self._edges

    @property
    def mapping(self) -> dict:
        """ get the learned mapping for the DAG """
        return self._mapping

    # Public Methdods
    def learn(self, input_data: list, output: str, idg: InputDataGraph):
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

                os = output[i:j]
                self._mapping[i][j] = set([EXPRS.ConstStringExpr(os)])
                for vk in input_data:
                    l = vk.index(os) + 1
                    r = l + len(os)
                    substr = EXPRS.gen_sub_str_expr(
                                        vk,
                                        l,
                                        r,
                                        self.string_to_id(vk),
                                        idg
                                )
                    self._mapping[i][j].add(substr)
