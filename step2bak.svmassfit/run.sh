outDIR=${1:-tmp}

### Set executable path and python library path
BASE_DIR=$PWD
PATH=$BASE_DIR:$PATH
PYTHONPATH=$PWD:$PYTHONPATH

### Create output directory
touch $outDIR && /bin/rm -r $outDIR && mkdir -p $outDIR && cd $outDIR
function the_exit() { echo $1; exit; }

link_file_if_absent.sh $BASE_DIR/data
link_file_if_absent.sh $BASE_DIR/out_makehisto.root

sh $BASE_DIR/run.step1.fitGJet_inclusive.sh \
  data/makehist_gjet_inclusive.yaml \
  data/initcomposition_gjet_inclusive.yaml || the_exit "---- run step1 failed ----"

sh $BASE_DIR/run.step2.fitDataSideband.sh \
  data/makehist_SBbtag.yaml \
  data/makehist_SBcvsb.yaml \
  data/makehist_SBcvsl.yaml || the_exit "---- run step2 failed ----"



fitinfo=fitinfo_merged.yaml
touch $fitinfo ; /bin/rm $fitinfo
cat fitinfo_sideband.yaml >> $fitinfo
cat fitinfo_gjet_inclusive.yaml >> $fitinfo

sh $BASE_DIR/run.step3.fitSignalRegion.sh \
  data/makehist_gjet.yaml \
  data/makehist_btag.yaml \
  data/makehist_cvsb.yaml \
  data/makehist_cvsl.yaml \
  $fitinfo || the_exit "---- run step3 failed ----"
