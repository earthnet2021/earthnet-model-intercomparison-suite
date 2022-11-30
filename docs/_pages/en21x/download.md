---
layout: single
title: EarthNet2021x Download
permalink: /en21x/download/
toc: true
toc_stickly: true
sidebar:
  title: "EarthNet2021X"
  nav: en21x
---

## Downloading EarthNet2021x

EarthNet2021x is hosted on the MinIO server (similar to Amazon S3 storage) of the Max-Planck-Institute for Biogeochemistry.

You may download it using the **EarthNet Toolkit**.

### Installing EarthNet Toolkit

```
pip install earthnet
```

### Downloading EarthNet2021x with EarthNet Toolkit

```
import earthnet as en
en.download(dataset = "earthnet2021x", split = "train", save_directory = "data_dir")
````

Where `data_dir` is the directory where EarthNet2021x shall be saved and splits is `"all"` or one of ["train","iid","ood","extreme","seasonal"].

