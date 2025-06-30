#### Set executable path and python library path
BASE_DIR=$PWD
PATH=$BASE_DIR:$PATH
PYTHONPATH=$PWD:$PYTHONPATH

inDATACARD=$BASE_DIR/data/makehist_gjet_inclusive.yaml
initCOMPOSITION=$BASE_DIR/data/initcomposition_gjet_inclusive.yaml
mkdir -p tmp ; cd tmp/
link_file_if_absent.sh $BASE_DIR/data
link_file_if_absent.sh $BASE_DIR/out_makehisto.root

sh run.step1.fitGJet_inclusive.sh $inDATACARD $initCOMPOSITION
