""" Main driver class Synthesizer for BlinkFilLO """
# src/synthesizer.py
from graphs.input_data_graph import InputDataGraph as IDG
from graphs.dag import DAG
from language.expressions import StringExpr
from language.base_tokens import BaseTokens

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

    def gen_input_data_graph(self, data: list[list]) -> IDG:
        """ Generate the input data graph for the spreadsheet """
        column_graphs = []
        for i in range(len(data)):
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
            # intersect
            dag = DAG.intersect(dag_p, dag)
        return dag

    def extract_formula(self, dag: DAG) -> list[str]:
        """ Given a DAG of expressions, extract LibreOffice Formulaes """
        start = dag.start_node
        final = dag.final_node
        path = []

        # do Djikstra's here to get a path
        if final in dag.mapping[start]:
            # here, pick best node according to heuristic
            for expr in dag.mapping[start][final]:
                path.append(expr)

        # Then create a StringExpr and convert to formula
        expr = StringExpr(path)
        return(expr.to_formula())
