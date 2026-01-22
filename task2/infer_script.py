from task1.infer_script import process_bn
import os
import json
ID_MAP_FILE = "trajectory_id_map.json"

def main():
    all_ids = {}
    for bn_dir in os.listdir('task2/real_bns'):
        ids = process_bn(os.path.join('task2/real_bns', bn_dir))
        all_ids.update(ids)

    with open(ID_MAP_FILE, 'w') as f:
        json.dump(all_ids, f, indent=4)

if __name__ == "__main__":
    main()