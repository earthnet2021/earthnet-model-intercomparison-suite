---
layout: single
title: Specifications
permalink: /docs/ds-specifications/
last_modified_at: 2020-11-29
toc: true
sidebar:
  title: "Documentation"
  nav: docs
---

The EarthNet2021 samples, so-called data multicubes, are saved as compressed `numpy`arrays, so analysis-ready for usage in `python`. In the following we describe what exactly is contained in each multicube.

## Accessing multicube

The next example shows how to access the data in one multicube `example.npz`:

```python
import numpy as np

# Loading File
sample = np.load("example.npz")

# Accessing high-resolution dynamic variables (the Sentinel 2 bands)
hrd = sample["highresdynamic"]  
imgs = hrd[:,:,:4,:] # B, G, R, NIR channels
msks = hrd[:,:,-1,:] # EarthNet2021 binary quality mask

# Accessing mesoscale dynamic variables (the E-OBS weather data)
md = sample["mesodynamic"]

# Accessing high-resolution and mesoscale static variables (the EUDEM digital elevation model)
hrs = sample["highresstatic"]
ms = sample["mesostatic"]
```

## Highresdynamic

The variables `"highresdynamic"` have:
  - axes (height, width, channels, time)
  - dimension (128, 128, c, t)
    - t is the 5-daily time
    - Train c = 7, t = 30
    - Test c = 5
      - context t = 10 / 20 / 70
      - target t = 20 / 40 / 140
  - Channels:
    - Train (Blue, Green, Red, Near-Infrared, Sen2Cor Cloud Mask, ESA Scene Classification, EarthNet2021 Data Quality Mask)
    - Test (Blue, Green, Red, Near-Infrared, EarthNet2021 Data Quality Mask)
  - Units:
    - B, G, R, NIR (B02, B03, B04, B8A): 0 - 2 reflectance, NaN if not available.
    - Sen2Cor Cloud Mask (CLD): 0-100 cloud probability
    - ESA Scene Classification (SCL): 0-11 categories (see [here](https://docs.sentinel-hub.com/api/latest/data/sentinel-2-l2a/))
    - EarthNet2021 data quality mask: {0,1} binary mask, 0 if good quality, 1 if bad quality.

**ProTip:** Preprocess images by `imgs[imgs < 0] = 0`, `imgs[imgs > 1] = 1`, and `imgs[np.isnan(imgs)] = 0`.
{: .notice--info}

## Mesodynamic

The variables `"mesodynamic"` have:
  - axes (height, width, channels, time)
  - dimension (80, 80, 5, t)
    - t is the daily time, `md[:,:,:,4]` fits the sentinel 2 date `hrd[:,:,:,0]`.
    - Train t = 30
    - Test context t = 150 / 300 / 1050, target t = 0
  - Channels:
    - Precipitation (RR), Sea pressure (PP), Mean temperature (TG), Minimum temperature (TN), Maximum temperature (TX)
    - for more see [here](https://www.ecad.eu/dailydata/datadictionaryelement.php)
  - Units:
    - All data has been rescaled to lay between 0 and 1, transformation rules:
      - Temperatur (°C) = 5000*(2*temp - 1)
      - Rain (mm) = 50 * rain
      - Pressure (hPa) = 200 * pressure + 900

**ProTip:** Missing data in the E-OBS variables is visible by those pixels where PP = 0. Note this information does not go into the high-resolution data quality mask.
{: .notice--info}

## Static

The static variable has:
  - axes (height, width, channels)
  - dimension (h, w, 1)
    - `"highresstatic"`has h = w = 128
    - `"mesostatic"`has h = w = 80
  - Channels:
    - EU-DEM, see [here](https://www.eea.europa.eu/data-and-maps/data/copernicus-land-monitoring-service-eu-dem)
  - Units:
    - Data has been rescaled to lay between 0 and 1, transformation rule:
      - DEM (m) = 2000 * (2*dem - 1)