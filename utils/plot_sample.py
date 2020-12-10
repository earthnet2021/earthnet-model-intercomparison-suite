import argparse
import numpy as np
import matplotlib
from matplotlib import pyplot as plt
import imageio
import os
import shutil
import multiprocessing as mp
from functools import partial
from tqdm import tqdm

def plot_tile(name, filepath, predpath, outpath, save_dir, dpi=200, brightness_factor=3, cpus=1, scores_text=None, pred=False, t=0):
    """Plots a single frame from a .npz sample of the EarthNet dataset.

    Params
    ------
    load_dir : int
        Sample directory
        
    dpi : int
        Resolution as dots per inch
        
    t : int
        Time of the temporal series to plot
        
    name : string
        Sample name. Used to find the sample in the directory 
        and plot text into the fig.
        
    brightness_factor : float
        Scales RGB images to increase values.
        
    cpus : int
        Used only to display progress on progress bar correctly 
        when multiprocessing.

    Returns
    -------
    This function does not return. It saves the figure to the 
    plotting directory.

    """

    #Load sample
    sample = np.load(filepath)
    
    if pred:
        pred_sample = np.load(predpath)
        pred_length = pred_sample['arr_0'].shape[3]
    
    #Transform 0-1 float variables E-Obs units of measuremnts.
    mesodynamic = sample['mesodynamic']
    mesodynamic[:,:,0,:] = 50 * sample['mesodynamic'][:,:,0,:]
    mesodynamic[:,:,1,:] = 200 * sample['mesodynamic'][:,:,1,:] + 900
    mesodynamic[:,:,2:,:] = 50 * ( 2 * sample['mesodynamic'][:,:,2:,:] - 1)
    highresstatic = 2000 * (2 * sample['highresstatic'] -1)
    mesostatic = 2000 * (2 * sample['mesostatic'] -1)
    
    #Create subplot
    fig = plt.figure(figsize=(10, 12), dpi=dpi)
    widths = [1, 1, 1]
    heights = [1.2, 1, 1, 1]
    spec = fig.add_gridspec(ncols=3, nrows=4, width_ratios=widths, height_ratios=heights)

    
    def subplot_tile(array, title, num, cmap='nipy_spectral', colorbar = False, cmin=None, cmax=None, center=False):
        #For RGB
        if array.shape[2] > 2:
            array = array * brightness_factor
            array = np.where(array>1,1,array)
        
        #For double channel (Only Cloud cover)
        if array.shape[2] == 2:
            ax = fig.add_subplot(spec[num])
            plt.title(title, fontsize = 13)
            plt.axis('auto')
            plot = plt.imshow(array[:,:,0].astype(np.float))
            plot.axes.get_xaxis().set_visible(False)
            plot.axes.get_yaxis().set_visible(False)
            plt.clim(cmin, cmax)
            plt.colorbar(fraction=0.046, pad=0.04)
            plot.set_cmap(cmap)
            plot2 = plt.imshow(array[:,:,1].astype(np.float), cmap=plt.cm.Purples, alpha=.2)
            plt.clim(0, 1)
            return

        ax = fig.add_subplot(spec[num])
        plt.title(title, fontsize = 13)
        plt.axis('auto')
        plot = plt.imshow(array.astype(np.float))
        plot.axes.get_xaxis().set_visible(False)
        plot.axes.get_yaxis().set_visible(False)
        
        if cmin is not None:
            plt.clim(cmin, cmax)
        if colorbar:
            plt.colorbar(fraction=0.046, pad=0.04)            
        plot.set_cmap(cmap)
        if center:
            cpix = np.zeros_like(array)
            cpix[41,41] = 1
            plot2 = plt.imshow(cpix.astype(np.float), cmap=plt.cm.Greys, alpha=.2)
            ax.text(0.5,5, str(np.round(array[41,41].astype(np.float),2)))
            
    
    #Unpack channels
    #High Res
    top_label = 'High-resolution multispectral observations'
    
    t_fivey = int((t-4)/5)
    if t_fivey < 0: t_fivey = 0
        
    sequence_length = sample['highresdynamic'].shape[3]
    blue, green, red, nir,_,_,_ = np.split(sample['highresdynamic'][:,:,:,t_fivey], 7, axis=2)
    
    if pred:
        if t_fivey>(sequence_length-pred_length):
            blue, green, red, nir = np.split(pred_sample['arr_0'][:,:,:,t_fivey-(sequence_length-pred_length)], 4, axis=2)
            top_label = 'High-resolution multispectral predictions'
    
    _, _, _, _, cld, scl, bin_cld = np.split(sample['highresdynamic'][:,:,:,t_fivey], 7, axis=2)
    hr_dem = highresstatic
    
    #Multichannel
    rgb = np.dstack((red,green,blue))
    fci = np.dstack((nir,red,green))
    ndvi = (nir - red)*1.0/(nir+red)
    cld = np.dstack((cld,bin_cld))
    
    #Mesoscale
    rr, pp, tg, tn, tx = np.split(mesodynamic[:,:,:,t], 5, axis=2)
    meso_dem = mesostatic
    #Extract mesoscale min-max for plotting
    rr_min = mesodynamic[:,:,0,:].min()
    pp_min = mesodynamic[:,:,1,:].min()
    tn_min = mesodynamic[:,:,3,:].min()
    rr_max = mesodynamic[:,:,0,:].max()
    pp_max = mesodynamic[:,:,1,:].max()
    tx_max = mesodynamic[:,:,4,:].max()
    
    #Lists of layers, plot titles, color maps and colorbar.
    layers = (rgb, fci, ndvi, cld, scl, hr_dem, pp, rr, meso_dem, tn, tx, tg)
    titles = ('Natural color','False color infrared', 'NDVI', 'Cloud cover', 'Scene classification', 'HR Elevation',
             'Pressure', 'Rainfall', 'Meso Elevation', 'Min temperature', 'Max temperature', 'Mean temperature')
    cmaps = (None, None, 'nipy_spectral', 'YlOrBr', 'Set1', 'terrain',
            'rainbow','Blues','terrain','coolwarm','coolwarm','coolwarm')
    colorbar = (False, False, False, True, True, True, True, True, True, False, False, True)
    mins = (None, None, 0, 0, 0, None, pp_min, rr_min, None, tn_min, tn_min, tn_min)
    maxes = (None, None, 1, 100, 10, None, pp_max, rr_max/2, None, tx_max, tx_max, tx_max)
    center = (False, False, False, False, False, False, True, True, True, True, True, True)
    
    #Plotting loop
    for i, layer in enumerate(layers):
        subplot_tile(layer, titles[i], i, cmaps[i], colorbar[i], mins[i], maxes[i], center[i])
    plt.tight_layout()
    
    #Plot text
    plt.figtext(0.038, 0.005, 'Sample '+name[6:-4])
    plt.figtext(0.9, 0.005, 't = {}'.format(t))
    plt.figtext(0.038, 0.715, 'Auxiliary layers')
    plt.figtext(0.675, 0.715, 'High-resolution predictors')
    plt.figtext(0.038, 0.475, 'Mesoscale predictors')
    plt.figtext(0.019, 0.991, top_label)
    
    if scores_text:
        plt.figtext(0.359, 0.991, scores_text)
        
    
    #Save and close
    fig.savefig(outpath+'/{}.png'.format(str(t).zfill(4)))
    plt.close()
    
    try:
        pbar.update(cpus)
    except:
        pass

