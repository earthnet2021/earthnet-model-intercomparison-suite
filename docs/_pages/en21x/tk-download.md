---
layout: single
title: EarthNet2021 Toolkit API - Download
permalink: /en21x/tk-download/
toc: true
toc_stickly: true
sidebar:
  title: "EarthNet2021X"
  nav: en21x
---

## Downloading EarthNet2021

The key function for downloading EarthNet2021 is a class method that downloads, checks SHA-hashes and unpacks the Dataset into a desired folder.

Ensure you have enough free disk space! We recommend 1TB.

```python
import earthnet as en
en.Downloader.get(data_dir, splits)
```

Where  `data_dir` is the directory where EarthNet2021 shall be saved and `splits` is `"all"`or a subset of `["train","iid","ood","extreme","seasonal"]`.


Alternatively:

```shell
cd earthnet-toolkit/earthnet/
python download.py -h
python download.py "Path/To/Download/To" "all"
```
For using in the commandline.

## API

### earthnet.download module


### class earthnet.download.DownloadProgressBar(iterable=None, desc=None, total=None, leave=True, file=None, ncols=None, mininterval=0.1, maxinterval=10.0, miniters=None, ascii=None, disable=False, unit='it', unit_scale=False, dynamic_ncols=False, smoothing=0.3, bar_format=None, initial=0, position=None, postfix=None, unit_divisor=1000, write_bytes=None, lock_args=None, gui=False, \*\*kwargs)
Bases: `tqdm.std.tqdm`


#### update_to(b=1, bsize=1, tsize=None)

### class earthnet.download.Downloader(data_dir: str)
Bases: `object`

Downloader Class for EarthNet2021


#### \__init__(data_dir: str)
Initialize Downloader Class

Args:

    data_dir (str): The directory where the data shall be saved in, we recommend data/dataset/


#### classmethod get(data_dir: str, splits: Union[str, Sequence[str]], overwrite: bool = False, delete: bool = True)
Download the EarthNet2021 Dataset

Before downloading, ensure that you have enough free disk space. We recommend 1 TB.

Specify the directory data_dir, where it should be saved. Then choose, which of the splits you want to download.
All available splits: [“train”,”iid”,”ood”,”extreme”,”seasonal”]
You can either give “all” to splits or a List of splits, for example [“train”,”iid”].

Args:

    data_dir (str): The directory where the data shall be saved in, we recommend data/dataset/
    splits (Sequence[str]): Either “all” or a subset of [“train”,”iid”,”ood”,”extreme”,”seasonal”]. This determines the splits that are downloaded.
    overwrite (bool, optional): If True, overwrites an existing gzipped tarball by downloading it again. Defaults to False.
    delete (bool, optional): If True, deletes the downloaded tarball after unpacking it. Defaults to True.


### earthnet.download.get_sha_of_file(file: str, buf_size: int = 104857600)



