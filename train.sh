#!/bin/bash

# Define an array of arguments
args=("arg1" "arg2" "arg3" "arg4")

# Loop through the array and execute the Python script with each argument
for arg in "${args[@]}"
do
    python your_script.py "$arg"
done