---
layout: single
title: EarthNet2021 Toolkit API - EarthNetScore
permalink: /en21/tk-earthnetscore/
toc: true
toc_stickly: true
sidebar:
  title: "EarthNet2021"
  nav: en21
---

## Calculating EarthNetScore

EarthNetScore is implemented leveraging multiprocessing. With a class method, it can be computed over (possibly multiple) predictions of one test set.

Save your predictions for one test set in one folder in one of the following ways:
`{pred_dir/tile/cubename.npz, pred_dir/tile/ensemblenumber_cubename.npz}`
Then use the Path/To/Download/To/TestSet as the targets.

Then use the EarthNetScore:

```python
import earthnet as en
en.EarthNetScore.get_ENS(Path/to/predictions, Path/to/targets, data_output_file = Path/to/data.json, ens_output_file = Path/to/ens.json)
```

You will find the computed EarthNetScore in `Path/to/ens.json`.

**ProTip:** You can find further terms computed, such as subscores per prediction, in `Path/to/data.json`.
{: .notice--info}


## API

### earthnet.parallel_score module

EarthNetScore in parallel.


### class earthnet.parallel_score.CubeCalculator()
Bases: `object`

Loads single cube and calculates subscores for EarthNetScore

Example:

```python
>>> scores = CubeCalculator.get_scores({"pred_filepath": Path/to/pred.npz, "targ_filepath": Path/to/targ.npz})
```


#### classmethod EMD(preds: numpy.ndarray, targs: numpy.ndarray, masks: numpy.ndarray)
Earth mover distance score

The earth mover distance (w1 metric) is computed between target and predicted pixelwise NDVI timeseries value distributions. For the target distributions, only non-masked values are considered. Scaled by a scaling factor such that a distance the size of a 99.7% confidence interval of the variance of the pixelwise centered NDVI timeseries is scaled to 0.9 (such that the ols-score becomes 0.1). The emd-score is 1-mean(emd), it is scaled from 0 (worst) to 1 (best).

Args:

    preds (np.ndarray): NDVI Predictions, shape h,w,1,t
    targs (np.ndarray): NDVI Targets, shape h,w,1,t
    masks (np.ndarray): NDVI Masks, shape h,w,1,t, 1 if non-masked, else 0

Returns:

    Tuple[float, dict]: emd-score, debugging information


#### static MAD(preds: numpy.ndarray, targs: numpy.ndarray, masks: numpy.ndarray)
Median absolute deviation score

Median absolute deviation between non-masked target and predicted pixels. Scaled by a scaling factor such that a distance the size of a 99.7% confidence interval of the variance of the pixelwise centered timeseries is scaled to 0.9 (such that the mad-score becomes 0.1). The mad-score is 1-MAD, it is scaled from 0 (worst) to 1 (best).

Args:

    preds (np.ndarray): Predictions, shape h,w,c,t
    targs (np.ndarray): Targets, shape h,w,c,t
    masks (np.ndarray): Masks, shape h,w,c,t, 1 if non-masked, else 0

Returns:

    Tuple[float, dict]: mad-score, debugging information


#### static OLS(preds: numpy.ndarray, targs: numpy.ndarray, masks: numpy.ndarray)
Ordinary least squares slope deviation score

Mean absolute difference between ordinary least squares slopes of target and predicted pixelwise NDVI timeseries. Target slopes are calculated over non-masked values. Predicted slopes are calculated for all values between the first and last non-masked value of a given timeseries. Scaled by a scaling factor such that a distance the size of a 99.7% confidence interval of the variance of the pixelwise centered NDVI timeseries is scaled to 0.9 (such that the ols-score becomes 0.1). If the timeseries is longer than 40 steps, it is split up into parts of length 20. The ols-score is 1-mean(abs(b_targ - b_pred)), it is scaled from 0 (worst) to 1 (best).

Args:

    preds (np.ndarray): NDVI Predictions, shape h,w,1,t
    targs (np.ndarray): NDVI Targets, shape h,w,1,t
    masks (np.ndarray): NDVI Masks, shape h,w,1,t, 1 if non-masked, else 0

Returns:

    Tuple[float, dict]: ols-score, debugging information


#### static SSIM(preds: numpy.ndarray, targs: numpy.ndarray, masks: numpy.ndarray)
Structural similarity index score

Structural similarity between predicted and target cube computed for all channels and frames individually if the given target is less than 30% masked. Scaled by a scaling factor such that a mean SSIM of 0.8 is scaled to a ssim-score of 0.1. The ssim-score is mean(ssim), it is scaled from 0 (worst) to 1 (best).

