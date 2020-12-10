import subprocess
import yaml
import os
import sys

from options.base_options import BaseOptions
from earthnet.parallel_score import EarthNetScore
from utils.results_viz import EvalPlotter
'''
Main entry to launch training, testing and evaluation on the EarthNet2021 
Model Intercomparison Project.

run.py maps the arguments given to parse and the experimental settings
into the corresponding submodule in src/models/. The mapping for each model
is defined by the configuration file in configs/model.yml

If mode is 'evaluate' it runs the evaluation pipeline straight from the
data/outputs directory.

The mode 'plot' only works after at least one model has been evaluated.
If the flag 'animations' is used when plotting, it will also output 
visualizations for predictions with performance falling at quantiles 
[0,0.15,0.3,0.5,0.7,0.85,1].
'''

#parse arguments
opt = BaseOptions().parse(save=True)

if opt.mode in ['train','test']:
    
    #load submodule configuration file
    config_yml = os.path.join('configs',opt.model_name[0]+'.yml')
    with open(config_yml) as config_file:
        config = yaml.load(config_file, Loader=yaml.FullLoader)

    #entry_point is the python script that will be called by subprocess. it must be 
    #defined in config.yml with full path src/models/modelname/ENTRY_POINT.PY
    entry_point = config['entry_point'][opt.mode]

    #cuda devices to be used
    if opt.gpu_ids is not None:
        cuda_dev = 'export CUDA_VISIBLE_DEVICES={};'.format(*opt.gpu_ids)

    #define python interpreter. Useful if an specific conda environment is needed 
    #for the submodule
    if config['conda_env'] == 'Base':
        interpreter = 'python '
    else:
        interpreter = '/opt/conda/envs/{}/bin/python '.format(config['conda_env'])

    #arguments to be given to the submodule entry_point.py. Maps from opt to args 
    #according to config.yml
    args = []
    for arg in config['mapped_args_'+opt.mode]:
        try:
            value = str(getattr(opt, config['mapped_args_'+opt.mode][arg]))
        except:
            print('run.py was not given the argument needed to map --{0} into "{1}". Mapping of --{0} skipped.'.format(arg, entry_point))
            continue
        argument = '--' + arg
        if value is 'True':
            args.append(argument)
        elif value is 'False':
            pass
        else:
            args += argument, value
    try:
        for arg in config['fixed_args']:
            args.append('--' + arg)
            args.append(str(config['fixed_args'][arg]))
    except:
        print('No fixed arguments provided on {}'.format(config_yml))
        
    #subprocess is given the cuda_devices, the python interpreter, the script.py
    #(entry_point) and the train/test script arguments.
    sep = ' '
    cmd = sep.join([cuda_dev,interpreter,entry_point,*args])
    print('------------ Run command -------------')
    print(cmd)
    print('---------------- End -----------------')
    subprocess.call(cmd, shell=True)

elif opt.mode == 'evaluate':
    '''
    Evaluates results using src/evaluation/parallel_score.py
    Loops over the lists of model_names and experiment_names given to run.py.
    Saves results to results directory.
    '''
    
    #If test set is split into context/targets use subdirectory targets for GT
    if 'split' in opt.split_name: 
        targ_dir = os.path.join(opt.dataroot,opt.split_name,'target')
    else:
        targ_dir = os.path.join(opt.dataroot,opt.split_name)
    
    for i, model_exp in enumerate(zip(opt.model_name, opt.experiment_name)):
        model, experiment = model_exp
        m_e = os.path.join(model, experiment)
        print("Model/Experiment ({0}) to evaluate is {1}".format(i,m_e))
        
        save_dir = os.path.join(opt.evalpath,'logs',opt.split_name)
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
            
        data_output_file = os.path.join(save_dir, model, 'data', m_e.replace('/', '_')+'.json')   
        ens_output_file = os.path.join(save_dir, model, 'ens', m_e.replace('/', '_')+'.json')
        pred_dir = os.path.join(opt.outpath, m_e, opt.split_name)
        
        EarthNetScore.get_ENS(pred_dir, targ_dir, data_output_file = data_output_file, ens_output_file = ens_output_file)

elif opt.mode == 'plot':
    '''
    Plots density plots for every submetric and ENS for:
     -ablations (performance across different experiments)
     -frames (performance across time steps)
     -generalization (performance across different test sets)
     -spatial (performance across different tiles)
     -models (performance across different model/experiments)
    
    Should use the functions in src.evaluation.viz
    '''
    plotter = EvalPlotter(opt.evalpath, opt.dataroot, opt.outpath)
    plotter.plot_all()
    if opt.animations:
        plotter.plot_animations_percentile()
