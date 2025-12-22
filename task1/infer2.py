import re
import networkx as nx
import pandas as pd

def main():
    scoring_types = ['MDL', 'BDE']
    var_name_pattern = r"x\d*"
    data_unknown_type = pd.read_csv('data/trajectories_synchronous.csv') # todo change to argument
    assert type(data_unknown_type) is pd.DataFrame, "failed reading csf"
    data_df: pd.DataFrame = data_unknown_type
    var_names = [col_name for col_name in data_df.columns.to_list() if re.match(var_name_pattern, col_name) and type(col_name) is str]

    for scoring_type in scoring_types:
        inferred_graph = nx.DiGraph()
        inferred_graph.add_nodes_from(var_names)
        with open('tmp/bnf_output_' + scoring_type + '.sif', 'r', encoding='utf-8') as bnf_output:
            bnf_output_str = bnf_output.read()
            for (source, sign, destination) in re.findall('(' + var_name_pattern + r')\s*([+-])\s*(' + var_name_pattern + ')', bnf_output_str):
                inferred_graph.add_edge(source, destination, weight=1 if sign == '+' else -1)


main()
