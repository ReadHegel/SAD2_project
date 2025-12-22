set -ex

simulate() {
    python simulate_paths.py \
        --path "$1" \
        --outdir "$2" \
        --mode "${3:-asynchronous}" \
        --steps "${4:-100}" \
        --freq "${5:-10}" \
        --num_traj "$6"
}

simulate5() {
    simulate "data/bn5/network.bnet" "data/bn5/trajectories" "$1" "$2" "$3" "$4"
}
simulate7() {
    simulate "data/bn7/network.bnet" "data/bn7/trajectories" "$1" "$2" "$3" "$4"
}
simulate10() {
    simulate "data/bn10/network.bnet" "data/bn10/trajectories" "$1" "$2" "$3" "$4"
}

#
# Simulate 5
#
simulate5 asynchronous 10 1 3
simulate5 asynchronous 10 3 3
simulate5 asynchronous 10 5 3

simulate5 synchronous 10 1 3
simulate5 synchronous 10 3 3
simulate5 synchronous 10 5 3

#
# Simulate 7
#

simulate7 asynchronous 10 1 3
simulate7 asynchronous 10 3 3
simulate7 asynchronous 10 5 3

simulate7 synchronous 10 1 3
simulate7 synchronous 10 3 3
simulate7 synchronous 10 5 3

#
# Simulate 10
#

simulate10 asynchronous 10 1 3
simulate10 asynchronous 10 3 3
simulate10 asynchronous 10 5 3

simulate10 synchronous 10 1 3
simulate10 synchronous 10 3 3
simulate10 synchronous 10 5 3
