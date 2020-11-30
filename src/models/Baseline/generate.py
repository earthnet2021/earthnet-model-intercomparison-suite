import os
import numpy as np
import argparse
from tqdm import tqdm
import multiprocessing as mp
from functools import partial

from mean_model import ArithmeticMeanModel
from linear_model import LinearModel

parser = argparse.ArgumentParser(description="Predicts over the EarthNet test splits using the Baseline model.")
parser.add_argument('--dataroot', type = str, default = "data/datasets/release/", metavar = '/PATH/TO/CUBE/', help='Path to load files from')
parser.add_argument('--outpath', type = str, default = "data/outputs/", metavar = 'PATH/TO/OUTPUT/TO/', help ='Path to output files to')
parser.add_argument('--checkpoint', type = str, default = 'data/pretrained/Baseline', help ='Path to the pickled linear model')
parser.add_argument('--experiment_name', type = str, default = '01_test_mean', metavar = 'EXPERIMENT_NAME', help ='Name of the experiment')
parser.add_argument('--split_name', type = str, default = 'iid_test', metavar = 'SPLIT_NAME', help ='Name of the dataset split [iid_test,ood_test,seasonal_test,extreme_test]')
parser.add_argument('--submodel', type = str, default = 'mean', help ='Name of the baseline model [mean,linear]')
parser.add_argument('--context_length', type = int, default = 10, help ='Number of context frames')
parser.add_argument('--prediction_length', type = int, default = 20, help ='Number of context frames')
parser.add_argument('--keep_input', action='store_true', default=False, help='Saves the forecasts in a .NPZ that contains all of the layers of the input sample')
args = parser.parse_args()
    
    
if args.submodel == 'mean':
    model = ArithmeticMeanModel(args.context_length, args.prediction_length+args.context_length)
elif args.submodel == 'linear':
    model = LinearModel(args.context_length, args.prediction_length+args.context_length)

split_path = os.path.join(args.dataroot, args.split_name)
                            
#Count Samples in all Tile directories
cpt = sum([len(files) for r, d, files in os.walk(split_path)])
print("{0} samples found on the {1} split".format(cpt,args.split_name))

#Progress bar.
global pbar
pbar = tqdm(total=cpt)

#predicts and save. Parallelize it.
def predict_and_save(cpus, paths):
    in_path, out_file_path = paths
    input_data = np.load(in_path)
    pred = model.predict(input_data)
    
    #save predictions
    if args.keep_input:
        #saves predictors
        output_data = dict(input_data)
        output_data['highrespred'] = output_data['highresdynamic'][:,:,:4,:]
        output_data['highrespred'][:,:,:,args.context_length:] = pred
        np.savez(out_file_path, **output_data)
    else:
        #does not save predictors
        np.savez(out_file_path, pred)
    pbar.update(cpus)
        
#Loops trough Sentinel Tiles in the dataset/split directory
tiles = os.listdir(split_path)
tiles.sort()

in_files = []
out_files = []
for tile in tiles:
    in_tile_path = os.path.join(args.dataroot,  args.split_name, tile)
    out_tile_path = os.path.join(args.outpath, tile)
    if not os.path.exists(out_tile_path):
        os.makedirs(out_tile_path)
    files = os.listdir(in_tile_path)
    files.sort()
    for file in files:
        in_files.append(os.path.join(in_tile_path, file))
        out_files.append(os.path.join(out_tile_path, file))
#zip input paths and output paths
all_paths = zip(in_files, out_files)

cpus = mp.cpu_count()
pool = mp.Pool(cpus)
func = partial(predict_and_save, cpus)
pool.map(func, all_paths)
pool.close()