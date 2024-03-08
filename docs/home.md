---
layout: splash
permalink: /
header:
  overlay_color: "#5e616c"
  overlay_image: /assets/images/en-home-overlay.png
  cta_label: "<i class='fa fa-download'></i> Install Now"
  cta_url: "/en21x/download/"
  caption:
excerpt: 'A machine learning challenge and dataset for Earth surface and localized impact forecasting.<br /> <small><a href="https://arxiv.org/abs/2303.16198v2">GreenEarthNet - accepted at CVPR 2024</a></small><br /> <small><a href="https://openaccess.thecvf.com/content/CVPR2021W/EarthVision/html/Requena-Mesa_EarthNet2021_A_Large-Scale_Dataset_and_Challenge_for_Earth_Surface_Forecasting_CVPRW_2021_paper.html">EarthNet2021 - CVPR 2021 EarthVision paper</a></small><br /> <small><a href="https://arxiv.org/abs/2210.13648">ConvLSTM over Africa - NeurIPS 2022 HADR.AI workshop</a></small><br />'
feature_row:
  - image_path: /assets/images/en-feature-1-satellite.png
    alt: "earth surface forecasting"
    title: "Earth surface forecasting"
    excerpt: "Using Machine Learning to forecast the dynamics of Earth's surface, we can predict crop yield, forest health, the effects of a drought and more."
    url: "/en21/ch-task/"
    btn_class: "btn--primary"
    btn_label: "Learn more"
  - image_path: /assets/images/en-feature-2-pt-tf.png
    alt: "earthnet-models-pytorch"
    title: "EarthNet Models PyTorch"
    excerpt: 'Perform training and inference of deep neural networkswith the EarthNet Models PyTorch Python package.{::nomarkdown}<p style="margin-top: -5px;margin-bottom: 0px"><iframe style="display: inline-block;" src="https://ghbtns.com/github-btn.html?user=earthnet2021&repo=earthnet-models-pytorch&type=star&count=true&size=large" frameborder="0" scrolling="0" width="160px" height="30px"></iframe><iframe style="display: inline-block;" src="https://ghbtns.com/github-btn.html?user=earthnet2021&repo=earthnet-models-pytorch&type=fork&count=true&size=large" frameborder="0" scrolling="0" width="158px" height="30px"></iframe></p>{:/nomarkdown}'
    url: "https://github.com/earthnet2021/earthnet-models-pytorch"
    btn_class: "btn--primary"
    btn_label: "Learn more"
  - image_path: /assets/images/en-feature-3-opensource.png
    alt: "earthnet-minicuber"
    title: "EarthNet Minicuber"
    excerpt: 'Generate new analysis-ready minicubes at any place on Earth using the EarthNet Minicuber Python package.{::nomarkdown}<p style="margin-top: -5px;margin-bottom: 0px"><iframe style="display: inline-block;" src="https://ghbtns.com/github-btn.html?user=earthnet2021&repo=earthnet-minicuber&type=star&count=true&size=large" frameborder="0" scrolling="0" width="160px" height="30px"></iframe><iframe style="display: inline-block;" src="https://ghbtns.com/github-btn.html?user=earthnet2021&repo=earthnet-minicuber&type=fork&count=true&size=large" frameborder="0" scrolling="0" width="158px" height="30px"></iframe></p>{:/nomarkdown}'
    url: "https://github.com/earthnet2021/earthnet-minicuber"
    btn_class: "btn--primary"
    btn_label: "Learn more" 
---
{% include feature_row %}

<h1> Latest News</h1>
<div class="grid__wrapper">
  {% for post in site.posts limit:3 %}
    {% include archive-single.html %}
  {% endfor %}
</div>
