""" Definitions for the InputDataGraph """
# graphs/input_data_graph.py
import re

from language.base_tokens import BaseTokens

class InputDataGraph:
    """ Graph structure representing common substructures in input data """
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
        return f"IDG:\n\t{self._edge_labels}"

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

        if node not in self._nodes:
            print(f"Node {node} not in InputDataGraph")
            return False

        if node not in self._node_labels:
            self._node_labels[node] = set([])

        _id, i = label
        self._node_labels[node].add((_id, i))
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

        if len(tok_match) != 2:
            print("Token matches must be of form (t, k)")
            return False

        if not tok_match[1]:
            return False

        v1, v2 = edge
        if v1 not in self._nodes or v2 not in self._nodes:
            print(f"Edge: {edge} not in InputDataGraph")
            return False

        self.add_edge(edge)
        if v1 not in self._edge_labels:
            self._edge_labels[v1] = {}

        if v2 not in self._edge_labels[v1]:
            self._edge_labels[v1][v2] = []

        self._edge_labels[v1][v2].append(tok_match)
        return True

    ### Public Properties
    @property
    def nodes(self):
        """ Nodes property """
        return self._nodes

    @property
    def node_labels(self):
        """ Node label property """
        return self._node_labels

    @property
    def edges(self):
        """ Edge property """
        return self._edges

    @property
    def edge_labels(self):
        """ Edge label property """
        return self._edge_labels

    @property
    def id(self):
        """ ID property """
        return self._id

    ### Public Methods
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

    def label_nodes(self, node: int, labels: list[tuple]):
        """ Label a node """
        for l in labels:
            self._label_node(node, l)

    def label_edges(self, edge: tuple, labels: list[tuple]):
        """ Label an edge """
        for l in labels:
            self._label_edge(edge, l)

    def to_dot(self, path: str) -> bool:
        """ generate a dot (graphviz) graph for the IDG """
        with open(path, "w", encoding='utf-8') as f:
            f.write("digraph idg {\n")
            for n1 in self._edge_labels:
                for n2 in self._edge_labels[n1]:
                    f.write(f"\"{n1}\" -> \"{n2}\" [label = \"{self._edge_labels[n1][n2]}\"];\n")
            f.write("}")

        return True

    ### Static, Public Methods
    @staticmethod
    def gen_graph_str(s: str, _id: int = -1):
        """ Generate a single IDG given an input string """
        # Init graph and get new unique string ID
        graph = InputDataGraph(_id)
        # label all the nodes
        for i in range(0, len(s) + 3):
            graph.add_node((i,))
            graph.label_nodes((i,), [(_id, i)])

        # label the start and end symbols
        graph.label_edges(
            ((0,),(1,)),
            [(BaseTokens.StartT.name, 1)]
        )
        graph.label_edges(
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
                graph.add_edge(((start,), (end,)))
                graph.label_edges(
                    ((start,), (end,)),
                    [((tok.name), (i+1, i-n))]
                )

        # Add string literal matches
        for i in range(1, len(s) + 1):
            for j in range(i+1, len(s) + 2):
                idx_l, idx_r = i-1, j-1
                substr = s[idx_l:idx_r]
                graph.add_edge(((i,), (j,)))

                # print(substr)
                # for the pattern, escape any regex special characters
                pat = substr.replace("(","\\(").replace(")", "\\)")
                pat = pat.replace("[","\\[").replace("]", "\\]")
                tok = re.compile(pat)
                matches = tuple(tok.finditer(s))
                n = len(matches)
                for k, span in enumerate(matches):
                    start, end = span.start()+1, span.end()+1
                    if start == i and end == j:
                        graph.label_edges(
                            ((start,), (end,)),
                            [((substr), (k+1, k-n))]
                        )
        return graph

    @staticmethod
    def intersect(graph_1, graph_2):
        """ Intersect two IDGs """
        new_graph = InputDataGraph()
        # O(n^4) in worst case be avearges to O(n^2) in practice
        for vi in graph_1.edge_labels:
            for vj in graph_2.edge_labels:
                for vk in graph_1.edge_labels[vi]:
                    for vl in graph_2.edge_labels[vj]:
                        # all tokens that the graphs share on the new edge
                        for tok in set(graph_1.edge_labels[vi][vk]) & set(graph_2.edge_labels[vj][vl]):
                            # add nodes
                            new_graph.add_node(vi + vj)
                            new_graph.add_node(vk + vl)
                            # add node label
                            new_labels1 = graph_1.node_labels[vi] | graph_2.node_labels[vj]
                            new_graph.label_nodes(vi + vj, new_labels1)

                            new_labels2 = graph_1.node_labels[vk] | graph_2.node_labels[vl]
                            new_graph.label_nodes(vk + vl, new_labels2)
                            # add edges
                            new_graph.add_edge((vi + vj, vk + vl))
                            new_graph.label_edges((vi + vj, vk + vl), [tok])
        return new_graph


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
