#!/bin/bash

MODEL_NAME="SVM-linear"
SAMPLER="TomekLinks"

python train.py --model "$MODEL_NAME" --sampler "$SAMPLER"
