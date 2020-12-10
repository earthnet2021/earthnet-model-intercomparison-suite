import argparse
import os

class BaseOptions():
    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.initialized = False

    def initialize(self):
        # run usage
        self.parser.add_argument('--mode', type = str, default = "test", choices=['train', 'test', 'evaluate', 'plot'], help='Select a mode')
        self.parser.add_argument('--animations', action='store_true', help='If mode is plot, will also save animations')
        
        # for setting inputs/outputs
        self.parser.add_argument('--dataroot', type = str, default = "data/datasets/release/", metavar = '/PATH/TO/CUBE/', help='Path to load files from')
        self.parser.add_argument('--outpath', type = str, default = "data/outputs/", metavar = 'PATH/TO/OUTPUT/TO/', help ='Path to output files to')
        self.parser.add_argument('--evalpath', type = str, default = "data/results/", metavar = 'PATH/TO/EVALUATE/TO/', help ='Path to output evaluations to')
        
        # for model specifics
        self.parser.add_argument('--model_name', type = str, nargs='+', default = ['Baseline'], help ='Name of the submodule [Baseline,Tf_template,(...)]')
        self.parser.add_argument('--submodel', type = str, default = 'mean', help ='Name of the model in the submodule (in case there are). e.g. [mean,linear] for Baseline submodule')
        self.parser.add_argument("--dataset", type=str, help="dataset class name [used by Arcon]")
        self.parser.add_argument('--experiment_name', type = str, nargs='+', default = ['mean'], metavar = 'EXPERIMENT_NAME', help ='Name of the experiment')
        self.parser.add_argument('--split_name', type = str, default = 'iid_test', metavar = 'SPLIT_NAME', help ='Name of the dataset split [iid_test,ood_test,seasonal_test,extreme_test]')
        self.parser.add_argument('--checkpoint', type = str, default = 'data/temp/checkpoint/', help ='Path to load/save checkpoints')
        self.parser.add_argument('--experiment_settings', type = str, metavar = 'EXPERIMENT_SETTINGS.JSON OR DIRECTORY', help ='Filename/directory of the experiment settings')
        self.parser.add_argument('--context_length', type = int, default = 10, help ='Number of context frames')
        self.parser.add_argument('--prediction_length', type = int, default = 20, help ='Number of context frames')

        # for training
        self.parser.add_argument("--resume", action='store_true', help='Resume from lastest checkpoint in checkpoint.')
        self.parser.add_argument('--gpu_ids', type=str, default='0', help='Gpu ids: e.g. 0  0,1,2, 0,2. use -1 for CPU')
        self.parser.add_argument('--batch_size', type=int, default=1, help='Input batch size')
        
        # for generating
        self.parser.add_argument("--num_stochastic_samples", type=int, default=1)

        self.initialized = True

    def parse(self, save=True):
        if not self.initialized:
            self.initialize()
        self.opt = self.parser.parse_args()
        if self.opt.mode == 'evaluate':
            save=False
            
        #Compose full directories
        self.opt.data_expr_dir = os.path.join(self.opt.dataroot, self.opt.split_name)
        self.opt.check_expr_dir = os.path.join(self.opt.checkpoint, self.opt.model_name[0], self.opt.experiment_name[0])
        self.opt.out_expr_dir = os.path.join(self.opt.outpath, self.opt.model_name[0], self.opt.experiment_name[0],self.opt.split_name)
        self.opt.eval_expr_dir = os.path.join(self.opt.evalpath, self.opt.model_name[0], self.opt.experiment_name[0],self.opt.split_name)
        if self.opt.experiment_settings:
            self.opt.set_expr_dir = os.path.join('experiments', self.opt.model_name[0], self.opt.experiment_settings)
        
        str_ids = self.opt.gpu_ids.split(',')
        self.opt.gpu_ids = []
        for str_id in str_ids:
            id = int(str_id)
            if id >= 0:
                self.opt.gpu_ids.append(id)

        args = vars(self.opt)

        print('------------ Options -------------')
        for k, v in sorted(args.items()):
            print('%s: %s' % (str(k), str(v)))
        print('-------------- End ----------------')

        #save to the disk
        if self.opt.mode == 'train':
            self.opt.expr_dir = self.opt.check_expr_dir
        elif self.opt.mode == 'test':
            self.opt.expr_dir = self.opt.out_expr_dir
        elif self.opt.mode == 'evaluate':
            self.opt.expr_dir = self.opt.eval_expr_dir
        elif self.opt.mode == 'plot':
            self.opt.expr_dir = os.path.join(self.opt.evalpath, 'figures')
        
        if save and not self.opt.resume:
            if not os.path.exists(self.opt.expr_dir):
                os.makedirs(self.opt.expr_dir)
            file_name = os.path.join(self.opt.expr_dir, 'opt.txt')
            with open(file_name, 'wt') as opt_file:
                opt_file.write('------------ Options -------------\n')
                for k, v in sorted(args.items()):
                    opt_file.write('%s: %s\n' % (str(k), str(v)))
                opt_file.write('-------------- End ----------------\n')
        return self.opt
