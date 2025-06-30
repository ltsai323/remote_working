outDIR=${1:-tmp}

### Set executable path and python library path
this_file=`realpath $0`
BASE_DIR=`dirname $thisfile`
PATH=$BASE_DIR:$PATH
PYTHONPATH=$PWD:$PYTHONPATH

function the_exit() { echo $1; exit; }
### Create output directory
#touch $outDIR && /bin/rm -r $outDIR && mkdir -p $outDIR && cd $outDIR
cd $outDIR


sh $BASE_DIR/run.step1.fitGJet_WP.sh \
  $BASE_DIR/data/makehist_gjet_WP0.yaml \
  $BASE_DIR/data/initcomposition_gjet_inclusive.yaml \
  WP0 \
  || the_exit "---- run step1 WP0 failed ----"

sh $BASE_DIR/run.step1.fitGJet_WP.sh \
  $BASE_DIR/data/makehist_gjet_WPc.yaml \
  $BASE_DIR/data/initcomposition_gjet_inclusive.yaml \
  WPc \
  || the_exit "---- run step1 WPc failed ----"

sh $BASE_DIR/run.step1.fitGJet_WP.sh \
  $BASE_DIR/data/makehist_gjet_WPb.yaml \
  $BASE_DIR/data/initcomposition_gjet_inclusive.yaml \
  WPb \
  || the_exit "---- run step1 WPb failed ----"
