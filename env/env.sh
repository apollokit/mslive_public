#!/bin/bash
set -e

SCRIPT_DIR=$(dirname $(realpath $0))
PROJ_DIR="$SCRIPT_DIR/.."

source $SCRIPT_DIR/source_virtualenv
# execute
PYTHONPATH=$PYTHONPATH:$PROJ_DIR "$@"
