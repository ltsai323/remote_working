#!/usr/bin/env python3

import ROOT
from array import array
import ExternalFileMgr


#outputFILE = 'WPeff_2022GJetMadgraph.root'
outputFILE = 'WPeff_2022GJetPythiaFlat.root'

class histCollection:
    def __init__(self):
        pass
    def WriteAllHists(self, fOUT):
        fOUT.cd()
        for hname, hinst in vars(self).items():
            hinst.Write()


def normhist(hist):
    newhist = hist.Clone()
    newhist.SetName( hist.GetName() + '_norm' )
    newhist.Scale(1./hist.Integral())
    return newhist
def TakeRatio(outHISTname, hUPPER, hLOWER):
    hU = hUPPER
    hL = hLOWER
    for ibin in range(1,hL.GetNbinsX()+2):
        if hL.GetBinContent(ibin) == 0: hL.SetBinContent(ibin, 1e-8)
    ratio = ROOT.TGraphAsymmErrors()
    ratio.SetName(outHISTname)
    ratio.Divide(hU,hL, 'pois')
    return ratio

def TakeNormedRatio(outHISTname, hUPPER, hLOWER):
    hU = hUPPER.Clone()
    hL = hLOWER.Clone()
    hU.SetName( hU.GetName() + '_norm' )
    hL.SetName( hL.GetName() + '_norm' )
    hU.Scale( 1./hU.Integral() )
    hL.Scale( 1./hL.Integral() )
    return TakeRatio(outHISTname, hU, hL)

def take_ratio_in_obj(obj, insU:str, insD:str, ratioNAME):
    hU = getattr(obj,insU)
    hD = getattr(obj,insD)


    ratio = TakeRatio(ratioNAME, hU.GetValue(), hD.GetValue())
    setattr(obj,ratioNAME, ratio)
    print(f'[GenerateRatio] {ratioNAME} generate from {hU.GetName()} / {hD.GetName()}')



