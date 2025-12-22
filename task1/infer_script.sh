#!/bin/bash
source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate sad_inference
python infer1.py
conda activate sad_inference2
python infer2.py
