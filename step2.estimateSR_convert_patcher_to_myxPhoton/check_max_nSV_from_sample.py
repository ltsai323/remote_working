import ROOT

# Define a ROOT DataFrame
iFILE = '/data4/ltsai/ReceivedFile/2022EE_NanoAODv12/Run2022F.root'
iFILE = '/data4/ltsai/ReceivedFile/2022EE_NanoAODv12/QCD4JetsMadgraph_200to400.root'
iFILE = '/data4/ltsai/ReceivedFile/2022EE_NanoAODv12/QCD4JetsMadgraph_1500to2000.root'
df = ROOT.RDataFrame("Events", iFILE)

vv = df.Max("Jet_nSVs").GetValue()
vvv = df.Define("leadjet_nSV", "Jet_nSVs[0]").Max("leadjet_nSV").GetValue()
v = df.Max("nSV").GetValue()
print(f'[GetValue] maximum value of nSV is {v}, and Jet_nSV = {vv}, leading jet nSV = {vvv}')
