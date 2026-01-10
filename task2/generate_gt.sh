#!/bin/bash

set -ex

if [[ -z "$SAD2_PROJECT" ]]; then
    echo "Error: SAD2_PROJECT environment variable is not set"
    echo "Run: export SAD2_PROJECT=/path/to/SAD2_project"
    exit 1
fi

eval "$(conda shell.bash hook)"
conda activate sad_generation

for bn_dir in "$SAD2_PROJECT/task2/real_bns"/*/; do
    bn_name=$(basename "$bn_dir")
    bnet_file="$bn_dir/model.bnet"
    
    if [[ ! -f "$bnet_file" ]]; then
        echo "Skipping $bn_name (no model.bnet found)"
        continue
    fi
    
    echo "Generating ground truth for $bn_name"
    
    python "$SAD2_PROJECT/task1/generate_bn.py" \
        --path "$bnet_file" \
        --outdir "$bn_dir"
done

echo "All done."