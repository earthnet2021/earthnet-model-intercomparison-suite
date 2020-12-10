'''
Translates the dataset from .npz to serialized .tfrecords.
Exports data into .tfrecords readable by off-the-shelf tensorflow implementations
of Video Prediction models such as SAVP.

Warning:
The TFrecords exported are a rundown version of the .npz samples. Interpolation 
is done in some layers, precission might be lost, temporal resolution of predictors 
is neglected. Use the native .npz for model training when possible for full potential.

'''

import numpy as np
import os
import argparse
from tqdm import tqdm
import tensorflow as tf
from scipy.ndimage import zoom
import multiprocessing as mp
from functools import partial

def _bytes_feature(value):
    return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))


def _bytes_list_feature(values):
    return tf.train.Feature(bytes_list=tf.train.BytesList(value=values))


def _int64_feature(value):
    return tf.train.Feature(int64_list=tf.train.Int64List(value=[value]))

def preprocess_8b(sample):
    '''Transforms a single .npz sample of the EarthNet dataset. Into
    .tfrecords in 8 bites

    Params
    ------
    sample: np.array 
        Array with the sample data to be written to a
        single cube of .tfrecords

    Returns
    -------
    sample_out: byte like serialization of the input sample to be saved.
        sample_out contains: (128,128,12)
        Target:
            Channel 1 (Red):      B4 RED
            Channel 2 (Green):    B3 GREEN
            Channel 3 (Blue):     B2 BLUE
            Channel 4 (Infrared): B8 NIR

        Pred:
            Channel 5 :        High Res DEM
            Channel 6 :        Precipitation
            Channel 7 :        Pressure
            Channel 8 :        Daily Mean Temperature
            Channel 9 :        Daily Min Temperature
            Channel 10:        Daily Max Temperature
            Channel 11:        Mesoscale DM
        
        Mask:
            Channel 12 :       Bad Data Mask (clouds/shadows/buffers)

    '''
    sample_out = sample*255
    
    sample_out = sample_out.astype(np.uint8)
    return sample_out.tobytes()

def preprocess_f16(sample):
    '''Transforms a single .npz sample of the EarthNet dataset. Into
    .tfrecords in floating 16b

    Params
    ------
    sample: np.array 
        Array with the sample data to be written to a
        single cube of .tfrecords

    Returns
    -------
    sample_out: byte like serialization of the input sample to be saved.
        sample_out contains: (128,128,12)
        Target:
            Channel 1 (Red):      B4 RED
            Channel 2 (Green):    B3 GREEN
            Channel 3 (Blue):     B2 BLUE
            Channel 4 (Infrared): B8 NIR

        Pred:
            Channel 5 :        High Res DEM
            Channel 6 :        Precipitation
            Channel 7 :        Pressure
            Channel 8 :        Daily Mean Temperature
            Channel 9 :        Daily Min Temperature
            Channel 10:        Daily Max Temperature
            Channel 11:        Mesoscale DM
        
        Mask:
            Channel 12 :       Bad Data Mask (clouds/shadows/buffers)

    '''
    
    sample_out = sample.astype(np.float16)
    return sample_out.tobytes()

def save_tf_record_v1(output_fname, sequences, preprocess_image):
    with tf.io.TFRecordWriter(output_fname) as writer:
        for sequence in sequences:
            num_frames = len(sequence)
            height, width, channels = sequence[0].shape
            sequence = sequence
            encoded_sequence = [preprocess_image(image) for image in sequence]
            features = tf.train.Features(feature={
                'sequence_length': _int64_feature(num_frames),
                'height': _int64_feature(height),
                'width': _int64_feature(width),
                'channels': _int64_feature(channels),
                'images/encoded': _bytes_list_feature(encoded_sequence),
            })
            example = tf.train.Example(features=features)
            writer.write(example.SerializeToString())

def save_tf_record_v2(output_fname, sequences, preprocess_image):
    with tf.io.TFRecordWriter(output_fname) as writer:
        for sequence in sequences:
            num_frames = len(sequence)
            height, width, _ = sequence[0].shape
            color_channels = 4
            guide_channels = 7
            mask_channels = 1
            sequence = sequence
            encoded_images = [preprocess_image(image) for image in sequence[:,:,:4]]
            encoded_guides = [preprocess_image(image) for image in sequence[:,:,:11]]
            encoded_mask = [preprocess_image(image) for image in sequence[:,:,11:]]
            features = tf.train.Features(feature={
                'sequence_length': _int64_feature(num_frames),
                'height': _int64_feature(height),
                'width': _int64_feature(width),
                'color_channels': _int64_feature(color_channels),
                'guide_channels': _int64_feature(guide_channels),
                'mask_channels': _int64_feature(mask_channels),
                'images/encoded': _bytes_list_feature(encoded_images),
                'guides/encoded': _bytes_list_feature(encoded_guides),
                'mask/encoded': _bytes_list_feature(encoded_mask),
            })
            example = tf.train.Example(features=features)
            writer.write(example.SerializeToString())

