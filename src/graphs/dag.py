""" Definition for the DAG used in synthesis """
# graphs/dag.py
from .input_data_graph import InputDataGraph
import language.expressions as EXPRS

class DAG:
    """ Directed Acyclic Graph to compactly store expressions in the language """
    def __init__(self, string_to_id, num_nodes: int = 0):
        self._nodes = list(range(num_nodes))
        self._start_node = 0
        self._final_node = num_nodes
        self._edges = {}
        self._mapping = {} # mapping edges to substring expresssions

        self.string_to_id = string_to_id # function pointer to string map

    def __repr__(self):
        """ A better repr for a DAG """
        return f"DAG:\n\t\n\tStart:{self.start_node}\n\tFinal:{self.final_node}\n\t{self._mapping}"

    @property
    def nodes(self) -> dict:
        """ get the nodes of the DAG """
        return self._nodes

    @property
    def edges(self) -> dict:
        """ get the edges of the DAG """
        return self._edges

    @property
    def mapping(self) -> dict:
        """ get the learned mapping for the DAG """
        return self._mapping

    @property
    def start_node(self) -> int:
        """ get the start node index """
        return self._start_node

    @start_node.setter
    def start_node(self, start):
        """ set the start node """
        self._start_node = start

    @property
    def final_node(self) -> int:
        """ get the final node index """
        return self._final_node

    @final_node.setter
    def final_node(self, final):
        """ set the final node """
        self._final_node = final

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

    @staticmethod
    def intersect(dag_1: 'DAG', dag_2: 'DAG') -> 'DAG':
        """ intersect two DAGs, construct a new DAG """
        # create a new, empty DAG
        new_dag = DAG(
                    string_to_id=dag_1.string_to_id
                )

        # cartesian product of nodes from two dags
        new_nodes_src = [(i,j) for i in dag_1.edges for j in dag_2.edges]
        # set the start node to the first intersected node
        new_dag.start_node = new_nodes_src[0]
        # intersect
        for node_src in new_nodes_src:
            n1_src, n2_src = node_src
            edges_1 = dag_1.mapping[n1_src]
            edges_2 = dag_2.mapping[n2_src]
            # cartesian product of all nodes on the source node edge 
            new_nodes_dst = [(i,j) for i in edges_1 for j in edges_2]
            # set the final node to the final intersected node
            new_dag.final_node = new_nodes_dst[-1]
            for node_dst in new_nodes_dst:
                n1_dst, n2_dst = node_dst

                # retrieve substring expression labels for each edge
                substr1 = dag_1.mapping[n1_src][n1_dst]
                substr2 = dag_2.mapping[n2_src][n2_dst]

                # perform the intersection
                intersection = []
                for s1 in substr1:
                    for s2 in substr2:
                        # equality over constant strings
                        if isinstance(s1, EXPRS.ConstStringExpr) and \
                        isinstance(s2, EXPRS.ConstStringExpr):
                            if s1 == s2:
                                intersection.append(s1)

                        # intersect defined by substringexpr
                        elif isinstance(s1, EXPRS.SubStringExpr) and \
                        isinstance(s2, EXPRS.SubStringExpr):
                            sub_int = EXPRS.SubStringExpr.interesct(s1,s2)
                            if sub_int:
                                intersection.append(sub_int)

                # a non-empty intersection is produced
                if intersection:
                    if node_src not in new_dag.edges:
                        new_dag.nodes.append(node_src)
                        new_dag.edges[node_src] = {}
                        new_dag.mapping[node_src] = {}

                    if node_dst not in new_dag.edges[node_src]:
                        new_dag.nodes.append(node_dst)
                        new_dag.edges[node_src][node_dst] = {}
                        new_dag.mapping[node_src][node_dst] = {}

                    new_dag.mapping[node_src][node_dst] = set(intersection)

        return new_dag
