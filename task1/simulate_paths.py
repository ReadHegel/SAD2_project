import argparse
import itertools
from itertools import chain
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


def add_atractor_col(dataset_df, primes, mode):
    stg = pyboolnet.state_transition_graphs.primes2stg(primes, mode)
    attractors = compute_attractors_tarjan(stg)
    set_attractors = set(chain.from_iterable(attractors))
    node_size = len(primes.keys())

    dataset_df["isattractor"] = dataset_df.apply(
        lambda row: 1 if "".join(row[:node_size].astype(str)) in set_attractors else 0,
        axis=1,
    )

    return dataset_df


def main():
    parser = argparse.ArgumentParser(
        description="Boolean network simulation with PyBoolNet"
    )
    parser.add_argument("--path", type=str, required=True)
    parser.add_argument("--outdir", type=str, required=True)

    parser.add_argument(
        "--mode", choices=["synchronous", "asynchronous"], required=True
    )
    parser.add_argument("--steps", type=int, default=20)
    parser.add_argument("--freq", type=int, default=1)
    parser.add_argument("--num_traj", type=int, default=1)
    parser.add_argument("--seed", type=int, default=42)

    args = parser.parse_args()
    random.seed(args.seed)

    os.makedirs(args.outdir, exist_ok=True)

    primes = bnet2primes(args.path)
    nodes = primes.keys()

    # --- generate
    all_df = []
    for i in range(args.num_traj):
        init = random_state(primes)
        if args.mode == "synchronous":
            traj = simulate_sync(primes, init, args.steps * args.freq)
        else:
            traj = simulate_async(primes, init, args.steps * args.freq)

        dataset = traj[:: args.freq]
        df = trajectory_to_df(dataset, nodes)
        df["time"] = range(len(df))
        df["trajectory"] = i

        all_df.append(df)

    concat_df = pd.concat(all_df, ignore_index=True)
    concat_df = add_atractor_col(concat_df, primes, args.mode)

    attractor_percent = concat_df["isattractor"].sum() / concat_df.shape[0]
    csv_name = f"trajectory_{args.mode}_step{args.steps}_numtraj{args.num_traj}_freq{args.freq}_attper{attractor_percent}"
    csv_path = os.path.join(args.outdir, csv_name + ".csv")
    concat_df.to_csv(csv_path, index=False)

    print(f"[INFO] Saved trajectories to {csv_path}")

    print("[DONE]")


if __name__ == "__main__":
    main()
