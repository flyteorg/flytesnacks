#!/bin/bash

VERSION=""
while IFS=':' read -ra IMG; do
  for i in "${IMG[@]}"; do
      VERSION=$i
  done
done <<< "${FLYTE_INTERNAL_IMAGE}"
echo ${VERSION}
