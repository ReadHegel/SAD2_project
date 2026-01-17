import os
import re
import csv
import json
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from infer2 import run_infer2

# --- CONFIG ---
ID_MAP_FILE = "trajectory_id_map.json"
TOTAL_CSV = "all_data.csv"
HEADER = ["mode", "steps", "numtraj", "freq", "attper", "score_type", "jaccard_result", "jaccard_weighted_result"]

def parse_metadata(filename):
    mode = "asynchronous" if "asynchronous" in filename else "synchronous"
    steps = re.search(r'step(\d+)', filename).group(1)
    numtraj = re.search(r'numtraj(\d+)', filename).group(1)
    freq = re.search(r'freq(\d+)', filename).group(1)
    attper = re.search(r'attper(\d+\.?\d*)', filename).group(1)
    return [mode, steps, numtraj, freq, attper]

def process_traj(traj_path, traj_id):
    traj_path_obj = Path(traj_path)
    bn_dir = traj_path_obj.parent.parent
    bn_val = bn_dir.name.replace("bn", "")
    gt_path = bn_dir / "ground_truth_digraph.pkl"
    out_csv = bn_dir / "reconstruction_results.csv"

    if not out_csv.exists():
        with open(out_csv, 'w', newline='') as f:
            csv.writer(f).writerow(HEADER)

    meta = parse_metadata(traj_path_obj.name)
    output = run_infer2(str(traj_path), str(gt_path), traj_id)
    rows = []
    for score in ["MDL", "BDE"]:
        j = output.get(f"{score}_jaccard")
        jw = output.get(f"{score}_jaccard_weighted")
        row = meta + [score, j, jw]
        # Append to local and global CSVs
        with open(out_csv, 'a', newline='') as f:
            csv.writer(f).writerow(row)
        rows.append([bn_val] + row)
    return rows

def main():
    if not os.path.exists(ID_MAP_FILE):
        print(f"Error: {ID_MAP_FILE} not found. Run Phase 1 first.")
        return

    with open(ID_MAP_FILE, 'r') as f:
        traj_to_id = json.load(f)

    with open(TOTAL_CSV, 'w', newline='') as f:
        csv.writer(f).writerow(["var_num"] + HEADER)

    all_rows = []
    with ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(process_traj, traj_path, traj_id)
            for traj_path, traj_id in traj_to_id.items()
        ]
        for future in as_completed(futures):
            rows = future.result()
            all_rows.extend(rows)

    with open(TOTAL_CSV, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(all_rows)

    print(f"\nPhase 2 Complete. Results saved to {TOTAL_CSV}")

if __name__ == "__main__":
    main()