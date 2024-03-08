---
layout: single
title: GreenEarthNet Download
permalink: /en21x/download/
toc: true
toc_stickly: true
sidebar:
  title: "GreenEarthNet"
  nav: en21x
---

## Downloading GreenEarthNet

GreenEarthNet is hosted on the MinIO server (similar to Amazon S3 storage) of the Max-Planck-Institute for Biogeochemistry.

You may download it using the **EarthNet Toolkit**.

### Installing EarthNet Toolkit

```
pip install earthnet
```

### Downloading GreenEarthNet with EarthNet Toolkit

```
import earthnet as entk
entk.download(dataset = "greenearthnet", split = "train", save_directory = "data_dir")
````

Where `data_dir` is the directory where GreenEarthNet shall be saved and `split` is `"all"`or a subset of `["train","val_chopped","ood-t_chopped","ood-s_chopped","ood-st_chopped"]`.

