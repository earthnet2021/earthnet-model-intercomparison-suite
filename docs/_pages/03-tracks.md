---
layout: single
title: Tracks
permalink: /docs/tracks/
last_modified_at: 2020-11-07
toc: true
sidebar:
  title: "Getting Started"
  nav: docs
---

For all tracks, models are allowed to use the EarthNet2021 training set for model training in whichever way is useful for them.
<figure class="half">
    <a href="{{ site.baseurl }}/assets/images/guide_cube_spatial_distribution.png"><img src="{{ site.baseurl }}/assets/images/guide_cube_spatial_distribution.png"></a>
    <figcaption>Spatial distribution of test sets.</figcaption>
</figure>
## Independent and Identically Distributed
The independent and identically distributed test set (iid_test) is the main track of the EarthNet2021 challenge. The iid_test assumes that in production any such model would haveaccess to all prior global data, thus the test set has the same underlying distribution as the training set.


## Out-of-Distribution

The out-of-distribution test set (ood_test) is the robustness track of the EarthNet2021 challenge. For this track samples in the test set are drawn from a distribution of geolocations diferent to that of the training set, else it is set up exactly like the main track. This spatial out-of-data setting is particularly interesting as a mean to measure the generalization capability of the models.


## Extreme Weather

The extreme summer test set (extreme_test) contains samples from the extreme summer 2018 in northern Germany, a known harsh drought. Samples are larger, with 4 months of context (20 imagery frames) starting in February and 6 months (40 frames) starting from June to evaluate predictions. For these locations there are some samples dated before 2018 in the training set. Accurate downscaling of an extreme heat event and it's effects to vegetation will greatly benefit resilience strategies.



## Full Seasonal Cycle

 The full seasonal cycle test set (seasonal_test) covers multiple years of observations; and hence, includes vegetation's full seasonal cycle. This track in line with the recently rising interest in seasonal forecasts within physical climate models. It contains multicubes from the spatial distribution of ood_test, but this time each sample has 1 year (70 frames) of context frames and 2 years (140 frames) to evaluate predictions. While the main target EarthNet2021 is to evaluate near-future forecasting, models are likely able to predict longer horizons. This test track will provide useful insight to determine how far into the future predictions are accurate and to design the test tracks for future editions.