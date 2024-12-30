import ROOT

# Define a ROOT DataFrame
iFILE = '/data4/ltsai/ReceivedFile/2022EE_NanoAODv12/Run2022F.root'
df = ROOT.RDataFrame("Events", iFILE)

v = df.Max("nSV").GetValue()
print(f'[GetValue] maximum value of nSV is {v}')