Args:

    preds (np.ndarray): Predictions, shape h,w,c,t
    targs (np.ndarray): Targets, shape h,w,c,t
    masks (np.ndarray): Masks, shape h,w,c,t, 1 if non-masked, else 0

Returns:

    Tuple[float, dict]: ssim-score, debugging information


#### static compute_w1(datarow: numpy.ndarray)
Computing w1 distance for np.apply_along_axis

Args:

    datarow (np.ndarray): 1-dimensional array that can be split into three parts of equal size, these are in order: predictions, targets and masks for a single pixel and channel through time.

Returns:

    Union[np.ndarray, None]: w1 distance between prediction and target, if not completely masked, else None.


#### classmethod get_scores(filepaths: dict)
Get all subscores for a given cube

Args:

    filepaths (dict): Has keys “pred_filepath”, “targ_filepath” with respective paths.

Returns:

    dict: subscores and debugging info for the input cube


#### static load_file(pred_filepath: pathlib.Path, targ_filepath: pathlib.Path)
Load a single target cube and a matching prediction

Args:

    pred_filepath (Path): Path to predicted cube
    targ_filepath (Path): Path to target cube

Returns:

    Sequence[np.ndarray]: preds, targs, masks, ndvi_preds, ndvi_targs, ndvi_masks


### class earthnet.parallel_score.EarthNetScore(pred_dir: str, targ_dir: str)
Bases: `object`

EarthNetScore class, fast computation using multiprocessing

Example:

> Direct computation
> >>> EarthNetScore.get_ENS(Path/to/predictions, Path/to/targets, data_output_file = Path/to/data.json, ens_output_file = Path/to/ens.json)

> More control (for further plotting)
> >>> ENS = EarthNetScore(Path/to/predictions, Path/to/targets)
> >>> data = ENS.compute_scores()
> >>> ens = ENS.summarize()


#### \__init__(pred_dir: str, targ_dir: str)
Initialize EarthNetScore

Args:

    pred_dir (str): Directory with predictions, format is one of {pred_dir/tile/cubename.npz, pred_dir/tile/experiment_cubename.npz}
    targ_dir (str): Directory with targets, format is one of {targ_dir/target/tile/target_cubename.npz, targ_dir/target/tile/cubename.npz, targ_dir/tile/target_cubename.npz, targ_dir/tile/cubename.npz}


#### compute_scores(n_workers: Optional[int] = -1)
Compute subscores for all cubepaths

Args:

    n_workers (Optional[int], optional): Number of workers, if -1 uses all CPUs, if 0 uses no multiprocessing. Defaults to -1.

Returns:

    dict: data of format {cubename: score_dict}


#### classmethod get_ENS(pred_dir: str, targ_dir: str, n_workers: Optional[int] = -1, data_output_file: Optional[str] = None, ens_output_file: Optional[str] = None)
Method to directly compute EarthNetScore

Args:

    pred_dir (str): Directory with predictions, format is one of {pred_dir/tile/cubename.npz, pred_dir/tile/experiment_cubename.npz}
    targ_dir (str): Directory with targets, format is one of {targ_dir/target/tile/target_cubename.npz, targ_dir/target/tile/cubename.npz, targ_dir/tile/target_cubename.npz, targ_dir/tile/cubename.npz}
    n_workers (Optional[int], optional): Number of workers, if -1 uses all CPUs, if 0 uses no multiprocessing. Defaults to -1.
    data_output_file (Optional[str], optional): Output filepath for subscores and debugging information, recommended to end with .json. Defaults to None.
    ens_output_file (Optional[str], optional): Output filepath for EarthNetScore, recommended to end with .json. Defaults to None.


#### get_paths(pred_dir: str, targ_dir: str)
Match paths of target cubes with predicted cubes

Each target cube gets 1 or more predicted cubes.

Args:

    pred_dir (str): Directory with predictions, format is one of {pred_dir/tile/cubename.npz, pred_dir/tile/experiment_cubename.npz}
    targ_dir (str): Directory with targets, format is one of {targ_dir/target/tile/target_cubename.npz, targ_dir/target/tile/cubename.npz, targ_dir/tile/target_cubename.npz, targ_dir/tile/cubename.npz}


#### save_scores(output_file: str)
Save all subscores and debugging info as JSON

Args:

    output_file (str): Output filepath, recommended to end with .json


#### summarize(output_file: Optional[str] = None)
Calculate EarthNetScore from subscores and optionally save to file as JSON

Args:

    output_file (Optional[str], optional): If not None, saves EarthNetScore to this path, recommended to end with .json. Defaults to None.

Returns:

    Tuple[float, float, float, float, float]: ens, mad, ols, emd, ssim
