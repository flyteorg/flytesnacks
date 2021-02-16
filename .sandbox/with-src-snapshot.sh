#!/bin/sh

set -e

SOURCE_DIR=${SOURCE_DIR:-/mnt/src}
DESTINATION_DIR=${DESTINATION_DIR:-/usr/src}

[ -d $SOURCE_DIR ] || ( echo >&2 "Not a directory: $SOURCE_DIR" && exit 1 )

mkdir -p $DESTINATION_DIR
rsync -az $SOURCE_DIR/ $DESTINATION_DIR/

exec "$@"
