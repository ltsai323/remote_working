histSOURCE_gjet=`realpath $1`
initVAL_gjet=`realpath $2`
OUT_FITINFO=fitinfo_gjet_inclusive.yaml

function the_exit() { echo $1; exit; }



### Use sideband fit to extract the initial value of the C/B/L fractions
 ### [preprocess] prepare datacard and root files
 make_hist_source_and_datacard.py $histSOURCE_gjet
 
 ###### created files from make_hist_source_and_datacard.py
 _TMP_INPUT_HIST=datacard_gjet_inclusive.root
 _TMP_DATACARD=datacard_gjet_inclusive.txt


 ###### created file from extract_data_entries.py
 _TMP_BASHVAR=bashvar_gjet_inclusive.sh

 ### [pre process] grab init values
 extract_data_entries.py \
   $_TMP_INPUT_HIST 'gjet_inclusive/data_obs' \
   $_TMP_BASHVAR \
   $initVAL_gjet \
   || the_exit "[Failed] extract_data_entries.py got error"
 source ./$_TMP_BASHVAR # get bash variables

 ### [combine] create workspace for combine fitting

 ###### created file from text2workspace.py
 _TMP_INPUT_WORKSPACE=ws_gjet_inclusive.root
 text2workspace.py $_TMP_DATACARD -o $_TMP_INPUT_WORKSPACE \
     -P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel \
     --PO "map=.*/gjet:nSIGN[$initSIGN,0.,$nDATA]" \
     --PO "map=.*/SB:nFAKE[$initFAKE,0.,$nDATA]" \
     --PO verbose || exit "failed to create workspace from datacard"
 
 ### [combine] apply simultaneous fit
 combine --saveWorkspace -M MultiDimFit -d $_TMP_INPUT_WORKSPACE --saveFitResult --saveNLL --robustFit on || the_exit "failed to run combine @ data sideband"

 ### [combine] collect result
 
 _TMP_MULTIDIMFITTEST=multidimfitTest_gjet_inclusive.root
 _TMP_HIGGSCOMBINETEST=higgsCombineTest.MultiDimFit.mH120_gjet_inclusive.root
 mv multidimfitTest.root $_TMP_MULTIDIMFITTEST || the_exit "[NullOutput] Unable to get output file 'multidimfitTest.root' from fit result."
 mv higgsCombineTest.MultiDimFit.mH120.root $_TMP_HIGGSCOMBINETEST || the_exit "[NullOutput] Unable to get output file 'higgsCombineTest.MultiDimFit.mH120.root' from fit result."
 
 ### [post process] collect result to yaml file
 extract_fit_value.py inclusiveinfo \
   $_TMP_HIGGSCOMBINETEST \
   $OUT_FITINFO
### Use sideband fit to extract the initial value of the C/B/L fractions ended

####### Timer #######
#real	1m44.901s
#user	0m18.271s
#sys	0m21.646s
####### Timer #######
