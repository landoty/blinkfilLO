""" Definitions for the InputDataGraph """
# graphs/input_data_graph.py

class InputDataGraph:
    def __init__(self):
        """ Build an empty IDG

            An IDG encodes substring token matches contained within a single
            string

            V: set of nodes
            E: set of edges
            I: V -> {(id, idx)}, labeling function/map over indeces of the nodes
            L: E -> {(t, k)}, labeling function/map over token matches of the
            edges
        """
        self._nodes = set()
        self._node_labels = {}
        self._edges = {}
        self._edge_labels = {}

    ### Private Methods
    def __repr__(self):
        """ A better repr when printing a graph """
        return str(f"{self._edge_labels} \n {self._node_labels}")

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
            print("Node not in InputDataGraph")
            return False

        else:
            _id, i = label
            self._node_labels[node] = (_id, i)
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

        v1, v2 = edge
        if v1 not in self._nodes or v2 not in self._nodes:
            print(f"Edge: {edge} not in InputDataGraph")

        else:
            self.add_edge(edge)
            if v1 not in self._edge_labels:
                self._edge_labels[v1] = {}

            if v2 not in self._edge_labels[v1]:
                self._edge_labels[v1][v2] = []

            self._edge_labels[v1][v2].append(tok_match)

    ### Public Methods

    def add_node(self, node: int):
        """ Add a node to the graph """
        if node in self._nodes:
            print(f"Node {node} already in InputDataGraph")

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
