---
layout: single
title: Download
permalink: /docs/ds-download/
last_modified_at: 2020-11-29
toc: true
sidebar:
  title: "Documentation"
  nav: docs
---

The EarthNet2021 dataset is free to download and no registration is required. There is 2 ways to download the dataset.

**Note:** We recommend at least **600GB** of free disk space before starting the download of EarthNet2021. 
{: .notice--warning}

## With EarthNet2021 toolkit (Recommended)

We recommend downloading the dataset with the [EarthNet2021 toolkit](/docs/tk-download/).

1. Install the EarthNet2021 toolkit `pip install earthnet` (see [here](/docs/tk-overview))
2. Run in `python`:
  
```python
import earthnet as en

en.Downloader.get(path/to/download/to, splits)
```

Here, `splits` specifies what parts of earthnet to download:
  - `"all"` Download the whole dataset.
  - `"train"`Download just the training dataset.
  - `["train","iid"]`Download just training and iid test set.
  
For more options see [here](/docs/tk-download/)

## Direct download links

We host the EarthNet2021 dataset as many gzipped tarballs, find the splits here:
  - [Download training data](https://owncloud.gwdg.de/index.php/s/7ZvOGBEXVXFBHgO)
  - [Download IID test data](https://owncloud.gwdg.de/index.php/s/rhMvwZylorD6riJ)
  - [Download OOD test data](https://owncloud.gwdg.de/index.php/s/rhMvwZylorD6riJ)
  - [Download Extreme event test data](https://owncloud.gwdg.de/index.php/s/8EZDLyzmEw0Qls1)
  - [Download Seasonal cycle test data](https://owncloud.gwdg.de/index.php/s/BkFoMR4ZRN459b4)

