import argparse
import igraph as ig
import itertools
from itertools import chain
import os
import random
from tqdm import tqdm

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
from attractors import compute_attractors_tarjan


# -------------------------------------------------
# Symulacje
# -------------------------------------------------
def simulate_sync(primes, init, steps):
    traj = [init]
    current = init
    for _ in range(steps - 1):
        current = successor_synchronous(primes, current)
        traj.append(current)
    return traj


def simulate_async(primes, init, steps):
    traj = [init]
    current = init
    for _ in range(steps):
        current = random_successor_asynchronous(primes, current)
        traj.append(current)
    return traj


def trajectory_to_df(traj, nodes):
    return pd.DataFrame([{n: s[n] for n in nodes} for s in traj])


def compute_attractors_igraph(stg):
    """
    Szybsza wersja compute_attractors_tarjan używająca igraph.
    Zwraca steady_states i cyclic_attractors.
    """

    # Lista wszystkich wierzchołków
    nodes = list(stg.nodes())
    node_index = {n: i for i, n in enumerate(nodes)}
    edges = [(node_index[u], node_index[v]) for u, v in stg.edges()]

    # Tworzymy graf igraph
    g = ig.Graph(directed=True)
    g.add_vertices(len(nodes))
    g.add_edges(edges)

    # Use the updated method names to avoid DeprecationWarnings
    scc_clustering = g.connected_components(mode="strong")
    sccs = scc_clustering.membership

    membership_to_nodes = {}
    for idx, m in enumerate(sccs):
        membership_to_nodes.setdefault(m, []).append(nodes[idx])

    steady_states = []
    cyclic_attractors = []

    # Use cluster_graph() to create the condensed graph
    cond_graph = scc_clustering.cluster_graph()

    for cluster_idx, scc_nodes in membership_to_nodes.items():
        # In the condensed graph, an attractor is a node with out-degree 0
        if cond_graph.outdegree(cluster_idx) == 0:
            if len(scc_nodes) == 1:
                # Check for self-loops: a single node is only a steady state
                # if it actually transitions to itself.
                node_idx = scc_clustering[cluster_idx][0]
                if g.get_eid(node_idx, node_idx, directed=True, error=False) != -1:
                    steady_states.append(scc_nodes[0])
            else:
                cyclic_attractors.append(set(scc_nodes))

    return steady_states, cyclic_attractors

def compute_attractors(primes, mode):
    stg = pyboolnet.state_transition_graphs.primes2stg(primes, mode)

    #print(stg)

    # steady_states, cyclic_attractors = compute_attractors_tarjan(stg)
    steady_states, cyclic_attractors = compute_attractors_igraph(stg)
    #print(steady_states, cyclic_attractors)

    return set(steady_states) | set(chain.from_iterable(cyclic_attractors))

def add_atractor_col(dataset_df, primes, attractors):

    node_size = len(primes.keys())

    dataset_df["isattractor"] = dataset_df.apply(
        lambda row: 1 if "".join(row[:node_size].astype(str)) in attractors else 0,
        axis=1,
    )

    return dataset_df

def run(primes, attractors, outdir: str, mode: str, steps: int, freq: int, num_traj: int, seed: int = 42):
    random.seed(seed)

    os.makedirs(outdir, exist_ok=True)

    nodes = primes.keys()

    # --- generate
    all_df = []
    for i in range(num_traj):
        init = random_state(primes)
        if mode == "synchronous":
            traj = simulate_sync(primes, init, steps * freq)
        else:
            traj = simulate_async(primes, init, steps * freq)

        dataset = traj[:: freq]
        df = trajectory_to_df(dataset, nodes)
        df["time"] = range(len(df))
        df["trajectory"] = i

        all_df.append(df)

    concat_df = pd.concat(all_df, ignore_index=True)
    concat_df = add_atractor_col(concat_df, primes, attractors)

    attractor_percent = concat_df["isattractor"].sum() / concat_df.shape[0]
    csv_name = f"trajectory_{mode}_step{steps}_numtraj{num_traj}_freq{freq}_attper{attractor_percent}"
    csv_path = os.path.join(outdir, csv_name + ".csv")
    concat_df.to_csv(csv_path, index=False)

    #print(f"[INFO] Saved trajectories to {csv_path}")

    #print("[DONE]")

def main():
    node_nums = [5, 7, 10, 13, 16]
    possible_modes = ['asynchronous', 'synchronous']
    steps_list = [5, 20, 50, 80]
    freq_list = [1, 3, 5]
    num_traj_list = [20, 50, 100]

    total_runs = len(node_nums) * len(possible_modes) * len(steps_list) * len(freq_list) * len(num_traj_list)

    with tqdm(total=total_runs, desc="Total progress") as pbar:
        for n in node_nums:
            primes = bnet2primes(f"data/bn{n}/network.bnet")
            for mode in possible_modes:
                attractors = compute_attractors(primes, mode)
                for steps in steps_list:
                    for freq in freq_list:
                        for num_traj in num_traj_list:
                            run(primes, attractors, f"data/bn{n}/trajectories", mode, steps, freq, num_traj)
                            pbar.update(1)


if __name__ == "__main__":
    main()
