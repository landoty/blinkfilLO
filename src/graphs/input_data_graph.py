""" Definitions for the InputDataGraph """
# graphs/input_data_graph.py

from typing import Union
import re

import pdb

from language.base_tokens import BaseTokens

class InputDataGraph:
    def __init__(self, _id: int = -1):
        """ Build an empty IDG

            An IDG encodes substring token matches contained within a single
            string

            V: set of nodes
            E: set of edges
            I: V -> {(id, idx)}, labeling function/map over indeces of the nodes
            L: E -> {(t, k)}, labeling function/map over token matches of the
            edges
        """
        # core member variables
        self._nodes = set()
        self._node_labels = {}
        self._edges = {}
        self._edge_labels = {}

        # member variable for generation
        self._id = _id

    ### Private Methods
    def __repr__(self):
        """ A better repr when printing a graph """
        return str(f"{self._edge_labels}\n\n{self._edges}\n\n{self._node_labels}\n\n{self._nodes}")

    def _label_node(self, node: int, label: tuple) -> bool:
        """ Label a single node

            Node labels of the form:

            {
                nodeID: (id, idx),
                ...
            }

            where id is the unqique ID from the string which the node is
            generated from and idx is the index the node represents in said
            string
        """
        if len(label) != 2:
            print("Label must be of form (id, i)")
            return False

        elif node not in self._nodes:
            print(f"Node {node} not in InputDataGraph")
            return False

        else:
            if node not in self._node_labels:
                self._node_labels[node] = []

            _id, i = label
            self._node_labels[node].append((_id, i))
            return True

    def _label_edge(self, edge: tuple, tok_match: tuple) -> bool:
        """ Label a single edge

            Edge labels of the form:

            {
                node1: {
                    node2: [(tok, k), ...],
                    ...
                },
                node2: {
                    node3: [(tok, k), ...],
                    ...
                },
                ...
            }
            where tok is the token that matched on that edge and k is the kth
            occurence of that match
        """
        if len(edge) != 2:
            print("Edges must be a pair")
            return False

        elif len(tok_match) != 2:
            print("Token matches must be of form (t, k)")
            return False

        elif not tok_match[1]:
            return False

        v1, v2 = edge
        if v1 not in self._nodes or v2 not in self._nodes:
            print(f"Edge: {edge} not in InputDataGraph")
            return False

        else:
            self.add_edge(edge)
            if v1 not in self._edge_labels:
                self._edge_labels[v1] = {}

            if v2 not in self._edge_labels[v1]:
                self._edge_labels[v1][v2] = []

            self._edge_labels[v1][v2].append(tok_match)
            return True

    ### Public Methods
    def get_id(self) -> int:
        return self._id

    def add_node(self, node: int):
        """ Add a node to the graph """
        if node in self._nodes:
            pass
        else:
            self._nodes.add(node)

    def add_edge(self, edge: tuple):
        """ Add an ordered pair to the edges in the graph """
        if len(edge) != 2:
            print("Edges must be a pair")
            return

        v1, v2 = edge
        if v1 > v2:
            # no back edges expected
            v1, v2 = v2, v1

        if v1 not in self._edges:
            self._edges[v1] = set([v2])

        elif v2 not in self._edges[v1]:
            self._edges[v1].add(v2)

    def I(self, node: int, labels: list[tuple]):
        """ Label a node """
        for l in labels:
            self._label_node(node, l)

    def L(self, edge: tuple, labels: list[tuple]):
        """ Label an edge """
        for l in labels:
            self._label_edge(edge, l)

    def GenSubStrExpr(self, vk, l, r, sid):
        """ Generate all substring expressions for the given string

        vk: string to generate SubStrExpr's for
        l: left position
        r: right position
        sid: unique string index
        """
        vl = set([])
        vr = set([])
        for v in self._nodes:
            if (sid, l) in self._node_labels.values():
                pass
        # pdb.set_trace()

    ### Static, Public Methods
    @staticmethod
    def GenGraphStr(s: str, _id: int = -1):
        """ Generate a single IDG given an input string """
        # Init graph and get new unique string ID
        G = InputDataGraph(_id)
        # label all the nodes
        for i in range(0, len(s) + 3):
            G.add_node((i,))
            G.I((i,), [(_id, i)])

        # label the start and end symbols
        G.L(
            ((0,),(1,)),
            [(BaseTokens.StartT.name, 1)]
        )
        G.L(
            ((len(s)+1,), (len(s)+2,)),
            [(BaseTokens.EndT.name, 1)]
        )

        # Add token matches
        for tok in BaseTokens:
            if tok is BaseTokens.StartT or tok is BaseTokens.EndT:
                continue
            matches = tuple(tok.value.finditer(s))
            n = len(matches)
            for i, span in enumerate(matches):
                start, end = span.start() + 1, span.end() + 1
                G.add_edge(((start,), (end,)))
                G.L(
                    ((start,), (end,)),
                    [((tok.name), (i+1, i-n))]
                )

        # Add string literal matches
        for i in range(1, len(s) + 1):
            for j in range(i+1, len(s) + 2):
                idxL, idxR = i-1, j-1
                substr = s[idxL:idxR]
                G.add_edge(((i,), (j,)))

                tok = re.compile(substr)
                matches = tuple(tok.finditer(s))
                n = len(matches)
                for k, span in enumerate(matches):
                    start, end = span.start()+1, span.end()+1
                    if start == i and end == j:
                        G.L(
                            ((start,), (end,)),
                            [((substr), (k+1, k-n))]
                        )
        return G

    @staticmethod
    def intersect(G1, G2):
        """ Intersect two IDGs """
        newG = InputDataGraph()

        # O(n^4) in worst case be avearges to O(n^2) in practice
        for vi in G1._edges:
            for vj in G2._edges:
                for vk in G1._edges[vi]:
                    for vl in G2._edges[vj]:
                        # all tokens that the graphs share on the new edge
                        for tok in set(G1._edge_labels[vi][vk]) & set(G2._edge_labels[vj][vl]):
                            # add nodes
                            newG.add_node(vi + vj)
                            newG.add_node(vk + vl)
                            # add node label
                            new_labels = G1._node_labels[vi] + G2._node_labels[vj]
                            newG.I(vi + vj, new_labels)
                            # add edges
                            newG.add_edge((vi + vj, vk + vl))
                            newG.L((vi + vj, vk + vl), [tok])
        return newG


    @staticmethod
    def union(graphs: list):
        """ Union two IDGs """
        if len(graphs) == 1:
            return graphs[0]

        '''
        newG = InputDataGraph()

        for v1 in G1._edges:
            for v2 in G1._edges[v1]:
                if v1 in newG._nodes and v2 in newG._nodes:
                    continue

                newG.add_node(v1)
                newG.I(v1, G1._node_labels[v1])
                newG.add_node(v2)
                newG.I(v2, G1._node_labels[v2])

                newG.add_edge((v1, v2))
                newG.L((v1, v2), G2._edge_labels[v1][v2])
        '''
