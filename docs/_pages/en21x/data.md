---
layout: single
title: Dataset Specifications
permalink: /en21x/data/
toc: true
sidebar:
  title: "EarthNet2021X"
  nav: en21x
---

## Overview

EarthNet2021x is an updated version of the EarthNet2021 dataset. Improvements are mainly:

- Files are now netCDF (having proper georeferencing)
- Landcover map included
- New cloud mask
- New Scoring with a focus on vegetation modeling
- No more mesoscale weather

It contains the same locations of minicubes that were present in EarthNet2021.

## One Minicube

One Minicube (one sample) of EarthNet2021x contains 20 variables of different dimensions:

- Spatio-temporal:
    - Sentinel 2
        - Bands B02, B03, B04, B8A (blue, green, red, near-infrared)
        - 20m resolution
        - 5-daily (with NaN in between)
        - Variable names `["s2_B02", "s2_B03", "s2_B04", "s2_B8A"]`
    - Sentinel 2 Auxilary information
        - Improved cloud mask (variable name `"s2_mask"`)
        - Scene classification layer SCL (variable name `"s2_SCL"`)
        - Availability indicator (only temporal, variable name `"s2_avail"`)
- Temporal:
    - E-OBS meterology
        - Wind speed `"eobs_fg"` (often missing!)
        - Relative humidity `"eobs_hu"`
        - Rainfall `"eobs_rr"`
        - Sea-level pressure `"eobs_pp"`
        - Shortwave downwelling radiation `"eobs_qq"`
        - Temperature (Daily Avg, Min, Max: `"eobs_tg", "eobs_tn", "eobs_tx"`)
        - daily
- Spatial:
    - Digital Elevation models
        - from NASA, ESA and JAXA
        - Variable names `["nasa_dem", "cop_dem", "alos_dem"]`
        - Resampled to 20m
    - ESA Worldover Landcover map
        - `"esawc_lc"`
    - Geomorpho90m terrain classification
        - `"geom_cls"`

## Computing NDVI

The recommended way for computing the Normalized Difference Vegetation Index (NDVI) is using the Python package `xarray`:

```
import xarray as xr

minicube = xr.open_dataset("path_to_minicube")
nir = minicube.s2_B8A
red = minicube.s2_B04
mask = minicube.s2_mask

ndvi = ((nir - red) / (nir + red + 1e-8)).where(mask == 0, np.NaN)

minicube["s2_ndvi"] = ndvi
```

## Getting Sentinel 2 dates

Sentinel 2 observations are only (at maximum) 5-daily within the minicube. They are on each 5th datum, i.e. there is preceding 4 days of meterological observations before each Sentinel 2 observation.

You may select only dates with Sentinel 2 observations using the Python package `xarray`:

```
import xarray as xr
minicube = xr.open_dataset("path_to_minicube")
minicube_on_sen2_dates = minicube.isel(time = slice(4, None, 5))
```

## Aggregating E-OBS data to 5-daily

You may want to aggregate E-OBS data to 5-daily to match with Sentinel 2 observations. This is possible using the Python package `xarray`:

```
import xarray as xr
minicube = xr.open_dataset("path_to_minicube")
minicube_5daily = minicube.coarsen(time = 5, coord_func = "max").mean()
```

Instead of `mean()`, you may use other aggregation functions such as `min()` or `max()`.


## Folder structure

After downloading EarthNet2021x to your `data_dir`, you will have the following folder structure:
```
data_dir
├── train   			# training set
|  ├── 29SND      # Sentinel 2 tile with samples at lon 29, lat S, subquadrant ND
|  |  ├── 29SND_2017...124.nc 	# First training minicube, name cubename.nc
|  |  └── ...
|  ├── 29SPC      # there is 85 tiles in the train set
|  └── ...      # with 23816 .nc train minicubes in total
├── iid    # main track testing samples (4205)
|     └── ... # same as train, but with test samples
├── ood     # robustness track testing samples (4202)
|     └── ...
├── extreme    # extreme weather testing samples (3972)
|     └── ...
└── seasonal   # seasonal testing samples (3880)
|     └── ...

```