if __name__ == "__main__":
    import sys
    pts_ = sys.argv[2:]

    dataERA = sys.argv[1]
    file = ExternalFileMgr.GetEstimateSRFile_GJetPythiaFlat(dataERA)
    the_sign = ROOT.RDataFrame('tree', file)
    df       = the_sign \
            .Filter("photon_pt>200") \
            .Define("bin00", "fabs(photon_eta)<1.5 && fabs(jet_eta)<1.5") \
            .Define("bin01", "fabs(photon_eta)<1.5 && fabs(jet_eta)>1.5") \
            .Define("bin10", "fabs(photon_eta)>1.5 && fabs(jet_eta)<1.5") \
            .Define("bin11", "fabs(photon_eta)>1.5 && fabs(jet_eta)>1.5") \
            .Define('WPc_loose' , 'ParTCvsL > 0.039 && ParTCvsB > 0.067' ) \
            .Define('WPc_medium', 'ParTCvsL > 0.117 && ParTCvsB > 0.128' ) \
            .Define('WPc_tight' , 'ParTCvsL > 0.358 && ParTCvsB > 0.095' ) \
            .Define('WPb_loose' , 'ParTB > 0.0897') \
            .Define('WPb_medium', 'ParTB > 0.4510') \
            .Define('WPb_tight' , 'ParTB > 0.8604') \
            .Define("C", "isHadFlvr_C == 1") \
            .Define("B", "isHadFlvr_B == 1") \
            .Define("L", "isHadFlvr_L == 1") \
            .Define("event_weight", "wgt") # gen weight, xs norm, PU weight, photon SF, trigger SF



    #out_file = ROOT.TFile(outputFILE, 'RECREATE')
    hists = histCollection()
    canv = ROOT.TCanvas("c","",500,500)



    #pts = [ 210,230,250,300,400,500,600,1000,1500 ]
    pts = [ int(pt) for pt in pts_ ]
    print(f'[PtSpectrum - GetWPeff] "{pts}"')
    #binpt = lambda hNAME: ROOT.ROOT.RDF.TH1DModel( hNAME, 'pt', len(pts)-1, array('f',pts) )
    def binpt(hNAME):
        print(f'[GenerateHist] {hNAME}')
        return ROOT.ROOT.RDF.TH1DModel( hNAME, 'pt', len(pts)-1, array('f',pts) )

    def get_effhists(hists, tag, df):
        setattr( hists, f'{tag}_all' , df                       .Histo1D(binpt(f'{tag}_all' ), 'photon_pt', 'event_weight') )
        setattr( hists, f'{tag}_WPcL', df.Filter('WPc_loose')   .Histo1D(binpt(f'{tag}_WPcL'), 'photon_pt', 'event_weight') )
        setattr( hists, f'{tag}_WPcM', df.Filter('WPc_medium')  .Histo1D(binpt(f'{tag}_WPcM'), 'photon_pt', 'event_weight') )
        setattr( hists, f'{tag}_WPcT', df.Filter('WPc_tight')   .Histo1D(binpt(f'{tag}_WPcT'), 'photon_pt', 'event_weight') )
        setattr( hists, f'{tag}_WPbL', df.Filter('WPb_loose')   .Histo1D(binpt(f'{tag}_WPbL'), 'photon_pt', 'event_weight') )
        setattr( hists, f'{tag}_WPbM', df.Filter('WPb_medium')  .Histo1D(binpt(f'{tag}_WPbM'), 'photon_pt', 'event_weight') )
        setattr( hists, f'{tag}_WPbT', df.Filter('WPb_tight')   .Histo1D(binpt(f'{tag}_WPbT'), 'photon_pt', 'event_weight') )

        ### remove weighting to check statistics in MC
        setattr( hists, f'{tag}_all_' , df                       .Histo1D(binpt(f'{tag}_all_' ), 'photon_pt') )
        setattr( hists, f'{tag}_WPcL_', df.Filter('WPc_loose')   .Histo1D(binpt(f'{tag}_WPcL_'), 'photon_pt') )
        setattr( hists, f'{tag}_WPcM_', df.Filter('WPc_medium')  .Histo1D(binpt(f'{tag}_WPcM_'), 'photon_pt') )
        setattr( hists, f'{tag}_WPcT_', df.Filter('WPc_tight')   .Histo1D(binpt(f'{tag}_WPcT_'), 'photon_pt') )
        setattr( hists, f'{tag}_WPbL_', df.Filter('WPb_loose')   .Histo1D(binpt(f'{tag}_WPbL_'), 'photon_pt') )
        setattr( hists, f'{tag}_WPbM_', df.Filter('WPb_medium')  .Histo1D(binpt(f'{tag}_WPbM_'), 'photon_pt') )
        setattr( hists, f'{tag}_WPbT_', df.Filter('WPb_tight')   .Histo1D(binpt(f'{tag}_WPbT_'), 'photon_pt') )

        take_ratio_in_obj(hists, f'{tag}_WPcL', f'{tag}_all', f'{tag}_WPcL_eff')
        take_ratio_in_obj(hists, f'{tag}_WPcM', f'{tag}_all', f'{tag}_WPcM_eff')
        take_ratio_in_obj(hists, f'{tag}_WPcT', f'{tag}_all', f'{tag}_WPcT_eff')
        take_ratio_in_obj(hists, f'{tag}_WPbL', f'{tag}_all', f'{tag}_WPbL_eff')
        take_ratio_in_obj(hists, f'{tag}_WPbM', f'{tag}_all', f'{tag}_WPbM_eff')
        take_ratio_in_obj(hists, f'{tag}_WPbT', f'{tag}_all', f'{tag}_WPbT_eff')

    get_effhists(hists, 'bin00L', df.Filter('bin00').Filter('L'))
    get_effhists(hists, 'bin00C', df.Filter('bin00').Filter('C'))
    get_effhists(hists, 'bin00B', df.Filter('bin00').Filter('B'))

    get_effhists(hists, 'bin01L', df.Filter('bin01').Filter('L'))
    get_effhists(hists, 'bin01C', df.Filter('bin01').Filter('C'))
    get_effhists(hists, 'bin01B', df.Filter('bin01').Filter('B'))

    get_effhists(hists, 'bin10L', df.Filter('bin10').Filter('L'))
    get_effhists(hists, 'bin10C', df.Filter('bin10').Filter('C'))
    get_effhists(hists, 'bin10B', df.Filter('bin10').Filter('B'))

    get_effhists(hists, 'bin11L', df.Filter('bin11').Filter('L'))
    get_effhists(hists, 'bin11C', df.Filter('bin11').Filter('C'))
    get_effhists(hists, 'bin11B', df.Filter('bin11').Filter('B'))


    f_out = ROOT.TFile(outputFILE, 'recreate')
    hists.WriteAllHists(f_out)
    f_out.Close()
