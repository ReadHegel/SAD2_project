import subprocess
import pandas as pd
import os

NUM_CPU = 4
DIR = 'tmp/'

def run_infer1(trajectories_path):
    data_unknown_type = pd.read_csv(trajectories_path)
    assert type(data_unknown_type) is pd.DataFrame, "failed reading csf"
    data_df = data_unknown_type
    assert data_df is not None

    skip_names = ["trajectory", "time", "isattractor"]
    var_names = [name for name in data_df.columns.tolist() if name not in skip_names]

    preambule_string = ' '.join(['EXP{}:{}'.format(traj_num, time) for traj_num, time in zip(data_df['trajectory'], data_df['time'])]) + '\n'
    bnf_data_string = '\n'.join([var_name + ' ' + ' '.join([str(val) for val in data_df[var_name]]) for var_name in var_names])
    bnf_file_str = preambule_string + bnf_data_string

    if not os.path.exists('tmp'):
        os.makedirs('tmp')

    random_run_id = os.urandom(8).encode('hex')
    input_filename = "bnf_input_" + random_run_id + ".txt"
    input_path = DIR + input_filename

    with open(input_path, 'w') as bnf_input:
        bnf_input.write(bnf_file_str)

    scoring_types = ['MDL', 'BDE']
    for scoring_type in scoring_types:
        output_file_filename = "bnf_output_{}_{}.sif".format(random_run_id, scoring_type)
        output_file_path = DIR + output_file_filename
        cmd = [
            "bnf", "-e", input_path, "-g", "1", "--cpu={}".format(NUM_CPU), "-n", str(output_file_path), "-s", scoring_type, "-l", "3"
        ]
        subprocess.check_call(cmd)
    return random_run_id


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Bayesian network inferrer")
    parser.add_argument("--trajectories", type=str, required=True)
    args = parser.parse_args()
    run_infer1(args.trajectories)

if __name__ == "__main__":
    main()
