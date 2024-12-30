#### Set executable path and python library path
BASE_DIR=$PWD
PATH=$BASE_DIR:$PATH
PYTHONPATH=$PWD:$PYTHONPATH
mkdir -p tmp ; cd tmp/
link_file_if_absent.sh $BASE_DIR/data
link_file_if_absent.sh $BASE_DIR/out_makehisto.root

fitinfo=fitinfo_merged.yaml
sh run.step3.fitSignalRegion.sh $BASE_DIR/data/makehist_gjet.yaml $BASE_DIR/data/makehist_btag.yaml $BASE_DIR/data/makehist_cvsb.yaml $BASE_DIR/data/makehist_cvsl.yaml $fitinfo
