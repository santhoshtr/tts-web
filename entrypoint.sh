#!/bin/bash
BASE_MODEL_DIR="models"
set -e

mkdir -p $BASE_MODEL_DIR
wget -N --no-verbose --show-progress --progress=bar:force:noscroll https://data.statmt.org/lid/lid201-model.bin.gz -P models
pushd $BASE_MODEL_DIR
gunzip lid201-model.bin.gz
rm -rf lid201-model.bin.gz
popd


uvicorn app:app --host 0.0.0.0 --port 80
