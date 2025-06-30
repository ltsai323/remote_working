outDIR=$1
pETAbin=$2
jETAbin=$3
pPTlow=$4
pPThigh=$5
dataERA=2022EE


### Set executable path and python library path
BASE_DIR=$PWD/
DIR_STEP31=$BASE_DIR/../step3.1.makehisto
DIR_STEP32=$BASE_DIR/../step3.2.fit
DIR_STEP33=$BASE_DIR/../step3.3.visualization
PATH=$DIR_STEP32:$PATH
PYTHONPATH=$DIR_STEP32:$PYTHONPATH

### Create output directory
touch $outDIR && /bin/rm -r $outDIR && mkdir -p $outDIR && cd $outDIR
function the_exit() { echo $1; exit; }

### step3.1
echo "[step31] start"
python3  $DIR_STEP31/makehisto_Run2022.py $dataERA $pETAbin $jETAbin $pPTlow $pPThigh
echo "[step31] finished"


### step3.2
echo "[step32] start"
link_file_if_absent.sh $DIR_STEP32/data
#link_file_if_absent.sh $BASE_DIR/out_makehisto.root

sh $DIR_STEP32/run.step1.fitGJet_inclusive.sh \
  $DIR_STEP32/data/makehist_gjet_inclusive.yaml \
  $DIR_STEP32/data/initcomposition_gjet_inclusive.yaml || the_exit "---- run step1 failed ----"

sh $DIR_STEP32/run.step2.fitDataSideband.sh \
  $DIR_STEP32/data/makehist_SBbtag.yaml \
  $DIR_STEP32/data/makehist_SBcvsb.yaml \
  $DIR_STEP32/data/makehist_SBcvsl.yaml || the_exit "---- run step2 failed ----"



fitinfo=fitinfo_merged.yaml
touch $fitinfo ; /bin/rm $fitinfo
cat fitinfo_sideband.yaml >> $fitinfo
cat fitinfo_gjet_inclusive.yaml >> $fitinfo

sh $DIR_STEP32/run.step3.fitSignalRegion.sh \
  $DIR_STEP32/data/makehist_gjet.yaml \
  $DIR_STEP32/data/makehist_btag.yaml \
  $DIR_STEP32/data/makehist_cvsb.yaml \
  $DIR_STEP32/data/makehist_cvsl.yaml \
  $fitinfo || the_exit "---- run step3 failed ----"
echo "[step32] finished"


### step3.3
echo "[step33] start"
file_postfit=postfit.root
file_yaml_template=$DIR_STEP33/data/input.template.yaml
mkdir outputs/

FILE_PLOTABLE=secondary_plotable.root
python3 $DIR_STEP33/secondary_plotable.py $file_postfit $FILE_PLOTABLE
python3 $DIR_STEP33/input_yaml_generator.py $file_yaml_template $FILE_PLOTABLE

DrawRatioPlotablesWithCMSFormat.py input.gjet.yaml
DrawRatioPlotablesWithCMSFormat.py input.btag.yaml
DrawRatioPlotablesWithCMSFormat.py input.cvsl.yaml
DrawRatioPlotablesWithCMSFormat.py input.cvsb.yaml

echo "[step33] finished"
