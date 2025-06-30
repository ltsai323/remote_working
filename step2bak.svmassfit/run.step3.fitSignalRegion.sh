histSOURCE_gjet=`realpath $1`
histSOURCE_btag=`realpath $2`
histSOURCE_cvsb=`realpath $3`
histSOURCE_cvsl=`realpath $4`
fitinfo=$5
testMODE=$6

function the_exit() { echo $1; exit; }

histSOURCE_gjet=`realpath $histSOURCE_gjet`
histSOURCE_btag=`realpath $histSOURCE_btag`
histSOURCE_cvsb=`realpath $histSOURCE_cvsb`
histSOURCE_cvsl=`realpath $histSOURCE_cvsl`


### Use sideband fit to extract the initial value of the C/B/L fractions
 ### [preprocess] prepare datacard and root files
 make_hist_source_and_datacard.py $histSOURCE_gjet
 make_hist_source_and_datacard.py $histSOURCE_btag
 make_hist_source_and_datacard.py $histSOURCE_cvsl
 make_hist_source_and_datacard.py $histSOURCE_cvsb
 combineCards.py \
   gjet=datacard_gjet.txt \
   btag=datacard_btag.txt \
   cvsl=datacard_cvsl.txt \
   cvsb=datacard_cvsb.txt \
   > datacards.txt
 

 echo $PWD
 ### [pre process] grab init values from sideband fitting.
 extract_data_entries.py \
   datacard_gjet.root 'gjet/data_obs' \
   bashvar_fitinit.sh \
   $fitinfo || the_exit "[Failed] extract_data_entries.py is not able to calculate init value from SB fitting"
 source ./bashvar_fitinit.sh # get bash variables

 ### [combine] create workspace for combine fitting
 text2workspace.py datacards.txt -o ws.root \
     -P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel \
     --PO "map=.*/ljet:nL[$initL,0.,$nDATA]" \
     --PO "map=.*/cjet:nC[$initC,0.,$nDATA]" \
     --PO "map=.*/bjet:nB[$initB,0.,$nDATA]" \
     --PO "map=.*/SB:nFAKE[$initFAKE,0.,$nDATA]" \
     --PO verbose || exit "failed to create workspace from datacard"
 
 ### [combine] apply simultaneous fit
 combine --saveWorkspace -M MultiDimFit -d ws.root --saveFitResult --saveNLL --robustFit on || the_exit "failed to run combine @ data sideband"

 
 ### [post process] collect result to yaml file
 extract_fit_value.py Allinfo \
   higgsCombineTest.MultiDimFit.mH120.root \
   fitinfo.signal_region.yaml

 ### ToDo: need to prepare the corrected datacard templates and run this file.
 PostFitShapesFromWorkspace -d datacards.txt \
     -w higgsCombineTest.MultiDimFit.mH120.root \
     -m 120 -f multidimfitTest.root:fit_mdf \
     --postfit --print --output postfit.root || the_exit "PostFitShapeFromWorkspace failed to activate the command"
