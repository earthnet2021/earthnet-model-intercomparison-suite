---
layout: single
title: Structure
permalink: /docs/structure/
last_modified_at: 2020-11-08
sidebar:
  title: "Getting Started"
  nav: docs
---
Nothing clever here :wink:. Every sample is stored as a crompressed numpy array .npz. File structure follows `<split_name>/<tile_name>/<sample_name.npz>`

```bash
EarthNet2021
├── training			# training set of the EarthNet2021 challenge
|  ├── 29SND 			# Sentinel 2 tile containing samples at longitude 29, latitude S, subquadrant ND
|  |  ├── 29SND_2017...124.npz # First training sample
|  |  └── ...
|  ├── 29SPC			# there is 85 tiles in the train set
|  └── ...			# with 23904 .npz train samples in total
├── iid_test			# main track testing samples
|  └── 29SND 			# tiles containing iid_test samples.
|     └── ...			# there is 4219 iid_test samples in total
├── ood_test			# robustness track testing samples
|  └── 29SQC     		# tiles containing iid_test samples
|     └── ...			# there is 4214 ood_test samples in total
├── extreme_test		# extreme weather testing samples
|  └── 32UMC     		# tiles containing extreme_test samples
|     └── ...			# there is 4000 extreme_test samples in total
├── seasonal_test		# seasonal testing samples
|  └── 29SQC     		# tiles containing seasonal_test samples
|     └── ...			# there is 4000 iid_test samples in total
└── csv               		# summary statistics created during dataset generation
   ├── extreme.csv
   ├── iid.csv
   ├── ood.csv
   ├── seasonal.csv
   └── train.csv
```