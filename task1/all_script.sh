#!/bin/bash

set +ex

# rm -r data  
# ./generate_script.sh

rm -r data/*/trajectories/
./simulate_script.sh

rm data/bn*/reconstruction_results.csv
./infer_script.sh


