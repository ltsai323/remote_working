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
 combineCards.py \
   SBbtag=datacard_SBbtag.txt \
   SBcvsl=datacard_SBcvsl.txt \
   SBcvsb=datacard_SBcvsb.txt \
   > datacards_SB.txt
 

 ### [pre process] grab init values
 extract_data_entries.py \
   datacard_SBbtag.root 'SBbtag/data_obs' \
   bashvar_sideband.sh || the_exit "[Failed] extract_data_entries.py got error"
 source ./bashvar_sideband.sh # get bash variables

 ### [combine] create workspace for combine fitting
 text2workspace.py datacards_SB.txt -o ws_SB.root \
     -P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel \
     --PO "map=.*/ljet:nL[$initL,0.,$nDATA]" \
     --PO "map=.*/cjet:nC[$initC,0.,$nDATA]" \
     --PO "map=.*/bjet:nB[$initB,0.,$nDATA]" \
     --PO verbose || exit "failed to create workspace from datacard"
 
 ### [combine] apply simultaneous fit
 combine --saveWorkspace -M MultiDimFit -d ws_SB.root --saveFitResult --saveNLL --robustFit on || the_exit "failed to run combine @ data sideband"

 ### [combine] collect result
 mv multidimfitTest.root multidimfitTest_sideband.root || the_exit "[NullOutput] Unable to get output file 'multidimfitTest.root' from fit result."
 mv higgsCombineTest.MultiDimFit.mH120.root higgsCombineTest.MultiDimFit.mH120_sideband.root || the_exit "[NullOutput] Unable to get output file 'higgsCombineTest.MultiDimFit.mH120.root' from fit result."
 
 ### [post process] collect result to yaml file
 extract_fit_value.py LCBinfo \
   higgsCombineTest.MultiDimFit.mH120_sideband.root \
   fitinfo_sideband.yaml
### Use sideband fit to extract the initial value of the C/B/L fractions ended

####### Timer #######
#real	1m44.901s
#user	0m18.271s
#sys	0m21.646s
####### Timer #######
