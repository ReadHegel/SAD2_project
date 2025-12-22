import subprocess
import pandas as pd
import re
import os

def main():
    data_unknown_type = pd.read_csv('data/trajectories_synchronous.csv') # todo change to argument
    assert type(data_unknown_type) is pd.DataFrame, "failed reading csf"
    data_df = data_unknown_type # data_df is pd.DataFrame. python2 does not do typing
    assert data_df is not None

    var_name_pattern = r"^x\d*$"
    var_names = [col_name for col_name in data_df.columns.to_list() if re.match(var_name_pattern, col_name) and type(col_name) is str]

    preambule_string = ' '.join(['EXP{}:{}'.format(traj_num, time) for traj_num, time in zip(data_df['trajectory'], data_df['time'])]) + '\n'
    bnf_data_string = '\n'.join([var_name + ' ' + ' '.join([str(val) for val in data_df[var_name]]) for var_name in var_names]) # type: ignore
    bnf_file_str = preambule_string + bnf_data_string

    if not os.path.exists('tmp'):
        os.makedirs('tmp')

    with open('tmp/bnf_input.txt', 'w') as bnf_input:
        bnf_input.write (bnf_file_str)

    scoring_types = ['MDL', 'BDE']

    for scoring_type in scoring_types:
        cmd = 'bnf -e tmp/bnf_input.txt -n tmp/bnf_output_' + scoring_type + '.sif -s ' + scoring_type
        subprocess.check_call(cmd, shell=True)


main()