def plot_video(name, load_dir, pred_dir, save_dir, frames, dpi=300, gif=False, mp4=True, brightness_factor=3, keep_pngs=False, crf=0, frame_rate=12, scores_text=None, pred=False):
    """Creates video frame from a .npz sample of the EarthNet dataset.

    Params
    ------
    name : string
        Sample name. Used to find the sample in the directory
        
    load_dir : string
        Path to load samples from
        
    save_dir : string
        Path to save plots to
        
    dpi : int
        Resolution as dots per inch.
        
    frames : int
        Number of frames to plot starting at frame 0.
        
    brightness_factor : float
        Scales RGB images to increase values
    
    keep_png: bool
        Each frame is plotted into a .png and saved on disk. If 
        keep_png is True, these files are kept. If false they
        are deleted.

    Returns
    -------
    This function does not return. It saves a .mp4 in the 
    plotting directory.
    
    """
    folder = name[:-4]
    outpath = os.path.join(save_dir,folder)
    if not os.path.exists(outpath):
        os.mkdir(outpath)
        
    #Parallel plotting of frames
    cpus = mp.cpu_count()
    pool = mp.Pool(cpus)
    func = partial(plot_tile, name, load_dir, pred_dir, outpath, save_dir, dpi, brightness_factor, cpus, scores_text, pred)
    pool.map(func, range(frames))
    pool.close()
    
    #GIF and Video creation (requires ffmpeg)
    if gif:
        filespath = os.path.join(save_dir, name[:-4])
        filenames = os.listdir(filespath)
        images = []
        for filename in filenames:
            filepath = os.path.join(save_dir,name[:-4],filename)
            images.append(imageio.imread(filepath))
        outpath = os.path.join(save_dir, name[:-4]+'.gif')
        imageio.mimsave(outpath, images)
        
    if mp4:
        prefix = ''
        if pred: prefix = 'pred'
        command = ('ffmpeg -r '+
                   str(frame_rate) + ' -i ' +
                   save_dir +
                   name[:-4] + '/%04d.png -vcodec libx264 -crf ' +
                   str(crf) + ' -y ' +
                   save_dir + '/' + prefix +
                   name[:-4] + '.mp4')
        print(command)
        os.system(command)
    
    if not keep_pngs:
        shutil.rmtree(os.path.join(save_dir,name[:-4]))

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="Generate visualizations for a cube NPZ file")
    parser.add_argument('--datapath', type = str, default = "data/datasets/release/iid_test", metavar = '/PATH/TO/CUBE/', help='Path to load files from')
    parser.add_argument('--predpath', type = str, default = "data/outputs/Baseline/mean/iid_test", metavar = '/PATH/TO/CUBE/', help='Path to predictions files from')
    parser.add_argument('--tilename', type = str, default = "29SND", metavar = '/PATH/TO/CUBE/', help='name of the tile')
    parser.add_argument('--filename', type = str, default = "29SND_2017-06-20_2017-11-16_2105_2233_2489_2617_16_96_19_99.npz", metavar = '/PATH/TO/CUBE/', help='name of the datacube')
    parser.add_argument('--outpath', type = str, default = "data/plots/", metavar = 'PATH/TO/OUTPUT/TO/', help ='Path to output files to')
    parser.add_argument('--pred', action='store_true', default=False, help='Plots prediction from .NPZ if full_array was True during test')
    parser.add_argument('--video', action='store_true', default=False, help='Creates a .mp4 video')
    parser.add_argument('--gif', action='store_true', default=False, help='Creates a .gif animation')
    parser.add_argument('--image', action='store_true', default=False, help='Creates a .png with a single frame')
    parser.add_argument('--keep_pngs', action='store_true', default=False, help='Keeps the single frame .png files used to create the video')
    parser.add_argument('--frame', type=int, default=150, help='# of frames for the video or frame to plot')
    parser.add_argument('--brightness', type=float, default=3, help='Multiplier for values of RGB images. Satellite imagery tends to be dark')
    parser.add_argument('--dpi', type=float, default=300, help='Resolution of the plots in dots per inch')
    parser.add_argument('--frame_rate', type=int, default=12, help='Framerate of the video')
    parser.add_argument('--crf', type=int, default=22, help='Constant Rate Factor determines video quality. Low values for greater visual quality')

    args = parser.parse_args()
    
    args.filepath = os.path.join(args.datapath, args.tilename, args.filename)
    args.predpath = os.path.join(args.predpath, args.tilename, args.filename)
    #Creates a sequence vizualization as .MP4
    if args.video:
        pbar = tqdm(total=args.frame)
        plot_video(args.filename, 
                   args.filepath,
                   args.predpath,
                   args.outpath,
                   args.frame,
                   args.dpi,
                   gif = args.gif,
                   brightness_factor=args.brightness, 
                   keep_pngs=args.keep_pngs,
                   crf=args.crf,
                   frame_rate=args.frame_rate,
                   pred=args.pred)

    #Creates a single frame visualization as .PNG
    if args.image:
        plot_tile(args.filename,
                  args.filepath,
                  args.predpath,
                  args.outpath,
                  args.dpi,
                  args.brightness,
                  args.frame,
                  args.pred)
