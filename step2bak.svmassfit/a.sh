text2workspace.py $(_TMP_DATACARD) -o $(_TMP_INPUT_WORKSPACE) \
    	-P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel \
    	--PO "map=.*/Ljet:rL[1.0,0.,10.0]" \
    	--PO "map=.*/Cjet:rC[1.0,0.,10.0]" \
    	--PO "map=.*/Bjet:rB[1.0,0.,10.0]" \
    	--PO verbose || (echo "failed to create workspace from datacard"; exit 1)

combine --saveWorkspace -M MultiDimFit -d $(_TMP_INPUT_WORKSPACE) --saveFitResult --saveNLL --robustFit on || the_exit "failed to run combine @ data sideband"
