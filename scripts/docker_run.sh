#!/bin/bash
# Edit the directories to the ones where your data lives
# Give the project dir as the first keyboard argument. For optimal integration it should contain this repo earthnet2021 as a subdirectory.

#Workspace
project_dir=$1 #'/scratch/EarthNet2021/'
workspace='/workspace'

#Heavy files directory
data_dir='/dir/on/bigfilesdisk/to/data/'
work_data='/workspace/earthnet-model-intercomparison-suite/data'

#nvidia-docker run -p 8000:8888 -p 9300:9300 -it -v $project_dir:$workspace -it -v $data_dir:$work_data -it -v $dataset_dir:$work_dataset  earthnet2021:1.0 
docker run --gpus $2 --rm --ipc=host -p 8000:8888 -p 9300:9300 -p 9400:9400 -p 9500:9500 -p 9600:9600 -it -v $project_dir:$workspace -v $data_dir:$work_data -v /scratch/:/scratch/ earthnet2021:1.0