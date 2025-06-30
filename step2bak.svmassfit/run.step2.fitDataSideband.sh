histSOURCE_btag=`realpath $1`
histSOURCE_cvsb=`realpath $2`
histSOURCE_cvsl=`realpath $3`

function the_exit() { echo $1; exit; }

histSOURCE_SBbtag=`realpath $histSOURCE_btag`
histSOURCE_SBcvsb=`realpath $histSOURCE_cvsb`
histSOURCE_SBcvsl=`realpath $histSOURCE_cvsl`


### Use sideband fit to extract the initial value of the C/B/L fractions
 ### [preprocess] prepare datacard and root files
 make_hist_source_and_datacard.py $histSOURCE_SBbtag
 make_hist_source_and_datacard.py $histSOURCE_SBcvsl
 make_hist_source_and_datacard.py $histSOURCE_SBcvsb
_TMP_DATACARD=datacards_SB.txt
 combineCards.py \
   SBbtag=datacard_SBbtag.txt \
   SBcvsl=datacard_SBcvsl.txt \
   SBcvsb=datacard_SBcvsb.txt \
   > $_TMP_DATACARD
 

 ### [pre process] grab init values
 extract_data_entries.py \
   datacard_SBbtag.root 'SBbtag/data_obs' \
   bashvar_sideband.sh || the_exit "[Failed] extract_data_entries.py got error"
 source ./bashvar_sideband.sh # get bash variables

 ### [combine] create workspace for combine fitting
 text2workspace.py $_TMP_DATACARD -o ws_SB.root \
     -P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel \
     --PO "map=.*/ljet:nL[$initL,0.,$nDATA]" \
     --PO "map=.*/cjet:nC[$initC,0.,$nDATA]" \
     --PO "map=.*/bjet:nB[$initB,0.,$nDATA]" \
     --PO verbose || exit "failed to create workspace from datacard"
 
 ### [combine] apply simultaneous fit
 combine --saveWorkspace -M MultiDimFit -d ws_SB.root --saveFitResult --saveNLL --robustFit on || the_exit "failed to run combine @ data sideband"

_TMP_MULTIDIMFITTEST=multidimfitTest_sideband.root
_TMP_HIGGSCOMBINETEST=higgsCombineTest.MultiDimFit.mH120_sideband.root
 ### [combine] collect result
 mv multidimfitTest.root $_TMP_MULTIDIMFITTEST || the_exit "[NullOutput] Unable to get output file 'multidimfitTest.root' from fit result."
 mv higgsCombineTest.MultiDimFit.mH120.root $_TMP_HIGGSCOMBINETEST || the_exit "[NullOutput] Unable to get output file 'higgsCombineTest.MultiDimFit.mH120.root' from fit result."
 
 ### [post process] collect result to yaml file
 extract_fit_value.py LCBinfo \
   higgsCombineTest.MultiDimFit.mH120_sideband.root \
   fitinfo_sideband.yaml
### Use sideband fit to extract the initial value of the C/B/L fractions ended

 PostFitShapesFromWorkspace -d $_TMP_DATACARD \
     -w $_TMP_HIGGSCOMBINETEST \
     -m 120 -f $_TMP_MULTIDIMFITTEST:fit_mdf \
     --postfit --print --output postfit_fitDataSideband.root || the_exit "PostFitShapeFromWorkspace failed to activate the command"
