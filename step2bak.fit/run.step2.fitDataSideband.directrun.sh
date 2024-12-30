#### Set executable path and python library path
BASE_DIR=$PWD
PATH=$BASE_DIR:$PATH
PYTHONPATH=$PWD:$PYTHONPATH
mkdir -p tmp ; cd tmp/
link_file_if_absent.sh $BASE_DIR/data
link_file_if_absent.sh $BASE_DIR/out_makehisto.root

sh run.step2.fitDataSideband.sh $BASE_DIR/data/makehist_SBbtag.yaml $BASE_DIR/data/makehist_SBcvsb.yaml $BASE_DIR/data/makehist_SBcvsl.yaml
