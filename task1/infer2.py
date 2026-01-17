import re
import networkx as nx
import pandas as pd
import pickle
from graph_metrics import GRAPH_METRICS

def run_infer2(trajectories_path, gt_path, run_id):
    scoring_types = ["MDL", "BDE"]
    data_unknown_type = pd.read_csv(trajectories_path)
    assert type(data_unknown_type) is pd.DataFrame, "failed reading csf"
    data_df: pd.DataFrame = data_unknown_type
    skip_names = ["trajectory", "time", "isattractor"]
    var_names = [name for name in data_df.columns.to_list() if name not in skip_names]
    var_name_pattern = '|'.join(re.escape(name) for name in var_names)
    with open(gt_path, "rb") as ground_truth_file:
        ground_truth_digraph: nx.DiGraph = pickle.load(ground_truth_file)
    results = {}
    for scoring_type in scoring_types:
        inferred_graph = nx.DiGraph()
        inferred_graph.add_nodes_from(var_names)
        with open(f"tmp/bnf_output_{run_id}_{scoring_type}.sif", "r") as bnf_output:
            bnf_output_str = bnf_output.read()
            for source, sign, destination in re.findall(
                f"({var_name_pattern})\\s*([+-])\\s*({var_name_pattern})",
                bnf_output_str,
            ):
                inferred_graph.add_edge(
                    source, destination, sign={1} if sign == "+" else {-1}
                )
        for metric in GRAPH_METRICS:
            metric_score = metric(ground_truth_digraph, inferred_graph)
            if metric.__name__ == "jaccard_weighted":
                results[f"{scoring_type}_jaccard_weighted"] = metric_score
            elif metric.__name__ == "jaccard":
                results[f"{scoring_type}_jaccard"] = metric_score
    return results

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Bayesian network inferrer")
    parser.add_argument("--trajectories", type=str, required=True)
    parser.add_argument("--gt_path", type=str, required=True)
    parser.add_argument("--id", type=str, required=True)
    args = parser.parse_args()
    results = run_infer2(args.trajectories, args.gt_path, args.id)
    for scoring_type in ["MDL", "BDE"]:
        print(f"{scoring_type} ---- jaccard result {results.get(f'{scoring_type}_jaccard')}")
        print(f"{scoring_type} ---- jaccard_weighted result {results.get(f'{scoring_type}_jaccard_weighted')}")

if __name__ == "__main__":
    main()
