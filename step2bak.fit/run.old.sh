#inDATACARD=`realpath datacard_gjet.txt`
#inDATACARD=`realpath datacard_btag.txt`
#inDATACARD=`realpath datacards.txt`
inDATACARD_SB=datacard_SBbtag.txt
outDIR=tmp

function the_exit() { echo $1; exit; }

SOURCE_DIR=$PWD
histSOURCE=`realpath data/makehist_SBbtag.yaml`
histSOURCE_SBbtag=`realpath data/makehist_SBbtag.yaml`
histSOURCE_SBcvsb=`realpath data/makehist_SBcvsb.yaml`
histSOURCE_SBcvsl=`realpath data/makehist_SBcvsl.yaml`


### Set executable path and python library path
PATH=$PWD:$PATH
PYTHONPATH=$PWD:$PYTHONPATH

### Create output directory
mkdir -p $outDIR && cd $outDIR
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
 

 ### [preprocess] grab init values
 extract_data_entries.py \
   datacard_SBbtag.root 'SBbtag/data_obs' \
   bashvar_sideband.sh || the_exit "[Failed] extract_data_entries.py got error"
 source bashvar_sideband.sh # get bash variables

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
 
 ### [out] collect result to yaml file
 extract_fit_value.py LCBinfo higgsCombineTest.MultiDimFit.mH120_sideband.root fitinfo_sideband.yaml
### Use sideband fit to extract the initial value of the C/B/L fractions ended

####### Timer #######
#real	1m44.901s
#user	0m18.271s
#sys	0m21.646s
####### Timer #######

 ### [preprocess] grab init values from sideband fitting.
 # asdf need to modify the input root file and input hist name
 extract_data_entries.py \
   datacard_SBbtag.root 'SBbtag/data_obs' \
   bashvar_sideband_fit.sh \
   fitinfo_sideband.yaml || the_exit "[Failed] extract_data_entries.py is not able to calculate init value for fit."
exit

#text2workspace.py datacard_SBbtag.txt -o ws.root \
#    -P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel \
#    --PO "map=.*/ljet:nL[84655.0,0.,84655.0]" \
#    --PO "map=.*/cjet:nC[8465.0 ,0.,84655.0]" \
#    --PO "map=.*/bjet:nB[846.0  ,0.,84655.0]" \
#    --PO "map=.*/SB:nSB[8465.0 ,0.,84655.0]" \
#    --PO verbose || exit "failed to create workspace from datacard"


    
combine --saveWorkspace -M MultiDimFit -d ws.root --saveFitResult --saveNLL --robustFit on || the_exit "failed to run combine"

PostFitShapesFromWorkspace -d $inDATACARD -w higgsCombineTest.MultiDimFit.mH120.root  -m 120 -f multidimfitTest.root:fit_mdf --postfit --print --output postfit.root || the_exit "PostFitShapeFromWorkspace failed to activate the command"
#root -b -q '../combineFRAG2_plot.C('$pEtaBin','$jEtaBin','$pPtBin',"'$_pEtaBinDesc_'","'$_jEtaBinDesc_'","'$_pPtRangeStr_'", "'$inputfile'")' || "combineFRAG2_plot failed to active the command"

