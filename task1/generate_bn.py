import argparse
import itertools
import os
import random

import matplotlib.pyplot as plt
import networkx as nx

import pandas as pd
import pyboolnet
from pyboolnet.file_exchange import bnet2primes
from pyboolnet.state_space import random_state
from pyboolnet.state_transition_graphs import (
    primes2stg,
    random_successor_asynchronous,
    successor_synchronous,
)


def random_regulatory_graph(nodes, max_parents=3):
    graph = {}
    for n in nodes:
        k = random.randint(0, min(max_parents, len(nodes) - 1))
        parents = random.sample(nodes, k)
        graph[n] = parents
    return graph


def random_boolean_function(parents):
    if not parents:
        return random.choice(["0", "1"])

    terms = []
    for values in itertools.product([0, 1], repeat=len(parents)):
        # If condition is True then f(values) = 1
        if random.random() < 0.5:
            literals = []
            for p, v in zip(parents, values):
                literals.append(p if v else f"!{p}")
            terms.append("(" + " & ".join(literals) + ")")

    return " | ".join(terms) if terms else "0"


def write_bnet(path, graph):
    with open(path, "w") as f:
        for node, parents in graph.items():
            func = random_boolean_function(parents)
            f.write(f"{node}, {func}\n")


# -------------------------------------------------
# Rysowanie grafu regulacyjnego
# -------------------------------------------------
def plot_graph(primes, path):
    pyboolnet.interaction_graphs.create_image(primes, path)


# -------------------------------------------------
# Rysowanie STG state transition graph
# -------------------------------------------------
def plot_stg(primes, mode, path):
    pyboolnet.state_transition_graphs.create_stg_image(primes, mode, path)


def main():
    parser = argparse.ArgumentParser(
        description="Boolean network generation with PyBoolNet"
    )
    parser.add_argument("--nodes", type=int, required=True)
    parser.add_argument("--outdir", type=str, required=True)

    # Used only for stg graph
    parser.add_argument(
        "--mode", choices=["synchronous", "asynchronous"], required=True
    )
    parser.add_argument("--trajectories", type=int, default=10)
    parser.add_argument("--steps", type=int, default=20)
    parser.add_argument("--stg_graph", action="store_true")
    parser.add_argument("--reg_graph", action="store_true")
    parser.add_argument("--seed", type=int, default=42)

    args = parser.parse_args()
    random.seed(args.seed)

    os.makedirs(args.outdir, exist_ok=True)

    nodes = [f"x{i}" for i in range(1, args.nodes + 1)]

    # --- sieć boolowska
    graph = random_regulatory_graph(nodes)
    bnet_path = os.path.join(args.outdir, "network.bnet")
    write_bnet(bnet_path, graph)

    primes = bnet2primes(bnet_path)

    # --- STG
    if args.stg_graph:
        stg_path = os.path.join(args.outdir, f"stg_{args.mode}.png")
        plot_stg(primes, args.mode, stg_path)
        print(f"[INFO] Saved STG to {stg_path}")

    if args.reg_graph:
        structure_graph_path = os.path.join(
            args.outdir, f"structure_graph_{args.mode}.png"
        )
        plot_graph(primes, structure_graph_path)
        print(f"[INFO] Saved REG graph to {structure_graph_path}")

    print("[DONE]")


if __name__ == "__main__":
    main()
