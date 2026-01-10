#!/bin/bash

set -ex

if [[ -z "$SAD2_PROJECT" ]]; then
    echo "Error: SAD2_PROJECT environment variable is not set"
    echo "Run: export SAD2_PROJECT=/path/to/SAD2_project"
    exit 1
fi
cd "$SAD2_PROJECT/task2/real_bns" || exit 1
wget --directory-prefix=CARDIAC-DEVELOPMENT https://github.com/sybila/biodivine-boolean-models/raw/refs/heads/main/models/%5Bid-010%5D__%5Bvar-13%5D__%5Bin-2%5D__%5BCARDIAC-DEVELOPMENT%5D/model.bnet
wget --directory-prefix=NEUROTRANSMITTER-SIGNALING-PATHWAY https://github.com/sybila/biodivine-boolean-models/raw/refs/heads/main/models/%5Bid-015%5D__%5Bvar-14%5D__%5Bin-2%5D__%5BNEUROTRANSMITTER-SIGNALING-PATHWAY%5D/model.bnet
wget --directory-prefix=METABOLIC-INTERACTIONS-IN-GUT-MICROBIOME https://github.com/sybila/biodivine-boolean-models/raw/refs/heads/main/models/%5Bid-064%5D__%5Bvar-8%5D__%5Bin-4%5D__%5BMETABOLIC-INTERACTIONS-IN-GUT-MICROBIOME%5D/model.bnet