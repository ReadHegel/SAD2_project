#!/bin/bash

source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate sad_generation

set -ex
python simulate_paths.py
