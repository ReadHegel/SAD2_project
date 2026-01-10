#!/bin/bash

set -ex

if [[ -z "$SAD2_PROJECT" ]]; then
    echo "Error: SAD2_PROJECT environment variable is not set"
    echo "Run: export SAD2_PROJECT=/path/to/SAD2_project"
    exit 1
fi

simulate() {
    python "$SAD2_PROJECT/task1/simulate_paths.py" \
        --path "$1" \
        --outdir "$2" \
        --mode "${3:-asynchronous}" \
        --steps "${4:-100}" \
        --freq "${5:-10}" \
        --num_traj "$6"
}

for bn_dir in "$SAD2_PROJECT/task2/real_bns"/*/; do
    bn_name=$(basename "$bn_dir")
    bnet_file="$bn_dir/model.bnet"
    
    if [[ ! -f "$bnet_file" ]]; then
        echo "Skipping $bn_name (no model.bnet found)"
        continue
    fi
    
    echo "Processing $bn_name"
    
    outdir="$bn_dir/trajectories"
    mkdir -p "$outdir"
    
    for mode in asynchronous synchronous; do
        for steps in 5 20; do
            for freq in 1 3 5; do
                for num_traj in 20 70; do
                    simulate "$bnet_file" "$outdir" "$mode" "$steps" "$freq" "$num_traj"
                done
            done
        done
    done
done

echo "All done."