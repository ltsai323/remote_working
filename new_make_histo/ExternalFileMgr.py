#!/usr/bin/env python3


def GetXPhotonFile(dataERA):
    if dataERA == "UL2016PostVFP":
        return {
            'data': '/home/ltsai/ReceivedFile/GJet/latestsample/UL2016PostVFP/data.root',
            'sign': '/home/ltsai/ReceivedFile/GJet/latestsample/UL2016PostVFP/sig.madgraph.root',
            'fake': '/home/ltsai/ReceivedFile/GJet/latestsample/UL2016PostVFP/qcd.madgraph.root',
        }
