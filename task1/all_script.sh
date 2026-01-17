#!/bin/bash

set +ex
source "$(conda info --base)/etc/profile.d/conda.sh"

rm -r data  
./generate_script.sh

rm -r data/*/trajectories/
./simulate_script.sh --nruns 5

rm all_data.csv
rm data/bn*/reconstruction_results.csv
conda init
conda activate sad_inference
python2 infer_script.py
conda deactivate
conda activate sad_generation
python3 eval.py