import os
import glob
import json
from infer1 import run_infer1
from multiprocessing.pool import ThreadPool
from tqdm import tqdm

BN_NUMBERS = [5, 7, 10, 13, 16]
ID_MAP_FILE = "trajectory_id_map.json"

def process_bn(bn):
    bn_dir = os.path.join("data", "bn{}".format(bn))
    traj_dir = os.path.join(bn_dir, "trajectories")
    if not os.path.isdir(traj_dir):
        print("Skipping {} (missing trajectories dir)".format(bn_dir))
        return {}
    trajectories = glob.glob(os.path.join(traj_dir, "*.csv"))
    if not trajectories:
        print("Skipping {} (no trajectories found)".format(bn_dir))
        return {}
    def infer1_wrap(traj):
        return (traj, run_infer1(traj))
    pool = ThreadPool()
    results = []
    for result in tqdm(pool.imap_unordered(infer1_wrap, trajectories), total=len(trajectories), desc="BN{}".format(bn)):
        results.append(result)
    pool.close()
    pool.join()
    ids = dict(results)
    return ids

def main():
    all_ids = {}
    for bn in BN_NUMBERS:
        ids = process_bn(bn)
        all_ids.update(ids)
    with open(ID_MAP_FILE, 'w') as f:
        json.dump(all_ids, f, indent=4)
    print("\nPhase 1 Complete. IDs saved to {}".format(ID_MAP_FILE))

if __name__ == "__main__":
    main()