#!/bin/sh
#
# Usage: ./scripts/serialize-example.sh <example-dir> <version>

dir="$1"
version="$2"

build() {
    docker build . -t "$1"
}

serialize() {
    docker run -i --rm -v "$(pwd)":/root "$2" \
        pyflyte --pkgs "$1" \
        package \
        --image "$2" \
        --image mindmeld="ghcr.io/flyteorg/flytecookbook:core-latest" \
        --image borebuster="ghcr.io/flyteorg/flytekit:py3.9-latest" \
        --output ./flyte-package.tgz \
        --force
}

example_name=$(basename -- "$dir")
image_uri=ghcr.io/flyteorg/flytecookbook:"$example_name"-"$version"
(cd "$dir" && build "$image_uri" && serialize "$example_name" "$image_uri")
