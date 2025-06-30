### test fit for inclusive gjet, use rateParam instead of 2nd PO
text2workspace.py datacard_gjet_inclusive.txt -o ws.root \
   -P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel \
   --PO "map=.*/gjet:nSIGN[1801,0.,192968]" \
   --PO "extArgRatio:rRatio[8,0.,30.0]:nSIGN/val_SB" \
   --PO verbose

#combine --saveWorkspace -M MultiDimFit -d ws.root --saveFitResult --saveNLL --robustFit on


