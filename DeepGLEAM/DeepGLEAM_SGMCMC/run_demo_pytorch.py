import argparse
import numpy as np
import os
import sys
import yaml

from lib.utils import load_graph_data
from model.pytorch.dcrnn_supervisor_sgnht import DCRNNSupervisor


def run_dcrnn(args):
    with open(args.config_filename) as f:
        supervisor_config = yaml.load(f)

        graph_pkl_filename = supervisor_config['data'].get('graph_pkl_filename')
        sensor_ids, sensor_id_to_ind, adj_mx = load_graph_data(graph_pkl_filename)

        supervisor = DCRNNSupervisor(adj_mx=adj_mx, **supervisor_config)
        if args.loading_epoch != '':
            supervisor.setLoadEpoch(args.loading_epoch)
        mean_score, outputs = supervisor.evaluate('test')
        np.savez_compressed(args.output_filename, **outputs)
        print("MAE : {}".format(mean_score))
        print('Predictions saved as {}.'.format(args.output_filename))


if __name__ == '__main__':
    sys.path.append(os.getcwd())
    parser = argparse.ArgumentParser()
    parser.add_argument('--use_cpu_only', default=False, type=str, help='Whether to run tensorflow on cpu.')
    parser.add_argument('--config_filename', default='data/model/pretrained/COV-19/config.yaml', type=str,
                        help='Config file for pretrained model.')
    parser.add_argument('--output_filename', default='data/alltest_deepgleam_point_week31_seed1_epo69.npz')
    parser.add_argument('--loading_epoch', default='')
    args = parser.parse_args()
    run_dcrnn(args)
