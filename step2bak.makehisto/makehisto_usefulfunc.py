#!/usr/bin/env python3

#def Binning(df, pETAbin, jETAbin, pPTlow, pPThigh=-1):
#    ### if pPThigh < 0, disable the upper bond of photon pt
#    phoEtaCut = 'fabs(photon_eta)<1.5' if pETAbin == 0 else 'fabs(photon_eta)>1.5'
#    jetEtaCut = 'fabs(jet_eta)<1.5 && jet_pt>0' if jETAbin == 0 else 'fabs(jet_eta)>1.5 && jet_pt>0'
#    phoPtCut = f'photon_pt>{pPTlow} && photon_pt<{pPThigh}' if pPThigh > 0 else f'photon_pt>{pPTlow}'
#    return df.Filter( '&&'.join([phoEtaCut,jetEtaCut, phoPtCut]) )

import ROOT


class UsedDataFrames:
    def __init__(self,
                 dataFILE,
                 signFILE,
                 fakeFILE,
                 sidebandFILE,
                 ):
        self.dfSR = ROOT.RDataFrame('tree',dataFILE)
        self.dfsign = ROOT.RDataFrame('tree', signFILE)
        self.dffake = ROOT.RDataFrame('tree', fakeFILE)
        self.dfSB = ROOT.RDataFrame('tree', sidebandFILE)


class histCollection:
    def __init__(self):
        pass
    def WriteAllHists(self, fOUT,
                      writeNORMALIZEDhist = False,
                      writeOVERFLOWbin = False,
                      ):
        fOUT.cd()
        for hname, hinst in vars(self).items():
            if writeOVERFLOWbin:
                '''
                Append overflow bin to last bin and set overflow bin as 0
                Append underflowflow bin to first bin and set underflow bin as 0
                '''
                max_bin = hinst.GetNbinsX()
                hinst.SetBinContent(1, hinst.GetBinContent(0) + hinst.GetBinContent(1) )
                hinst.SetBinContent(max_bin, hinst.GetBinContent(max_bin) + hinst.GetBinContent(max_bin+1) )

                ## reset overflow and underflow bins
                hinst.SetBinContent(0, 0)
                hinst.SetBinContent(max_bin+1, 0)
            hinst.Write()

            if writeNORMALIZEDhist:
                norm_name = hinst.GetName() + "_norm"
                hnorm = hinst.Clone(norm_name)
                hnorm.Scale(1./hnorm.Integral())
                hnorm.Write()




############ ploting ################
hBDTAll = lambda tag: ( f'{tag}_BDTAll', 'BDT Score', 40, -1.,1.)
hBDTAct = lambda tag: ( f'{tag}_BDTAct', 'BDT Score with SV constructed', 40, -1.,1.)

hSVmAll = lambda tag: ( f'{tag}_SVmAll', 'SV mass including -1', 30, -1, 5 )
hSVmAct = lambda tag: ( f'{tag}_SVmAct', 'SV mass with SV constructed', 25, 0, 5 )

#hSVmAll = lambda tag: ( f'{tag}_SVmAll', 'SV mass including -1', 45, -1, 8 )
#hSVmAct = lambda tag: ( f'{tag}_SVmAct', 'SV mass with SV constructed', 40, 0, 8 )

#hSVmAll = lambda tag: ( f'{tag}_SVmAll', 'SV mass including -1', 55, -1, 10 )
#hSVmAct = lambda tag: ( f'{tag}_SVmAct', 'SV mass with SV constructed', 50, 0, 10)

#hSVmAll = lambda tag: ( f'{tag}_SVmAll', 'SV mass including -1', 80, -1, 15 )
#hSVmAct = lambda tag: ( f'{tag}_SVmAct', 'SV mass with SV constructed', 75, 0, 15 )


### high bin
#hSVmAll = lambda tag: ( f'{tag}_SVmAll', 'SV mass including -1', 60, -1, 5 )
#hSVmAct = lambda tag: ( f'{tag}_SVmAct', 'SV mass with SV constructed', 50, 0, 5 )

#hSVmAll = lambda tag: ( f'{tag}_SVmAll', 'SV mass including -1', 90, -1, 8 )
#hSVmAct = lambda tag: ( f'{tag}_SVmAct', 'SV mass with SV constructed', 80, 0, 8 )

#hSVmAll = lambda tag: ( f'{tag}_SVmAll', 'SV mass including -1', 110, -1, 10 )
#hSVmAct = lambda tag: ( f'{tag}_SVmAct', 'SV mass with SV constructed', 100, 0, 10)

#hSVmAll = lambda tag: ( f'{tag}_SVmAll', 'SV mass including -1', 160, -1, 15 )
#hSVmAct = lambda tag: ( f'{tag}_SVmAct', 'SV mass with SV constructed', 150, 0, 15 )
hbtag = lambda tag: ( f'{tag}_btag', 'b tag score', 40, 0.,1.)
hcvsb = lambda tag: ( f'{tag}_cvsb', 'c vs b', 40, 0,1.)
hcvsl = lambda tag: ( f'{tag}_cvsl', 'c vs l', 40, 0.,1.)