def translate_NPZ(cpus, dataformat, paths):
        #unzip the paths variables
        NPZ_path, filename = paths
        
        #print(NPZ_path)
        #loads array, safely concatenates them if split into context and target.
        NPZ = np.load(NPZ_path)
        if "context" in NPZ_path:
            target_NPZ = np.load(NPZ_path.replace("context", "target",2))
            highresdynamic = np.concatenate((NPZ['highresdynamic'], target_NPZ['highresdynamic']), axis=3)
        else:
            highresdynamic = NPZ['highresdynamic']
        mesodynamic = NPZ['mesodynamic']
        highresstatic = NPZ['highresstatic']
        mesostaic = NPZ['mesostatic']
        
        if "train" in NPZ_path:
            blue, green, red, nir, _, _, mask = np.split(highresdynamic.astype(np.float), 7, axis=2)
        else:
            blue, green, red, nir, mask = np.split(highresdynamic.astype(np.float), 5, axis=2)
            
        hr_dem = highresstatic.astype(np.float)

        #resample mesoscale (usually 80x80xXx150) to match highres (usually 128x128xYx30)
        hr_h, hr_w, _, hr_t = mask.shape
        meso_h, meso_w, meso_c, meso_t = mesodynamic.shape
        factor_h, factor_w, factor_t = hr_h/meso_h, hr_w/meso_w, hr_t/meso_t

        mesodynamic = zoom(mesodynamic.astype(np.float), (factor_h, factor_h, 1, factor_t), order=2)
        #we shift by 1 the weather predictors so they are fed 1 time step early.
        mesodynamic_shifted = np.roll(mesodynamic, shift=-1, axis=3)
        meso_dem = zoom(mesostaic.astype(np.float), (factor_h, factor_h, 1), order=2)
        
        #Where Sea Level Pressure == 0 mbar (channel 1), replace by np.nan
        for layer in range(0,5):
            var = mesodynamic_shifted[:,:,layer,:]
            var = np.where(mesodynamic_shifted[:,:,1,:]<0.01, np.nan, var)
            var = np.where(var == np.nan, np.nanmean(var), var)
            mesodynamic_shifted[:,:,layer,:] = var
            
        rr, pp, tg, tn, tx = np.split(mesodynamic_shifted, 5, axis=2)
        
        hr_dem = np.repeat(np.expand_dims(hr_dem, 3), hr_t, axis=3)
        meso_dem = np.repeat(np.expand_dims(meso_dem, 3), hr_t, axis=3)

        #Stack our arrays
        arrays = [red, green, blue, nir, hr_dem, rr, pp, tg, tn, tx, meso_dem, mask]
        sample = np.stack(arrays, axis=2)

        #move temporal axis to first axis
        sample = np.moveaxis(sample, -1, 0)
        sample = np.squeeze(sample)

        #generate and save the .tfrecord
        if dataformat=='v1':
            save_tf_record_v1(filename,[sample], preprocess_f16)
        elif dataformat=='v2':
            save_tf_record_v2(filename,[sample], preprocess_f16)
        else:
            raise NotImplementedError
            
        pbar.update(cpus)

def make_tfrecords(split_path='data/dataset/train', out_path='data/tf_dataset/train/', dataformat='v1'):
    '''
    Loops trough all tile folders given in split_path. Loads the .npz and
    generates a .tfrecords mirroring the same data structure.
    
    Each .npz array dictionary contains:
        'highresdynamic': [blue, green, red, nir, cloud, scene, mask](128,128,7,X)
        'highresstatic': [elevation](128,128)
        'mesodynamic': [precipitation, pressure, temp mean, temp min, temp max](80,80,5,X*5)
        'mesostatic': [elevation](80,80)
        
    Params
    ------
    split_path: string
        path to load the dataset split .npz from
    out_path: string
        path to save the .tfrecords dataset to
    
    '''
    
    if not os.path.exists(out_path):
        os.makedirs(out_path)
        
    #Count Samples in every tile directories
    cpt = sum([len(files) for r, d, files in os.walk(split_path)])
    print("{0} samples found in the {1} split".format(cpt, split_path))
    
    global pbar
    pbar = tqdm(total=cpt)
    concatenate=False
    
    print(split_path)
    if "_split" in split_path:
        split_path = os.path.join(split_path,"context")
    tiles = os.listdir(split_path)
        
    if 'LICENSE' in tiles:
        tiles.remove('LICENSE')
    tiles.sort()
    
    dirs = []
    filenames = []
    
    for tile in tiles:
        in_tile_path = os.path.join(split_path, tile)
        out_tile_path = os.path.join(out_path, tile)
        if not os.path.exists(out_tile_path):
            os.makedirs(out_tile_path)
        files = os.listdir(in_tile_path)
        files.sort()
        for file in files:
            dirs.append(os.path.join(in_tile_path, file))
            filenames.append(os.path.join(out_tile_path, file[:-4]+'.tfrecords'))
    all_paths = zip(dirs, filenames)
    
    cpus = mp.cpu_count()
    pool = mp.Pool(cpus)
    func = partial(translate_NPZ, cpus, dataformat)
    pool.map(func, all_paths)
    pool.close()

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="Generate TFrecords for a folder with a EarthNet dataset NPZ file")
    parser.add_argument('--inpath', type = str, default = "data/datasets/release/train/", metavar = '/PATH/TO/CUBE/NPZ/', help='Path to load .npz files from')
    parser.add_argument('--outpath', type = str, default = "data/tf_dataset/train/", metavar = 'PATH/TO/OUTPUT/TFRECORDS/', help ='Path to output .tfrecords files to')
    parser.add_argument('--dataformat', type = str, default = "v1", help ="tfrecord format: 'v1' has all channels together 'v2' has colors/predictors/mask separated")
    args = parser.parse_args()
    
    make_tfrecords(split_path=args.inpath, out_path=args.outpath, dataformat=args.dataformat)
