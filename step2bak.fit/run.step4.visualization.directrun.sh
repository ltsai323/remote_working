#!/usr/bin/env sh
#### Set executable path and python library path
BASE_DIR=$PWD
PATH=$BASE_DIR:$PATH
PYTHONPATH=$PWD:$PYTHONPATH
mkdir -p tmp ; cd tmp/
mkdir outputs/
link_file_if_absent.sh $BASE_DIR/postfit.root

sh run.step4.visualization.sh

