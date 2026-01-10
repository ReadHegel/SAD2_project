#!/bin/bash

set -e

if [[ -z "$SAD2_PROJECT" ]]; then
    echo "Error: SAD2_PROJECT environment variable is not set"
    echo "Run: export SAD2_PROJECT=/path/to/SAD2_project"
    exit 1
fi

eval "$(conda shell.bash hook)"

HEADER="network,mode,steps,numtraj,freq,attper,score_type,jaccard_result,jaccard_weighted_result"

for bn_dir in "$SAD2_PROJECT/task2/real_bns"/*/; do
    bn_name=$(basename "$bn_dir")
    
    echo "Processing $bn_name"

    GT_PATH="$bn_dir/ground_truth_digraph.pkl"
    TRAJ_DIR="$bn_dir/trajectories"
    OUT_CSV="$bn_dir/reconstruction_results.csv"

    if [[ ! -d "$TRAJ_DIR" || ! -f "$GT_PATH" ]]; then
        echo "Skipping $bn_name (missing trajectories or ground truth)"
        continue
    fi

    # create CSV with header if not exists
    if [[ ! -f "$OUT_CSV" ]]; then
        echo "$HEADER" > "$OUT_CSV"
    fi

    for TRAJ in "$TRAJ_DIR"/*.csv; do
        echo "  Trajectory: $(basename "$TRAJ")"

        FILENAME=$(basename "$TRAJ")

        # -------- PARSE METADATA FROM FILENAME --------
        # example:
        # trajectory_asynchronous_step100_numtraj3_freq1_attper0.96.csv

        MODE=$(echo "$FILENAME" | grep -oE 'synchronous|asynchronous')
        STEPS=$(echo "$FILENAME" | grep -oE 'step[0-9]+' | sed 's/step//')
        NUMTRAJ=$(echo "$FILENAME" | grep -oE 'numtraj[0-9]+' | sed 's/numtraj//')
        FREQ=$(echo "$FILENAME" | grep -oE 'freq[0-9]+' | sed 's/freq//')
        ATTPER=$(echo "$FILENAME" | grep -oE 'attper[0-9.]+' | sed 's/attper//')

        # -------- RUN INFERENCE 1 --------
        conda activate sad_inference
        python "$SAD2_PROJECT/task1/infer1.py" --trajectories "$TRAJ" > /dev/null

        # -------- RUN INFERENCE 2 & CAPTURE OUTPUT --------
        conda activate sad_generation
        OUTPUT=$(python "$SAD2_PROJECT/task1/infer2.py" --trajectories "$TRAJ" --gt_path "$GT_PATH")

        # -------- PARSE RESULTS --------
        for SCORE in MDL BDE; do
            JW=$(echo "$OUTPUT" | grep "$SCORE ---- jaccard_weighted result" | awk '{print $NF}')
            J=$(echo "$OUTPUT" | grep "$SCORE ---- jaccard result" | awk '{print $NF}')

            echo "$bn_name,$MODE,$STEPS,$NUMTRAJ,$FREQ,$ATTPER,$SCORE,$J,$JW" >> "$OUT_CSV"
        done

    done

done

echo "All done."