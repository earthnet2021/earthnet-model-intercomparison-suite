import glob
import os
import numpy as np
import random
import json
import pandas as pd
from scipy import stats
import seaborn as sns
from .plot_sample import plot_video


class EvalPlotter:
    def __init__(self, results_dir, data_dir, output_dir):
        """ 
        Loads score data from .json, creates a panda dataframes and plots 
        results for the different models and test sets.
        
        Params
        ------
        results_dir : string
            directory in which to read evaluation results and save plots

        """
        self.results_dir = results_dir
        self.data_dir = data_dir
        self.output_dir = output_dir
        self.logs_dir = os.path.join(results_dir,'logs')
        self.plots_dir = os.path.join(results_dir,'figures')
        self.pandas_df = None
    
    def create_pandas_df(self, save=False):
            """
            Generates two tidy pandas dataframe from the dict of dict with
            scores. Makes all sort of plotting easy peasy.
            
            pandas_df:
            Independent variables: split, tile, sample, model, experiment, metric, stoch
            Dependent variables: score
            
            frames_df (only SSIM):
            Independent variables: split, tile, sample, model, experiment, metric, stoch, frame, channel
            Dependent variables: score
            """
            def compute_ens(scores):
                """
                Computes harmonic mean of a list of scores
                """
                scores = list(filter(None, scores))
                if len(scores) == 0:
                    return None
                else:
                    return min(1,len(scores)/sum([1/(s+1e-8) for s in scores]))
            
            rows = []
            frames = []
            for split_name in os.listdir(self.logs_dir):
                split_path = os.path.join(self.logs_dir, split_name)
                for model in os.listdir(split_path):
                    data_path = os.path.join(split_path, model, 'data')
                    print(data_path)
                    for experiment_json in os.listdir(data_path):
                        experiment = experiment_json[:-5]
                        with open(os.path.join(data_path, experiment_json), 'r') as json_df:
                            dict_df = json.load(json_df)
                        filenames = list(dict_df.keys())
                        for filename in filenames:
                            tile = filename[:5]
                            sample = filename[:-4]
                            stochs = list(dict_df[filename])
                            for num_stoch, stoch in enumerate(stochs):
                                metrics = list(stoch.keys())
                                metrics.remove('pred_filepath')
                                metrics.remove('targ_filepath')
                                metrics.remove('debug_info')
                                stoch['ENS'] = compute_ens(list(stoch[metric] for metric in metrics))
                                metrics.append('ENS')
                                
                                for metric in metrics:
                                    score = stoch[metric]
                                    rows.append({'split':split_name,
                                                 'tile':tile,
                                                 'sample':sample,
                                                 'model':model,
                                                 'experiment':experiment,
                                                 'stoch':num_stoch,
                                                 'metric':metric,
                                                 'score':score})
                                    
                                    if metric in ['SSIM','MAD']:
                                        frame_scores = stoch['debug_info'][metric]['frames']
                                        channels = ['blue','green','red','infrared']
                                        for frame_num, score in enumerate(frame_scores):
                                            if score == 1000:
                                                score = np.nan
                                            if metric == 'SSIM':
                                                channel = channels[frame_num % 4]
                                                int_frame = int(frame_num / 4)
                                            if metric == 'MAD':
                                                metric == 'MAE' #debug info of MAD returns MAE
                                                channel = 'all'
                                                int_frame = frame_num
                                            frames.append({'split':split_name,
                                                     'tile':tile,
                                                     'sample':sample,
                                                     'model':model,
                                                     'experiment':experiment,
                                                     'stoch':num_stoch,
                                                     'metric':metric,
                                                     'frame':int_frame,
                                                     'channel':channel,
                                                     'score':score})

            self.pandas_df = pd.DataFrame(rows)
            if save:
                self.pandas_df.to_csv(os.path.join(self.results_dir,'eval_data.csv'))
            self.frames_df = pd.DataFrame(frames)
            print("Created tidy evaluation dataframe")
            
    def plot_all(self):
        """ Density plots (violin) for main comparisons:
        - ENS per model ablations
        - 5 metrics per model/experiment
        - Split test performance
        - Performance per model across tiles
        - Basemap per model/experiment
        """
        def set_axis_range(plot):
            #does not seem to be properly changing xlim on the subplots
            #unknown cause
            for (row_val, col_val), ax in plot.axes_dict.items():
                if col_val in ["iid_test","ood_test"]:
                    ax.set_xlim(0,20)
                elif col_val == "extreme_test":
                    ax.set_xlim(0,40)
                elif col_val == "seasonal_test":
                    ax.set_xlim(0,140)
            return plot
        if self.pandas_df == None:
            self.create_pandas_df()
        sns.set()
        ##############################
        ### Models plots
        models_path = os.path.join(self.plots_dir,'models')
        os.makedirs(models_path, exist_ok = True)
        violin = sns.catplot(x="experiment", y="score", col="metric", 
                             row="split", kind="violin", split=True, 
                             data=self.pandas_df,
                             scale="count", inner="quartile", bw=.2, cut=0)
        violin.set(ylim=(0, 1))
        violin.set_xticklabels(rotation=90)
        violin.savefig(os.path.join(models_path, 'all.png'), dpi=300)
        print("Model plots exported")
            
        ##############################
        ### Ablation plots
        for model in self.pandas_df.model.unique():
            ablations_path = os.path.join(self.plots_dir,'ablations')
            os.makedirs(ablations_path, exist_ok = True)
            violin = sns.catplot(x="experiment", y="score", col="metric", 
                                 row="split", kind="violin", split=True, 
                                 data=self.pandas_df[self.pandas_df.model == model], 
                                 scale="count", inner="quartile", bw=.2, cut=0)
            violin.set(ylim=(0, 1))
            violin.set_xticklabels(rotation=90)
            violin.savefig(os.path.join(ablations_path, model+'.png'), dpi=300)
        print("Ablation plots exported")
        
        ##############################
        ### Generalization plots
        for model in self.pandas_df.model.unique():
            generalization_path = os.path.join(self.plots_dir,'generalization')
            if not os.path.exists(generalization_path):
                os.makedirs(generalization_path)
            violin = sns.catplot(x="split", y="score", col="metric", 
                                 row="experiment", kind="violin", split=True, 
                                 data=self.pandas_df[self.pandas_df.model == model], 
                                 scale="count", inner="quartile", bw=.2, cut=0)
            violin.set(ylim=(0, 1))
            violin.set_xticklabels(rotation=90)
            violin.savefig(os.path.join(generalization_path, model+'.png'), dpi=300)
        print("Generalization plots exported")
        
        ##############################
        ### Spatial plots (performance across tiles)
        for model in self.pandas_df.model.unique():
            generalization_path = os.path.join(self.plots_dir,'spatial')
            os.makedirs(generalization_path, exist_ok = True)
            violin = sns.catplot(x="tile", y="score", col="metric", 
                                 row="experiment", kind="violin", split=True, 
                                 data=self.pandas_df[self.pandas_df.model == model], 
                                 scale="count", inner="quartile", bw=.2, cut=0)
            violin.set(ylim=(0, 1))
            violin.set_xticklabels(rotation=90, size=4)
            violin.savefig(os.path.join(generalization_path, model+'.png'), dpi=300)
        print("Spatial plots exported")
        
        ##############################
        ### SSIM plots (performance across time steps)
        self.frames_df.dropna(axis=0, inplace=True)
        frames_path = os.path.join(self.plots_dir,'frames')
        os.makedirs(frames_path, exist_ok = True)
        line = sns.relplot(x="frame", y="score", hue="experiment", style="model", col="split",
                           row="channel", kind="line", data=self.frames_df[self.frames_df.metric == 'SSIM'],
                           facet_kws={'sharex': False, 'sharey': False})
        line = set_axis_range(line)
        line.savefig(os.path.join(frames_path, 'ssim_raw_line.png'), dpi=300)
        
        
        violin = sns.catplot(x="frame", y="score", col="split",
                             row="experiment", kind="violin", data=self.frames_df[self.frames_df.metric == 'SSIM'],
                             sharex=False, sharey=False)
        violin = set_axis_range(violin)
        violin.savefig(os.path.join(frames_path, 'ssim_raw_violin.png'), dpi=300)
        print("Framewise SSIM exported")
        
        ##########
        ### MAE plots (performance across time steps)
        line = sns.relplot(x="frame", y="score", hue="experiment", style="model", col="split",
                           row="channel", kind="line", data=self.frames_df[self.frames_df.metric == 'MAD'],
                           facet_kws={'sharex': False, 'sharey': False})
        line = set_axis_range(line)
        line.savefig(os.path.join(frames_path, 'mae_raw_line.png'), dpi=300)
        
        violin = sns.catplot(x="frame", y="score", col="split",
                             row="experiment", kind="violin", data=self.frames_df[self.frames_df.metric == 'MAD'],
                             sharex=False, sharey=False)
        violin = set_axis_range(violin)
        violin.savefig(os.path.join(frames_path, 'mae_raw_violin.png'), dpi=300)
        print("Framewise MAE exported")
            
        
        #self.pandas_df.experiment.tolist() instead of just "experiment" since matplotli 3.3.1 breaks seaborn scatter plot
        #points = sns.relplot(x="tile", y="score", col="metric", data=self.pandas_df) 
        #points.set(ylim=(0, 1))
        #points.savefig(os.path.join('data/plots/', 'points.png'), dpi=500)
        
    def plot_animations_percentile(self):
        """
        Ranks predicted samples by calculated ENS. Export animations using plot_sample of
        percentiles 0% 15% 30% 50% 70% 85% 100%.
        """
        animation_path = os.path.join(self.results_dir, 'animations')
        if not hasattr(self, 'pandas_df'):
            self.create_pandas_df()
        
        quantiles = [0,0.15,0.3,0.5,0.7,0.85,1]
        for split in self.pandas_df.split.unique():
            if split == 'extreme_test':
                frames = 300
            if split == 'seasonal_test':
                frames = 1050
            elif split in ['iid_test','ood_test']:
                frames = 150
            split_df = self.pandas_df[self.pandas_df.split == split]
            for experiment in split_df.experiment.unique():
                exp_df = split_df[self.pandas_df.experiment == experiment]
                for q in quantiles:
                    ens_df = exp_df[self.pandas_df.metric == 'ENS']
                    df = ens_df[ens_df.score == ens_df.score.quantile(q, interpolation='nearest')]
                    
                    filename = df['sample'].values[0]
                    tilename = df['tile'].values[0]
                    model = df['model'].values[0]
                    exp = experiment.split('_')[1]
                    
                    MAD = exp_df[exp_df['sample']==filename][exp_df.metric == 'MAD']['score'].values[0]
                    OLS = exp_df[exp_df['sample']==filename][exp_df.metric == 'OLS']['score'].values[0]
                    EMD = exp_df[exp_df['sample']==filename][exp_df.metric == 'EMD']['score'].values[0]
                    SSIM = exp_df[exp_df['sample']==filename][exp_df.metric == 'SSIM']['score'].values[0]
                    ENS = exp_df[exp_df['sample']==filename][exp_df.metric == 'ENS']['score'].values[0]
                    scores_text= "MAD: {:.4f} OLS: {:.4f} EMD: {:.4f} SSIM: {:.4f} ENS: {:.4f}".format(MAD,OLS,EMD,SSIM,ENS)
                    
                    
                    filepath = os.path.join(self.data_dir, split, tilename, filename+'.npz')
                    outpath = os.path.join(animation_path, split, model, exp, str(q)+'/')
                    predpath = os.path.join(self.output_dir, model, exp, split, tilename,'*'+filename+'.npz')
                    try:
                        chosenpred = random.choice(glob.glob(predpath))
                    except:
                        print("No samples can be found for path {}".format(predpath))
                        continue

                    os.makedirs(outpath, exist_ok = True)
                    
                    #Plot predictions
                    plot_video(name=filename,
                               load_dir=filepath,
                               pred_dir=chosenpred,
                               save_dir=outpath,
                               frames=frames,
                               crf=22,
                               scores_text=scores_text,
                               pred=True)
                    #Plot groundtruth
                    plot_video(name=filename,
                               load_dir=filepath,
                               pred_dir=chosenpred,
                               save_dir=outpath,
                               frames=frames,
                               crf=22,
                               pred=False)
                    print(df)
