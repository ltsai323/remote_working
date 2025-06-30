#!/usr/bin/env python3
import logging

log = logging.getLogger(__name__)

import ROOT

iFILEname = 'aaa.root'

def modify_hist(iFILEname:str, oFILEname:str, histMODIFYfunc):
    log.debug(f'[LoadROOTFile] Load {iFILEname}')
    iFILE = ROOT.TFile.Open(iFILEname)

    oFILE = ROOT.TFile(oFILEname, 'recreate')
    oFILE.cd()
    for dirkey in iFILE.GetListOfKeys():
        log.debug(f'[AccessDir] {dirkey.GetName()} in ROOT file')
        oDIR = oFILE.mkdir(dirkey.GetName())
        oDIR.cd()

        iDIR = iFILE.Get( dirkey.GetName() )
        for histkey in iDIR.GetListOfKeys():
            log.debug(f'[AccessHist] {histkey.GetName()} in directory')
            hist = iDIR.Get(histkey.GetName())
            h_out = histMODIFYfunc(hist)
            h_out.Write()
        oDIR.Write()
        oFILE.cd()
    oFILE.Close()
    log.info(f'[ROOTGenerated] output file {oFILEname} generated')


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
        format='[basicCONFIG] %(levelname)s - %(message)s',
        datefmt='%H:%M:%S')

    import sys
    ifilename = sys.argv[1]
    ofilename = sys.argv[2]
    fakeINTEGRAL = float(sys.argv[3])


    def modifyFUNC(inHIST):
        if inHIST.GetName() != 'fake': return inHIST
        log.info(f'[ModifyContent] hist:{inHIST.GetName()} modify integration from {inHIST.Integral()} to {fakeINTEGRAL}')

        inHIST.Scale( fakeINTEGRAL/inHIST.Integral() )
        return inHIST
    modify_hist(
            ifilename,
            ofilename,
            modifyFUNC
            )
