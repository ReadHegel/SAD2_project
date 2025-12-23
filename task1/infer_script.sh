#!/bin/bash

TRAJ_PATH=$1

if (($# != 1)); then
    >&2 echo "Illegal number of parameters, pass only the trajectory file"
    exit 1
fi
if ! [[ -f $TRAJ_PATH ]]; then
    echo "$TRAJ_PATH is not a valid trajectory file"
    exit 1
fi

source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate sad_inference
# source ../venv/bin/activate
python infer1.py --trajectories $TRAJ_PATH
deactivate

# source ../venv3/bin/activate
conda activate sad_generation
python infer2.py --trajectories $TRAJ_PATH --gt_path data/bn5/ground_truth_digraph.pkl
deactivate
