---
layout: single
classes: wide
title: Earth surface forecasting - a novel task
permalink: /en21/ch-task/
sidebar:
  title: "EarthNet2021"
  nav: en21
---


{::nomarkdown}<iframe width="560" height="315" src="https://www.youtube.com/embed/sumLCeZ92Hk" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>{:/nomarkdown}

Climate change amplifies extreme weather events. Their impacts vary heterogeneously at the local scale. Thus forecasting localized climate impacts is highly relevant. Downstream applications include crop yield prediction, forest health assessments, biodiversity monitoring, coastline management or more general the estimation of vegetation state.

## A concrete example

![The 2018 summer heat wave impacted quite heterogenously on fields close to a river or depending on slope over the UK.](/assets/images/task-example-uk2019.png "South Dawns National Park near Seaford, UK. Satellite imagery from Sentinelhub.")

The 2018 summer heat wave, as can be seen, provides an example of different areas within one region being impacted very differently by extreme weather. This might be due to factors such as a nearby river or wether a slope is north- or south-facing. But obviously complex relationships come into play here.

## The Task

We define Earth surface forecasting as the task of guided video prediction of satellite imagery for forecasting localized weather impacts. More specifically, strong guidance with seasonal weather projections is leveraged. Models shall take past satellite imagery, topography and weather variables, the latter from past and future, and predict future satellite imagery.
