---
layout: single
title: Structure
classes: wide
permalink: /docs/ds-structure/
sidebar:
  title: "Documentation"
  nav: docs
---
Nothing clever here 😉. Every sample is stored as a compressed numpy array .npz. File structure follows `<split_name>/<tile_name>/<cube_name.npz>`

```bash
EarthNet2021
├── train   			# training set of the EarthNet2021 challenge
|  ├── 29SND      # Sentinel 2 tile with samples at lon 29, lat S, subquadrant ND
|  |  ├── 29SND_2017...124.npz 	# First training sample, name cubename.npz
|  |  └── ...
|  ├── 29SPC      # there is 85 tiles in the train set
|  └── ...      # with 23904 .npz train samples in total
├── iid_test_split    # main track testing samples
|  ├── context      # input data ("context") for models
|  |  └── 29SND       
|  |  |   └── context_29SND_....npz # context cube, name: context_cubename.npz
|  |  └── ...
|  └── target     # target/output data for models
|     ├── 29SND     # tiles containing iid_test samples.
|     |   └── target_29SND_....npz  # context cube, name: target_cubename.npz
|     └── ...     # there is 4219 iid_test samples in total
├── ood_test_split     # robustness track testing samples
|  ├── context     	
|  └── target     # there is 4214 ood_test samples in total
├── extreme_test_split    # extreme weather testing samples
|  ├── context     	
|  └── target     # there is 4000 extreme_test samples in total
└── seasonal_test_split   # seasonal testing samples
   ├── context     	
   └── target     # there is 4000 iid_test samples in total

```

**ProTip:** Each cubename has format `tile_startyear_startmonth_startday_endyear_endmonth_endday_hrxmin_hrxmax_hrymin_hrymax_mesoxmin_mesoxmax_mesoymin_mesoymax`. So contains the exact spatiotemporal footprint of the particular sample.
{: .notice--info}