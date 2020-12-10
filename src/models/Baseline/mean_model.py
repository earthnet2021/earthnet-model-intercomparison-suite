import numpy as np
import warnings

class ArithmeticMeanModel():
    def __init__(self, context_length=10, sequence_length=None, num_cpus=1):
        """
        Baseline spatio-temporal forecasting (STF) model.

        Non-trainable STF model. Predicts the arithmetic mean of context 
        multispectral values per pixel, and projects the same constant 
        value into future frames. It does not make use of weather or 
        topological predictors.
        
        Can be used as a template for models using Numpy as base library.

        Params
        ------
        input_data : NPZ 
            A test .NPZ datacube from EarthNet dataset.
                
        context_length : int
            Number of frames used for context. The average value of these 
            is projected into future frames.
                
        sequence_lenght : int
            Number of frames of the output datacube. If None, the lenght
            will default to that of the input datacube.
                
        num_cpus : int
            Number of cpus for multiprocessing.
        
        """
        
        self.context_length = context_length
        self.sequence_length = sequence_length
        
    def predict(self, input_data, no_data_channel):
        """

        Params
        ------
        input_data : NPZ 
            A test .NPZ datacube from EarthNet dataset.
        
        """
        #Sequence lengths
        if self.sequence_length is None:
            self.sequence_length = input_data['highresdynamic'].shape[3]
        
        assert self.context_length <= self.sequence_length, (
                "Context length must be smaller than sequence length"+
                "But context is {0} and sequence is {1}".format(self.context_length,self.sequence_length))
                
        predict_length = self.sequence_length - self.context_length
        
        # Extract conext R G B nIR (channels 0:4) for t_0:t_context
        context = input_data['highresdynamic'][:,:,:4,:self.context_length]
        
        # Mask RGB nIR with NaN whenver the No data auxiliary layer is True
        # These are either clouds, shadows or other artifacts on the images
        no_data = input_data['highresdynamic'][:,:,[no_data_channel],:self.context_length]
        context[np.repeat(no_data,4,2)==True] = np.nan
        
        #Set up the pred array
        width, height, channels, _ = context.shape
        pred = np.zeros([width, height, channels, predict_length])
        
        # Compute pixel means during context. Mean over time axis(3)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=RuntimeWarning)
            values = np.nanmean(context, 3, keepdims=True)
        
        # Fill in the remaining NaNs (these will ocurr only when a pixel is
        # hidden for the whole context_lenght). Mean over spatial axes 0,1
        inds = np.where(np.isnan(values))
        values[inds] = np.nanmean(values)
        
        #Repeat the mean values across all times for predict_length
        pred = np.repeat(values, predict_length, 3)
        
        return pred