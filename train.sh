#!/bin/bash

# Define an array of arguments
args=("back_trans" "emo_to_text" "baseline" "gpt_aug" "multi-label" "noise_aug" "emoji_augmentation")


# Loop through the array and execute the Python script with each argument
for arg in "${args[@]}"
do
    echo "Start training for $arg"
    export METHOD=$arg
    python train.py
    # echo $METHOD
    echo "completed!"
    echo " "
    echo " "
    # echo "$arg"
done