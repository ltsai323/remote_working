file_postfit=${1:-postfit.psuedodata.root}
### Set executable path and python library path
BASE_DIR=$PWD/
DIR_STEP33=$BASE_DIR/../step3.3.visualization
PATH=$DIR_STEP32:$PATH
PYTHONPATH=$DIR_STEP32:$PYTHONPATH


### step3.3
file_yaml_template=$DIR_STEP33/data/input.template.yaml
touch outputs ; /bin/rm -r outputs*; mkdir outputs

FILE_PLOTABLE=secondary_plotable.root
python3 $DIR_STEP33/secondary_plotable.py $file_postfit $FILE_PLOTABLE
python3 $DIR_STEP33/input_yaml_generator.py $file_yaml_template $FILE_PLOTABLE

DrawRatioPlotablesWithCMSFormat.py input.gjet.yaml
DrawRatioPlotablesWithCMSFormat.py input.btag.yaml
DrawRatioPlotablesWithCMSFormat.py input.cvsl.yaml
DrawRatioPlotablesWithCMSFormat.py input.cvsb.yaml
mv outputs outputs_psuedodata_generated

