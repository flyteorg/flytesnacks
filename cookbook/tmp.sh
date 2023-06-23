#!/bin/sh

files=$(find ./integrations -mindepth 1 -maxdepth 5 -type f -name Dockerfile -exec dirname '{}' \;)
mkdir -p ./_integrations
for file in $files
do
    example_name=$(basename -- $file)
    mv $file ./_integrations/$example_name
done
