---
layout: single
toc: true
toc_sticky: true
toc_label: Test Tracks
title: EarthNet2021 Challenge - Leaderboard
permalink: /docs/ch-leaderboard/
last_modified_at: 2022-08-19
sidebar:
  title: "Documentation"
  nav: docs
---

## Main (IID)

| **Rank** |      **Model Name**      | **Group Name** |   **MAD**  |   **OLS**  |   **EMD**  |  **SSIM**  | **EarthNetScore** |
|:----:|:--------------------:|:----------:|:------:|:------:|:------:|:------:|:-------------:|
| 1    | [Diaconu ConvLSTM](https://openaccess.thecvf.com/content/CVPR2022W/EarthVision/papers/Diaconu_Understanding_the_Role_of_Weather_Data_for_Earth_Surface_Forecasting_CVPRW_2022_paper.pdf) | [Codrut-Andrei Diaconu]([/about/](https://www.asg.ed.tum.de/en/sipeo/team/codrut-andrei-diaconu/))     | 0.2638 | 0.3513 | 0.2623 |     0.5565  |  0.3266   |
| 2    | [SGConvLSTM](https://www.biorxiv.org/content/10.1101/2022.08.16.504173v1.full.pdf) | [ETH Zurich](https://usys.ethz.ch/en/people/profile.MTUxNjQ5.TGlzdC8yODUyLDMyMDE5NzIyMg==.html)     | 0.2589 | 0.3456 | 0.2533 |     0.5292    | 0.3176 |
| 3    | [SGEDConvLSTM](https://www.biorxiv.org/content/10.1101/2022.08.16.504173v1.full.pdf) | [ETH Zurich](https://usys.ethz.ch/en/people/profile.MTUxNjQ5.TGlzdC8yODUyLDMyMDE5NzIyMg==.html)     | 0.2580 | 0.3440 | 0.2532 | 0.5237 |     0.3164    |
| 4    | [Channel-U-Net Baseline](https://arxiv.org/pdf/2104.10066.pdf) | [EN-Team](/about/)     | 0.2482 | 0.3381 | 0.2336 |     0.3973  | 0.2902   |
| 5    | [Arcon Baseline](https://arxiv.org/pdf/2104.10066.pdf) | [EN-Team](/about/)     | 0.2414 | 0.3216 | 0.2258 |     0.3863    | 0.2803 |
| 6    | [Persistence Baseline](https://arxiv.org/pdf/2104.10066.pdf) | [EN-Team](/about/)     | 0.2315 | 0.3239 | 0.2099 | 0.3265 |     0.2625    |
| 7    |                      |            |        |        |        |        |               |
| 8    |                      |            |        |        |        |        |               |
| 9    |                      |            |        |        |        |        |               |




## Robustness (OOD)

| **Rank** |      **Model Name**      | **Group Name** |   **MAD**  |   **OLS**  |   **EMD**  |  **SSIM**  | **EarthNetScore** |
|:----:|:--------------------:|:----------:|:------:|:------:|:------:|:------:|:-------------:|
| 1    | [Channel-U-Net Baseline](https://arxiv.org/pdf/2104.10066.pdf) | [EN-Team](/about/)     | 0.2402 | 0.3390 | 0.2371 | 0.3721 |     0.2854    |
| 2    | [Arcon Baseline](https://arxiv.org/pdf/2104.10066.pdf) | [EN-Team](/about/)     | 0.2314 | 0.3088 | 0.2177 | 0.3432 |     0.2655    |
| 3    | [Persistence Baseline](https://arxiv.org/pdf/2104.10066.pdf) | [EN-Team](/about/)     | 0.2248 | 0.3236 | 0.2123 | 0.3112 |     0.2587    |
| 4    |                      |            |        |        |        |        |               |
| 5    |                      |            |        |        |        |        |               |
| 6    |                      |            |        |        |        |        |               |



## Extreme Summer

| **Rank** |      **Model Name**      | **Group Name** |   **MAD**  |   **OLS**  |   **EMD**  |  **SSIM**  | **EarthNetScore** |
|:----:|:--------------------:|:----------:|:------:|:------:|:------:|:------:|:-------------:|
| 1    | [Channel-U-Net Baseline](https://arxiv.org/pdf/2104.10066.pdf) | [EN-Team](/about/)     | 0.2286 | 0.2973 | 0.2065 | 0.2306 |     0.2364    |
| 2    | [Arcon Baseline](https://arxiv.org/pdf/2104.10066.pdf) | [EN-Team](/about/)     | 0.2243 | 0.2753 | 0.1975 | 0.2084 |     0.2215    |
| 3    | [Persistence Baseline](https://arxiv.org/pdf/2104.10066.pdf) | [EN-Team](/about/)     | 0.2158 | 0.2806 | 0.1614 | 0.1605 |     0.1939    |
| 4    |                      |            |        |        |        |        |               |
| 5    |                      |            |        |        |        |        |               |
| 6    |                      |            |        |        |        |        |               |




## Seasonal Cycle

| **Rank** |      **Model Name**      | **Group Name** |   **MAD**  |   **OLS**  |   **EMD**  |  **SSIM**  | **EarthNetScore** |
|:----:|:--------------------:|:----------:|:------:|:------:|:------:|:------:|:-------------:|
| 1    | [Persistence Baseline](https://arxiv.org/pdf/2104.10066.pdf) | [EN-Team](/about/)     | 0.2329 | 0.3848 | 0.2034 | 0.3184 |     0.2676    |
| 2    | [Channel-U-Net Baseline](https://arxiv.org/pdf/2104.10066.pdf) | [EN-Team](/about/)     | 0.2169 | 0.3811 | 0.1903 | 0.1255 |     0.1955    |
| 3    | [Arcon Baseline](https://arxiv.org/pdf/2104.10066.pdf) | [EN-Team](/about/)     | 0.2014 | 0.3788 | 0.1787 | 0.0834 |     0.1587    |
| 4    |                      |            |        |        |        |        |               |
| 5    |                      |            |        |        |        |        |               |
| 6    |                      |            |        |        |        |        |               |
