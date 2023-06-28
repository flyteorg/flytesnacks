#!/bin/sh
#
# Usage for simple directory:
#
# ./scripts/pip-compile.sh <example-dir>
#
# Compile all examples:
#
# ./scripts/pip-compile.sh

examples=$1

if [ -z "$examples" ]
then
    examples=$(find examples -type d -d 1)
fi

build_requirements() {
    pip-compile requirements.in --upgrade --verbose --resolver=backtracking
}

for dir in $examples
do
    (cd "$dir" && build_requirements)
done
