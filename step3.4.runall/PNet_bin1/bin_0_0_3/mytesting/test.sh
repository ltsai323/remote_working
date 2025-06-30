text2workspace.py datacards.txt -o ws.root \
   -P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel \
   --PO "map=.btag/ljet:frac_l[0.9,0.,1.]" \
   --PO "map=.cvsl/ljet:frac_l" \
   --PO "map=.cvsb/ljet:frac_l" \
   --PO "map=.btag/cjet:frac_c[0.1,0.,1.]" \
   --PO "map=.cvsl/cjet:frac_c" \
   --PO "map=.cvsb/cjet:frac_c" \
   --PO "map=.btag/bjet:frac_b[0.05,0.,1.]" \
   --PO "map=.cvsl/bjet:frac_b" \
   --PO "map=.cvsb/bjet:frac_b" \
   --PO verbose
   #--PO "map=.*/gjet:nSIGN[1801,0.,192968]" --PO verbose

combine --saveWorkspace -M MultiDimFit -d ws.root --saveFitResult --saveNLL --robustFit on
