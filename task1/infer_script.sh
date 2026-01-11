#!/bin/bash

set -e

source "$(conda info --base)/etc/profile.d/conda.sh"

HEADER="mode,steps,numtraj,freq,attper,score_type,jaccard_result,jaccard_weighted_result"

HEADER_ALL="var_num,$HEADER"
TOTAL_CSV="all_data.csv"
echo "$HEADER_ALL" > "$TOTAL_CSV"

for BN in 5 7 10 13 16; do
    BN_DIR="data/bn${BN}"

    echo "Processing $BN_DIR"

    GT_PATH="$BN_DIR/ground_truth_digraph.pkl"
    TRAJ_DIR="$BN_DIR/trajectories"
    OUT_CSV="$BN_DIR/reconstruction_results.csv"

    if [[ ! -d "$TRAJ_DIR" || ! -f "$GT_PATH" ]]; then
        echo "Skipping $BN_DIR (missing trajectories or ground truth)"
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
        ATTPER=$(echo "$FILENAME" | grep -oE 'attper[0-9]+\.?[0-9]*' | sed 's/attper//')

        # -------- RUN INFERENCE 1 --------
        conda activate sad_inference
        python infer1.py --trajectories "$TRAJ" > /dev/null

        # -------- RUN INFERENCE 2 & CAPTURE OUTPUT --------
        conda activate sad_generation
        OUTPUT=$(python infer2.py --trajectories "$TRAJ" --gt_path "$GT_PATH")

        # -------- PARSE RESULTS --------
        for SCORE in MDL BDE; do
            JW=$(echo "$OUTPUT" | grep "$SCORE ---- jaccard_weighted result" | awk '{print $NF}')
            J=$(echo "$OUTPUT" | grep "$SCORE ---- jaccard result" | awk '{print $NF}')

            echo "$MODE,$STEPS,$NUMTRAJ,$FREQ,$ATTPER,$SCORE,$J,$JW" >> "$OUT_CSV"
            echo "$BN,$MODE,$STEPS,$NUMTRAJ,$FREQ,$ATTPER,$SCORE,$J,$JW" >> "$TOTAL_CSV"
        done

    done

done

echo "All done."
