#!/bin/sh

cp config.py.sample config.py
mkdir .cunik
cd .cunik

mkdir images
echo "{}" > images/metadata.json

mkdir volumes
echo "{}" > volumes/metadata.json

mkdir networkconfigs
echo "{}" > networkconfigs/metadata.json
