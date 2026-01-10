import re
import networkx as nx
import pandas as pd
import pickle
import argparse

from graph_metrics import GRAPH_METRICS


def compute_metrics(gt_graph: nx.DiGraph, inferred_graph: nx.DiGraph, name: str):
    for metric in GRAPH_METRICS:
        metric_score = metric(gt_graph, inferred_graph)
        print(f"{name} ---- {metric.__name__} result: {metric_score}")


def main():
    parser = argparse.ArgumentParser(description="Bayesian network inferrer")
    parser.add_argument("--trajectories", type=str, required=True)
    parser.add_argument("--gt_path", type=str, required=True)

    args = parser.parse_args()

    scoring_types = ["MDL", "BDE"]

    # -- Optain var_names
    data_unknown_type = pd.read_csv(args.trajectories)

    assert type(data_unknown_type) is pd.DataFrame, "failed reading csf"

    data_df: pd.DataFrame = data_unknown_type

    skip_names = ["trajectory", "time", "isattractor"]
    var_names = [name for name in data_df.columns.to_list() if name not in skip_names]
    var_name_pattern = '|'.join(re.escape(name) for name in var_names)

    # -- Get groupd_truth
    with open(args.gt_path, "rb") as ground_truth_file:
        ground_truth_digraph: nx.DiGraph = pickle.load(ground_truth_file)

    for scoring_type in scoring_types:
        inferred_graph = nx.DiGraph()
        inferred_graph.add_nodes_from(var_names)
        with open("tmp/bnf_output_" + scoring_type + ".sif", "r") as bnf_output:
            bnf_output_str = bnf_output.read()
            for source, sign, destination in re.findall(
                "(" + var_name_pattern + r")\s*([+-])\s*(" + var_name_pattern + ")",
                bnf_output_str,
            ):
                inferred_graph.add_edge(
                    source, destination, sign={1} if sign == "+" else {-1}
                )

        name = f"{scoring_type}"  # TODO dodać lepsze nazwy i w ogole lepszy wypisywanie wynikow
        compute_metrics(ground_truth_digraph, inferred_graph, name)


if __name__ == "__main__":
    main()
