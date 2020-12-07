#WIP
#TODO
import numpy as np
from sklearn.linear_model import LinearRegression
import pickle
import os

class LinearModel():
    def __init__(self, context_length=10, sequence_length=None, num_cpus=1, checkpoint=None):
        """
        Baseline spatio-temporal forecasting (STF) model.

        Trainable STF model. The linear model is trained using pixel 
        values of the context frames of a single sample. Then it is 
        used to extrapolate for the rest of the time series. It is an
        autoregressive model, it takes previous time-step as predictors
        for the next time. Uses weather and elevation.
        
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
            
        checkpoint : string
            Path to checkpoint .sav file
        
        """
        
        self.context_length = context_length
        self.sequence_length = sequence_length
        
    def predict(self, input_data):
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
        no_data = input_data['highresdynamic'][:,:,[6],:self.context_length]
        context[np.repeat(no_data,4,2)==True] = np.nan
        
        #Set up the pred array
        width, height, channels, _ = context.shape
        pred_flat = np.zeros([width*height*channels, predict_length])
        
        #flatten spatial dimensions
        context_flat = context.reshape(width*height*channels,self.context_length)
        
        X = np.arange(0,self.context_length).reshape(-1,1)
        X_hat = np.arange(self.context_length, self.sequence_length).reshape(-1,1)
        for i in range(width*height*channels):
            lm = LinearRegression()
            Y = np.squeeze(context_flat[i,:])
            X_masked = X[np.logical_not(np.isnan(Y))]
            Y_masked = Y[np.logical_not(np.isnan(Y))]
            try:
                lm.fit(X_masked.astype(np.float),Y_masked.astype(np.float))
                pred_flat[i,:] = lm.predict(X_hat)
            except:
                "Could not fit this one"
        
        pred = pred_flat.reshape(width,height,channels,predict_length)
        
        # Fill in the remaining NaNs (these will ocurr only when a pixel is
        # hidden for the whole context_lenght). Mean over spatial axes 0,1
        inds = np.where(np.isnan(pred))
        pred[inds] = np.nanmean(pred)
        
        return pred.astype(np.float16)
