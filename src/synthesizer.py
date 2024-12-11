""" Main driver class Synthesizer for BlinkFilLO """
# src/synthesizer.py
import pdb
from graphs.input_data_graph import InputDataGraph as IDG
from graphs.dag import DAG
from language.expressions import StringExpr
from language.base_tokens import BaseTokens
import time

class SynthDriver:
    """ Class that drives synthesis process

        Note: The definition of this class is not complete and will include
        additional logic as we complete the project
    """
    def __init__(self):
        # string to unique id mechanism
        self._s_id = {}
        self._counter = 0

    def string_to_id(self, s: str) -> int:
        """ Retrieve a unique ID for the string """
        if s not in self._s_id:
            self._s_id[s] = self._counter
            _id = self._counter
            self._counter += 1
            return _id
        return self._s_id[s]

    # private
    def _gen_graph_column(self, data: list) -> IDG:
        """ Generate the input data graph for a spreadsheet column """
        graph = IDG.gen_graph_str(data[0], self.string_to_id(data[0]))
        for i in range(1, len(data)):
            graph = IDG.intersect(
                graph,
                IDG.gen_graph_str(
                    data[i],
                    self.string_to_id(data[i])
                )
            )
        return graph

    def _get_topological_sort(self, dag, start) -> list:
        """ Helper to sort dag nodes topologically """
        def _rec_topo_sort(v, visited, stack):
            visited[v] = True
            if v in dag.mapping:
                for node in dag.mapping[v]:
                    if not visited[node]:
                        _rec_topo_sort(node, visited, stack)
            stack.append(v)

        visited = {node: False for node in dag.nodes}
        stack = []

        for node in dag.nodes:
            if not visited[node]:
                _rec_topo_sort(start, visited, stack)

        stack.reverse()
        return stack

    # public
    def gen_input_data_graph(self, data: list[list]) -> IDG:
        """ Generate the input data graph for the spreadsheet """
        column_graphs = []
        for i, _ in enumerate(data):
            column_graphs.append(self._gen_graph_column(data[i]))

        return IDG.union(column_graphs)

    def gen_dag(self, inp_data: list, output_data: list, idg: IDG) -> DAG:
        """ Generate a DAG from a row of input/output example and IDG """
        examples = list(zip(inp_data[0], output_data))
        dag = DAG(
                num_nodes=len(examples[0][1]),
                string_to_id=self.string_to_id
            )

        inp, out = examples[0]
        dag.learn([inp], out, idg)

        for i in range(1, len(examples)):
            dag_p = DAG(
                        num_nodes=len(examples[i][1]),
                        string_to_id=self.string_to_id
                    )
            inp, out = examples[i]
            dag_p.learn([inp], out, idg)
            dag = DAG.intersect(dag_p, dag)

        dag.rank()
        return dag

    def extract_formula(self, dag: DAG) -> str:
        """ Given a DAG of expressions, extract LibreOffice Formulaes """
        start = dag.start_node
        final = dag.final_node

        distances = {node: {"rank":0, "parent": None} for node in dag.nodes}
        topo_sort = self._get_topological_sort(dag, start)
        for n1 in topo_sort:
            if n1 not in dag.mapping:
                continue

            for n2 in dag.mapping[n1]:
                new_dist = distances[n1]["rank"] + dag.ranks[n1][n2]
                if distances[n2]["rank"] < new_dist:
                    distances[n2]["rank"] = new_dist
                    distances[n2]["parent"] = n1

        path = []

        # simple case
        if final in dag.mapping[start]:
            for expr in dag.mapping[start][final]:
                path.append(expr)
        # do Djikstra's
        else:
            node = final
            while node != start:
                next_node = distances[node]["parent"]
                for expr in dag.mapping[next_node][node]:
                    path.append(expr)

                node = next_node

        # Then create a StringExpr and convert to formula
        path.reverse()
        #print(path)
        expr = StringExpr(path)
        return expr.to_formula()
