---
layout: single
title: GreenEarthNet Scoring
permalink: /en21x/scoring/
toc: true
toc_stickly: true
sidebar:
  title: "GreenEarthNet"
  nav: en21x
---

## Scoring your predictions

You can score your predictions using the EarthNet toolkit (`pip install earthnet`)

Save your predictions for one test set in one folder in the following way:
`{pred_dir/region/cubename.nc}`
Name your NDVI prediction variable as `"ndvi_pred"`.

Then use the `data_dir/dataset/split` as the targets.

Then compute the normalized NSE over the full dataset:
```
import earthnet as entk
scores = entk.score_over_dataset(Path/to/targets, Path/to/predictions)
print(scores["veg_score"])
```

Alternatively you can score a single minicube:
```
import earthnet as entk
df = entk.normalized_NSE(Path/to/target_minicube, Path/to/prediction_minicube)
print(df.describe())
```

## Vegetation Score

GreenEarthNet uses a vegetation score to benchmark different models.

It is the average [Nash Sutcliffe Model Efficiency](https://en.wikipedia.org/wiki/Nash%E2%80%93Sutcliffe_model_efficiency_coefficient) (sometimes equivalent to the [Coefficient of Determination R^2](https://en.wikipedia.org/wiki/Coefficient_of_determination)) on cloud-free observations of Vegetation Pixels.

More specifically:
1. For each pixel compute the Nash-Sutcliffe Model Efficiency (NSE) at cloud-free observations
2. Rescale this with `1 / (2-nse)` to the range 0-1 for robust averaging
3. Averaging over all natural vegetation pixels (Landcover class Trees, Scrub or Grassland)
4. Scaling back with `2 - 1/mean_nnse` to the range -Inf,1

The Vegetation Score is 1 if the prediction is perfect.
It is 0 if on average predictions are as good as the mean over the target period.
It is negative if on average predictions are worse than the mean of the target period.

In Pseudo-Code it is computed as follows:

```
nse = NSE(targ_ndvi, pred_ndvi).where(targ_ndvi has no clouds)
nnse = 1 / (2-nse)
veg_score = 2 - 1/mean(nnse.where(landcover == Trees, Scrub or Grassland))
```

Models can use a context length for spin-up and are benchmarked over a target length, which is specified for the different test sets (tracks) as follows (same as EarthNet2021):
- IID: 50 days context, 100 days target
- OOD: 50 days context, 100 days target
- Extreme: 100 days context, 200 days target
- Seasonal: 350 days context, 700 days target

Here, five days equal one Sen2 observation.