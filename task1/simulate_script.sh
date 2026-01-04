
source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate sad_generation

set -ex

simulate() {
    time python simulate_paths.py \
        --path "$1" \
        --outdir "$2" \
        --mode "${3:-asynchronous}" \
        --steps "${4:-100}" \
        --freq "${5:-10}" \
        --num_traj "$6"
}

simulate_n() {
    simulate "data/bn$1/network.bnet" "data/bn$1/trajectories" "$2" "$3" "$4" "$5"
}

#
# Simulate 5
#
simulate_n 5 asynchronous 20 1 20
simulate_n 5 asynchronous 20 3 20
simulate_n 5 asynchronous 20 5 20

simulate_n 5 synchronous 20 1 20
simulate_n 5 synchronous 20 3 20
simulate_n 5 synchronous 20 5 20

#
# Simulate 7
#

simulate_n 7 asynchronous 20 1 20
simulate_n 7 asynchronous 20 3 20
simulate_n 7 asynchronous 20 5 20

simulate_n 7 synchronous 20 1 20
simulate_n 7 synchronous 20 3 20
simulate_n 7 synchronous 20 5 20

#
# Simulate 10
#

simulate_n 10 asynchronous 20 1 20
simulate_n 10 asynchronous 20 3 20
simulate_n 10 asynchronous 20 5 20

simulate_n 10 synchronous 20 1 20
simulate_n 10 synchronous 20 3 20
simulate_n 10 synchronous 20 5 20

#
# Simulate 13
#

simulate_n 13 asynchronous 20 1 20
simulate_n 13 asynchronous 20 3 20
simulate_n 13 asynchronous 20 5 20

simulate_n 13 synchronous 20 1 20
simulate_n 13 synchronous 20 3 20
simulate_n 13 synchronous 20 5 20

#
# Simulate 16
#

simulate_n 16 asynchronous 20 1 20
simulate_n 16 asynchronous 20 3 20
simulate_n 16 asynchronous 20 5 20

simulate_n 16 synchronous 20 1 20
simulate_n 16 synchronous 20 3 20
simulate_n 16 synchronous 20 5 20
