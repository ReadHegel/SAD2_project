#!/bin/bash

source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate sad_generation

set -ex

simulate() {
    time python simulate_paths.py \
        --path "$1" \
        --outdir "$2" \
        --mode "${3:-asynchronous}" \
        --steps "${4:-100}" \
        --freq "${5:-10}" \
        --num_traj "$6"
}

simulate_n() {
    simulate "data/bn$1/network.bnet" "data/bn$1/trajectories" "$2" "$3" "$4" "$5"
}

for n in 5 7 10 13 16; do
    for mode in asynchronous synchronous; do
        for steps in 5 20; do
            for freq in 1 3 5; do
                for num_traj in 20 70; do
                    simulate_n $n $mode $steps $freq $num_traj
                done
            done
        done
    done
done
