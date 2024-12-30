#!/usr/bin/env python3

class xPhotonFiles:
    def __init__(self, fDATA, fSIGN, fFAKE):
        self.data = fDATA
        self.sign = fSIGN
        self.fake = fFAKE
    def __str__(self):
        return f'xPhotonFiles(\n  data={self.data}\n  sign={self.sign}\n  fake={self.fake}\n)'

def GetXPhotonFile(dataERA) -> xPhotonFiles:
    if dataERA == "UL2016PostVFP":
        return xPhotonFiles(
            '/home/ltsai/ReceivedFile/GJet/latestsample/UL2016PostVFP/data.root',
            '/home/ltsai/ReceivedFile/GJet/latestsample/UL2016PostVFP/sig.madgraph.root',
            '/home/ltsai/ReceivedFile/GJet/latestsample/UL2016PostVFP/qcd.madgraph.root',
            )
    raise NotImplementedError()

class EstimateSRFiles:
    def __init__(self, fDATAsigReg, fDATAsideband, fSIGN, fFAKE):
        self.dataSR = fDATAsigReg
        self.dataSB = fDATAsideband
        self.sign = fSIGN
        self.fake = fFAKE
def GetEstimateSRFile(dataERA) -> EstimateSRFiles:
    if dataERA == '2022EE':
        return EstimateSRFiles(
            '/data4/ltsai/ReceivedFile/2022EE_NanoAODv12/estimateSR/data_signalregion.root',
            '/data4/ltsai/ReceivedFile/2022EE_NanoAODv12/estimateSR/data_sideband.root',
            '/data4/ltsai/ReceivedFile/2022EE_NanoAODv12/estimateSR/sig_madgraph.root',
            '/data4/ltsai/ReceivedFile/2022EE_NanoAODv12/estimateSR/QCD_madgraph.root',
        )
    raise NotImplementedError()
