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

        for hname, hinst in vars(self).items():
            if writeOVERFLOWbin:
                max_bin = hinst.GetNbinsX()
                hinst.SetBinContent(1, hinst.GetBinContent(0) + hinst.GetBinContent(1) )
                hinst.SetBinContent(max_bin, hinst.GetBinContent(max_bin) + hinst.GetBinContent(max_bin+1) )

                hinst.SetBinContent(0, 0)
                hinst.SetBinContent(max_bin+1, 0)

            if writeNORMALIZEDhist:
                norm_name = hinst.GetName() + "_norm"
                hnorm = hinst.Clone(norm_name)
                hnorm.Scale(1./hnorm.Integral())
                setattr(self, hname+"_norm", hnorm)


        #fOUT.cd()
        base_dir = fOUT
        no_evt_dir = fOUT.GetDirectory("NO_EVT_WEIGHT")
        no_evt_dir = no_evt_dir if no_evt_dir else fOUT.mkdir("NO_EVT_WEIGHT")
        for hname, hinst in vars(self).items():
            if '_NO_EVT_WEIGHT' in hinst.GetName():
                no_evt_dir.cd()
            else:
                base_dir.cd()

            hinst.Write()





############ ploting ################
hBDTAll = lambda tag: ( f'{tag}_BDTAll', 'BDT Score', 40, -1.,1.)
hNOWGTBDTAll = lambda tag: ( f'{tag}_BDTAll_NO_EVT_WEIGHT', 'BDT Score', 40, -1.,1.)
hBDTAct = lambda tag: ( f'{tag}_BDTAct', 'BDT Score with SV constructed', 40, -1.,1.)

#hSVmAll = lambda tag: ( f'{tag}_SVmAll', 'SV mass including -1', 30, -1, 5 )
#hSVmAct = lambda tag: ( f'{tag}_SVmAct', 'SV mass with SV constructed', 25, 0, 5 )

#hSVmAll = lambda tag: ( f'{tag}_SVmAll', 'SV mass including -1', 45, -1, 8 )
#hSVmAct = lambda tag: ( f'{tag}_SVmAct', 'SV mass with SV constructed', 40, 0, 8 )

#hSVmAll = lambda tag: ( f'{tag}_SVmAll', 'SV mass including -1', 55, -1, 10 )
#hSVmAct = lambda tag: ( f'{tag}_SVmAct', 'SV mass with SV constructed', 50, 0, 10)

#hSVmAll = lambda tag: ( f'{tag}_SVmAll', 'SV mass including -1', 80, -1, 15 )
#hSVmAct = lambda tag: ( f'{tag}_SVmAct', 'SV mass with SV constructed', 75, 0, 15 )


## high bin
hSVmAll = lambda tag: ( f'{tag}_SVmAll', 'SV mass including -1', 60, -1, 5 )
hSVmAct = lambda tag: ( f'{tag}_SVmAct', 'SV mass with SV constructed', 50, 0, 5 )

#hSVmAll = lambda tag: ( f'{tag}_SVmAll', 'SV mass including -1', 90, -1, 8 )
#hSVmAct = lambda tag: ( f'{tag}_SVmAct', 'SV mass with SV constructed', 80, 0, 8 )

#hSVmAll = lambda tag: ( f'{tag}_SVmAll', 'SV mass including -1', 110, -1, 10 )
#hSVmAct = lambda tag: ( f'{tag}_SVmAct', 'SV mass with SV constructed', 100, 0, 10)

#hSVmAll = lambda tag: ( f'{tag}_SVmAll', 'SV mass including -1', 160, -1, 15 )
#hSVmAct = lambda tag: ( f'{tag}_SVmAct', 'SV mass with SV constructed', 150, 0, 15 )
hbtag = lambda tag: ( f'{tag}_btag', 'b tag score', 40, 0.,1.)
hcvsb = lambda tag: ( f'{tag}_cvsb', 'c vs b', 40, 0,1.)
hcvsl = lambda tag: ( f'{tag}_cvsl', 'c vs l', 40, 0.,1.)
hNOWGTbtag = lambda tag: ( f'{tag}_btag_NO_EVT_WEIGHT', 'b tag score', 40, 0.,1.)
hNOWGTcvsb = lambda tag: ( f'{tag}_cvsb_NO_EVT_WEIGHT', 'c vs b', 40, 0,1.)
hNOWGTcvsl = lambda tag: ( f'{tag}_cvsl_NO_EVT_WEIGHT', 'c vs l', 40, 0.,1.)

h2DcvsbANDcvsl = lambda tag: (f'{tag}_cvsbANDcvsl', 'X(cvsb) Y(cvsl)', 10,0,1, 10,0,1)
hNOWGT2DcvsbANDcvsl = lambda tag: (f'{tag}_cvsbANDcvsl_NO_EVT_WEIGHT', 'X(cvsb) Y(cvsl)', 10,0,1, 10,0,1)

DEFAULT_PHOPT_RANGE = [ 0, 1500 ]
DEFAULT_JETPT_RANGE = [ 0, 1500 ]
kPhoPt  = lambda n: ( f'kine_{n}_phopt' , 'kinematics checking', 128, DEFAULT_PHOPT_RANGE[0],DEFAULT_PHOPT_RANGE[1] ) # this should be modified at run time
kPhoEta = lambda n: ( f'kine_{n}_phoeta', 'kinematics checking', 128, -3, 3)
kPhoPhi = lambda n: ( f'kine_{n}_phophi', 'kinematics checking', 128, -3.5, 3.5)
kJetPt  = lambda n: ( f'kine_{n}_jetpt' , 'kinematics checking', 50, DEFAULT_JETPT_RANGE[0],DEFAULT_JETPT_RANGE[1] ) # this should be modified at run time
kJetEta = lambda n: ( f'kine_{n}_jeteta', 'kinematics checking', 128, -3, 3)
kJetPhi = lambda n: ( f'kine_{n}_jetphi', 'kinematics checking', 128, -3.5, 3.5)
kNJet   = lambda n: ( f'kine_{n}_njet'  , 'kinematics checking', 20, 0, 20)

hJetPt          = lambda n: (n,'jet Pt v.s. njet', 40, DEFAULT_JETPT_RANGE[0],DEFAULT_JETPT_RANGE[1] ) # this should be modified at run time
h2DJetPtANDnJet = lambda n: (n,'jet Pt v.s. njet', 40, DEFAULT_JETPT_RANGE[0],DEFAULT_JETPT_RANGE[1], 18,0,18) # this should be modified at run time
h3DPhoPtJetPtANDnJet= lambda n: (n,'3D(phoPT,jetPT,nJET)',
                                 40, DEFAULT_PHOPT_RANGE[0], DEFAULT_PHOPT_RANGE[1],
                                 40, DEFAULT_JETPT_RANGE[0],DEFAULT_JETPT_RANGE[1],
                                 18,0,18)

cutWPcANDfitbTag = True
cutWPANDfitSVMass = False





def _take_ratio_from_TH2(h2Dup,h2Ddn, newHISTname) -> ROOT.TH2F:
    ''' Use ROOT.TGraphAsymmErros.Divide(hUP,hDN,"POIS") to calculate division and error.
        Since ROOT.TGraphAsymmErrors.Divide() only supports TH1. Flatten the histogram to 1D and create TGraph
    '''

    th2_out = h2Dup.Clone(newHISTname)
    th2_out.Divide(h2Ddn)
    return th2_out
    
    def _flatten(th2, n) -> ROOT.TH1F:
        nbin2D = th2.FindBin(1e9,1e9) + 1 # find last bin idx +1 for tot number of bins
        nbin1D = nbin2D - 2 # remove overflow bin and underflow bin
        
        th1 = ROOT.TH1F(n, '', nbin1D, 0, nbin1D)
        for ibin in range(nbin2D): # including overflow and underflow bin
            binvalue = th2.GetBinContent(ibin)
            binerror = th2.GetBinError  (ibin)
            th1.SetBinContent(ibin, binvalue)
            th1.SetBinError  (ibin, binerror)
        return th1
    
    h1Dup = _flatten(h2Dup, 'tmpUP')
    h1Ddn = _flatten(h2Ddn, 'tmpDN')
    
    err_ratio = ROOT.TGraphAsymmErrors()
    err_ratio.SetName('tmpRATIO')
    err_ratio.Divide(h1Dup,h1Ddn,'pois')


    th2_out = h2Dup.Clone(newHISTname)
    nbin2d = th2_out.FindBin(1e9,1e9) + 1 # find last bin idx + 1 for total number of bins
    for ibin in range(nbin2d):
        val = err_ratio.GetPointY(ibin)
        err = err_ratio.GetErrorY(ibin)
        th2_out.SetBinContent(ibin,val)
        th2_out.SetBinError  (ibin,err)
    return th2_out



def _CreateJetPtSF_toTH1( usedDF, pETAbin,jETAbin,pPTlow,pPThigh):
    '''
    .. function:: CreateJetPtSF_toTH1(usedDF, createINTERMEDIATEhist=None)

   Creates scale factor histograms for jet transverse momentum (`jet_pt`) by comparing
   data to Monte Carlo (MC) simulations. It calculates two scale factor curves:
   one for data vs. GJet MC and another for data vs. (GJet + QCD) MC. The resulting
   graphs are saved into `sfhist_jetpt.root`.

   Optionally, if `createINTERMEDIATEhist` is set, intermediate histograms used in
   the computation are also saved to `fraghist_CreateJetPtSF_toTH1.root` for debugging.

   :param usedDF: A container object with attributes:
                  - `dfSR`: Data ROOT RDataFrame (for data)
                  - `dfsign`: Signal MC RDataFrame (GJet)
                  - `dffake`: Fake/QCD MC RDataFrame
   :type usedDF: object with .dfSR, .dfsign, .dffake (ROOT.RDataFrame)
   :param createINTERMEDIATEhist: Optional flag to trigger saving intermediate histograms.
   :type createINTERMEDIATEhist: bool or None
   :return: None
   :rtype: None

   :Output files:
     - `sfhist_jetpt.root`:
         - `sfjet_dataOVERGJet`: `TGraphAsymmErrors` of Data / GJet
         - `sfjet_dataOVERGJetandQCD`: `TGraphAsymmErrors` of Data / (GJet + QCD)
     - `fraghist_CreateJetPtSF_toTH1.root`: Optional output of intermediate histograms (if enabled)
    '''

    # create fragment histograms for reweight (jet PT)
    pt_data   = usedDF.dfSR  .Histo1D( hJetPt('hdata')  , 'jet_pt', 'event_weight').GetValue()
    pt_mcsign = usedDF.dfsign.Histo1D( hJetPt('hmcsign'), 'jet_pt', 'event_weight').GetValue()
    pt_mcfake = usedDF.dffake.Histo1D( hJetPt('hmcfake'), 'jet_pt', 'event_weight').GetValue()

    # create 2D fragment histograms for reweight (jet PT v.s. nJet)
    ptandnjet_data   = usedDF.dfSR  .Histo2D( h2DJetPtANDnJet('h2Ddata')  , 'jet_pt', 'jet_multiplicity', 'event_weight').GetValue()
    ptandnjet_mcsign = usedDF.dfsign.Histo2D( h2DJetPtANDnJet('h2Dmcsign'), 'jet_pt', 'jet_multiplicity', 'event_weight').GetValue()
    ptandnjet_mcfake = usedDF.dffake.Histo2D( h2DJetPtANDnJet('h2Dmcfake'), 'jet_pt', 'jet_multiplicity', 'event_weight').GetValue()
    for ibin in range(300):
        if pt_data  .GetBinContent(ibin+1) < 1e-8: pt_data  .SetBinContent(ibin+1, 1e-8)
        if pt_mcsign.GetBinContent(ibin+1) < 1e-8: pt_mcsign.SetBinContent(ibin+1, 1e-8)
        if pt_mcfake.GetBinContent(ibin+1) < 1e-8: pt_mcfake.SetBinContent(ibin+1, 1e-8)
    last_bin = ptandnjet_data.FindBin(1e9,1e9) + 1 # find last bin idx +1 for tot number of bins
    for ibin in range(last_bin): # including overflow bin and underflow bin
        if ptandnjet_data  .GetBinContent(ibin) < 1e-8: ptandnjet_data  .SetBinContent(ibin, 1e-8)
        if ptandnjet_mcsign.GetBinContent(ibin) < 1e-8: ptandnjet_mcsign.SetBinContent(ibin, 1e-8)
        if ptandnjet_mcfake.GetBinContent(ibin) < 1e-8: ptandnjet_mcfake.SetBinContent(ibin, 1e-8)

    print(f'[NbinsChecking] data({pt_data.GetNbinsX()}, sign({pt_mcsign.GetNbinsX()}), fake({pt_mcfake.GetNbinsX()})')


    pt_mc0 = pt_mcsign.Clone('hmc0')
    pt_mc1 = pt_mcsign.Clone('hmc1')
    pt_mc1.Add(pt_mcfake)



    ### calculate data / sign
    gerr0 = ROOT.TGraphAsymmErrors()
    gerr0.Divide( pt_data, pt_mc0, 'pois')
    gerr0.SetName('sfjet_dataOVERGJet')

    ### calculate data / sign+QCD
    gerr1 = ROOT.TGraphAsymmErrors()
    gerr1.Divide( pt_data, pt_mc1, 'pois')
    gerr1.SetName('sfjet_dataOVERGJetandQCD')

    th2ratio_2D = _take_ratio_from_TH2(ptandnjet_data, ptandnjet_mcsign, 'sfjetANDnjet_dataOVERGJet')



    sffile = ROOT.TFile(f'sfhist_jetpt__{pETAbin}_{jETAbin}_{pPTlow}_{pPThigh}.root', 'recreate')
    sffile.cd()
    gerr0.Write()
    gerr1.Write()
    th2ratio_2D.Write()

    ### fregment histograms
    pt_data.Write()
    pt_mcsign.Write()
    pt_mcfake.Write()
    pt_mc0.Write()
    pt_mc1.Write()

    ptandnjet_data.Write()
    ptandnjet_mcsign.Write()
    ptandnjet_mcfake.Write()
    sffile.Close()
def CreateJetPtSF_toTH1( usedDF, pETAbin,jETAbin,pPTlow,pPThigh):
    '''
    .. function:: CreateJetPtSF_toTH1(usedDF, createINTERMEDIATEhist=None)

   Creates scale factor histograms for jet transverse momentum (`jet_pt`) by comparing
   data to Monte Carlo (MC) simulations. It calculates two scale factor curves:
   one for data vs. GJet MC and another for data vs. (GJet + QCD) MC. The resulting
   graphs are saved into `sfhist_jetpt.root`.

   Optionally, if `createINTERMEDIATEhist` is set, intermediate histograms used in
   the computation are also saved to `fraghist_CreateJetPtSF_toTH1.root` for debugging.

   :param usedDF: A container object with attributes:
                  - `dfSR`: Data ROOT RDataFrame (for data)
                  - `dfsign`: Signal MC RDataFrame (GJet)
                  - `dffake`: Fake/QCD MC RDataFrame
   :type usedDF: object with .dfSR, .dfsign, .dffake (ROOT.RDataFrame)
   :param createINTERMEDIATEhist: Optional flag to trigger saving intermediate histograms.
   :type createINTERMEDIATEhist: bool or None
   :return: None
   :rtype: None

   :Output files:
     - `sfhist_jetpt.root`:
         - `sfjet_dataOVERGJet`: `TGraphAsymmErrors` of Data / GJet
         - `sfjet_dataOVERGJetandQCD`: `TGraphAsymmErrors` of Data / (GJet + QCD)
     - `fraghist_CreateJetPtSF_toTH1.root`: Optional output of intermediate histograms (if enabled)
    '''

    # create fragment histograms for reweight (jet PT)
    pt_data   = usedDF.dfSR  .Histo1D( hJetPt('hdata')  , 'jet_pt', 'event_weight').GetValue()
    pt_mcsign = usedDF.dfsign.Histo1D( hJetPt('hmcsign'), 'jet_pt', 'event_weight').GetValue()
    pt_mcfake = usedDF.dffake.Histo1D( hJetPt('hmcfake'), 'jet_pt', 'event_weight').GetValue()

    # create 2D fragment histograms for reweight (jet PT v.s. nJet)
    ptandnjet_data   = usedDF.dfSR  .Histo2D( h2DJetPtANDnJet('h2Ddata')  , 'jet_pt', 'jet_multiplicity', 'event_weight').GetValue()
    ptandnjet_mcsign = usedDF.dfsign.Histo2D( h2DJetPtANDnJet('h2Dmcsign'), 'jet_pt', 'jet_multiplicity', 'event_weight').GetValue()
    ptandnjet_mcfake = usedDF.dffake.Histo2D( h2DJetPtANDnJet('h2Dmcfake'), 'jet_pt', 'jet_multiplicity', 'event_weight').GetValue()
    for ibin in range(300):
        if pt_data  .GetBinContent(ibin+1) < 1e-8: pt_data  .SetBinContent(ibin+1, 1e-8)
        if pt_mcsign.GetBinContent(ibin+1) < 1e-8: pt_mcsign.SetBinContent(ibin+1, 1e-8)
        if pt_mcfake.GetBinContent(ibin+1) < 1e-8: pt_mcfake.SetBinContent(ibin+1, 1e-8)
    last_bin = ptandnjet_data.FindBin(1e9,1e9) + 1 # find last bin idx +1 for tot number of bins
    for ibin in range(last_bin): # including overflow bin and underflow bin
        if ptandnjet_data  .GetBinContent(ibin) < 1e-8: ptandnjet_data  .SetBinContent(ibin, 1e-8)
        if ptandnjet_mcsign.GetBinContent(ibin) < 1e-8: ptandnjet_mcsign.SetBinContent(ibin, 1e-8)
        if ptandnjet_mcfake.GetBinContent(ibin) < 1e-8: ptandnjet_mcfake.SetBinContent(ibin, 1e-8)
    # create 3D fragment histograms for reweight (pho PT v.s. jet PT v.s. nJet)
    phoptjetptandnjet_data   = usedDF.dfSR  .Histo3D( h3DPhoPtJetPtANDnJet('h3Ddata')  , 'photon_pt', 'jet_pt', 'jet_multiplicity', 'event_weight').GetValue()
    phoptjetptandnjet_mcsign = usedDF.dfsign.Histo3D( h3DPhoPtJetPtANDnJet('h3Dmcsign'), 'photon_pt', 'jet_pt', 'jet_multiplicity', 'event_weight').GetValue()
    phoptjetptandnjet_mcfake = usedDF.dffake.Histo3D( h3DPhoPtJetPtANDnJet('h3Dmcfake'), 'photon_pt', 'jet_pt', 'jet_multiplicity', 'event_weight').GetValue()
    last_bin = phoptjetptandnjet_data.FindBin(1e9,1e9,1e9) + 1 # find last bin idx +1 for tot number of bins
    for ibin in range(last_bin): # including overflow bin and underflow bin
        if ptandnjet_data  .GetBinContent(ibin) < 1e-8: ptandnjet_data  .SetBinContent(ibin, 1e-8)
        if ptandnjet_mcsign.GetBinContent(ibin) < 1e-8: ptandnjet_mcsign.SetBinContent(ibin, 1e-8)
        if ptandnjet_mcfake.GetBinContent(ibin) < 1e-8: ptandnjet_mcfake.SetBinContent(ibin, 1e-8)

    print(f'[NbinsChecking] data({pt_data.GetNbinsX()}, sign({pt_mcsign.GetNbinsX()}), fake({pt_mcfake.GetNbinsX()})')


    pt_mc0 = pt_mcsign.Clone('hmc0')
    pt_mc1 = pt_mcsign.Clone('hmc1')
    pt_mc1.Add(pt_mcfake)



    ### calculate data / sign
    gerr0 = ROOT.TGraphAsymmErrors()
    gerr0.Divide( pt_data, pt_mc0, 'pois')
    gerr0.SetName('sfjet_dataOVERGJet')

    ### calculate data / sign+QCD
    gerr1 = ROOT.TGraphAsymmErrors()
    gerr1.Divide( pt_data, pt_mc1, 'pois')
    gerr1.SetName('sfjet_dataOVERGJetandQCD')

    th2ratio_2D = _take_ratio_from_TH2(ptandnjet_data, ptandnjet_mcsign, 'sfjetANDnjet_dataOVERGJet')
    th3ratio_3D = _take_ratio_from_TH2(phoptjetptandnjet_data, phoptjetptandnjet_mcsign, 'sfphoptjetptANDnjet_dataOVERGJet')



    sffile = ROOT.TFile(f'sfhist_jetpt__{pETAbin}_{jETAbin}_{pPTlow}_{pPThigh}.root', 'recreate')
    sffile.cd()
    gerr0.Write()
    gerr1.Write()
    th2ratio_2D.Write()
    th3ratio_3D.Write()

    ### fregment histograms
    pt_data.Write()
    pt_mcsign.Write()
    pt_mcfake.Write()
    pt_mc0.Write()
    pt_mc1.Write()

    ptandnjet_data.Write()
    ptandnjet_mcsign.Write()
    ptandnjet_mcfake.Write()

    phoptjetptandnjet_data.Write()
    phoptjetptandnjet_mcsign.Write()
    phoptjetptandnjet_mcfake.Write()
    sffile.Close()


def LoadAdditionalFunc():
    '''
    .. function:: LoadAdditionalFunc()

   Loads the external C++ header file `makehisto_additional_functions.h` into the ROOT
   interpreter using `ROOT.gInterpreter.Declare`. This header must define functions
   such as `pt_sfGJet` and `pt_sfGJetandQCD`, which are required by event weight
   reweighting routines.

   This function should be called before using:
   - :func:`UpdateEvtWeight_ReweightJetPtFromGJet`
   - :func:`UpdateEvtWeight_ReweightJetPtFromGJetandQCD`

   :return: None
   :rtype: None
   '''
    ROOT.gInterpreter.Declare('#include "makehisto_additional_functions.h"')

def UpdateEvtWeight_ReweightJetPtFromGJet(df, pETAbin,jETAbin,pPTlow,pPThigh, makehistoADDITIONALfunctions_LOADED = False):
    '''
    .. function:: UpdateEvtWeight_ReweightJetPtFromGJet(df, makehistoADDITIONALfunctions_LOADED=False)

   Applies a reweighting scale factor to the event weight in a ROOT RDataFrame using
   the GJet-derived jet transverse momentum scale factor (`pt_sfGJet`).

   This function requires that the `makehisto_additional_functions.h` header is loaded
   via `LoadAdditionalFunc()` before execution.

   :param df: A ROOT RDataFrame object containing `jet_pt` and `event_weight` columns.
   :type df: ROOT.RDataFrame
   :param makehistoADDITIONALfunctions_LOADED: Indicates whether the required header
       with `pt_sfGJet()` function is already loaded.
   :type makehistoADDITIONALfunctions_LOADED: bool
   :raises IOError: If `makehisto_additional_functions.h` has not been loaded prior.
   :return: A modified ROOT RDataFrame with:
             - `jetpt_sf`: scale factor based on jet_pt,
             - `event_weight_orig`: original event weight,
             - `event_weight`: redefined as `jetpt_sf * event_weight`.
   :rtype: ROOT.RDataFrame
   '''
    if makehistoADDITIONALfunctions_LOADED == False:
        raise IOError('[LoadHeaderFile] UpdateEvtWeight_ReweightJetPtFromGJet() require you load makehisto_additional_functions.h by LoadAdditionalFunc()')

    # use 2D jet pt & nJet sf
    #d = df.Define( 'jetpt_sf',  f"ptANDnjet_sfGJet(jet_pt,jet_multiplicity,{pETAbin},{jETAbin},{pPTlow},{pPThigh})" )
    d = df.Define( 'jetpt_sf',  f"phoptjetptANDnjet_sfGJet(photon_pt,jet_pt,jet_multiplicity,{pETAbin},{jETAbin},{pPTlow},{pPThigh})" )
    # use 1D jet pt Sf
    # d = df.Define( 'jetpt_sf',  f"pt_sfGJet(jet_pt,{pETAbin},{jETAbin},{pPTlow},{pPThigh})" )
    sum_of_jet_sf_norm = d.Define('jetptsfANDevtwgt','jetpt_sf * event_weight').Sum('jetptsfANDevtwgt').GetValue()
    sum_of_evtwgt_norm = d.Sum('event_weight').GetValue()
    jet_sf_norm = sum_of_evtwgt_norm / sum_of_jet_sf_norm

    return d \
            .Define('event_weight_jetsf', f'jetpt_sf * {jet_sf_norm}') \
            .Define( 'event_weight_orig', 'event_weight') \
            .Redefine('event_weight', 'event_weight_jetsf * event_weight')
def UpdateEvtWeight_ReweightJetPtFromGJetandQCD(df, makehistoADDITIONALfunctions_LOADED = False):
    '''
    .. function:: UpdateEvtWeight_ReweightJetPtFromGJetandQCD(df, makehistoADDITIONALfunctions_LOADED=False)

   Redefines event weights in a ROOT DataFrame based on jet transverse momentum (jet_pt)
   by applying a scale factor from the `pt_sfGJetandQCD` function. Requires external C++
   header `makehisto_additional_functions.h` to be loaded beforehand.

   :param df: A ROOT RDataFrame object containing the jet_pt and event_weight columns.
   :type df: ROOT.RDataFrame
   :param makehistoADDITIONALfunctions_LOADED: Boolean flag indicating whether the
       required C++ header with pt_sfGJetandQCD() has been loaded.
   :type makehistoADDITIONALfunctions_LOADED: bool
   :raises IOError: If `makehisto_additional_functions.h` has not been loaded.
   :return: The modified ROOT RDataFrame with added `jetpt_sf`, `event_weight_orig`,
            and redefined `event_weight`.
   :rtype: ROOT.RDataFrame
   '''
    if makehistoADDITIONALfunctions_LOADED == False:
        raise IOError('[LoadHeaderFile] UpdateEvtWeight_ReweightJetPtFromGJetandQCD() require you load makehisto_additional_functions.h by LoadAdditionalFunc()')

    return df.Define( 'jetpt_sf',  "pt_sfGJetandQCD(jet_pt)" ) \
             .Define( 'event_weight_orig', 'event_weight') \
             .Redefine('event_weight', 'jetpt_sf * event_weight')


def Define_NormalizeBTagSF(df, bSFcolumn, outCOLname) -> tuple:
    '''
    .. function: Define_NormalizedEventWeight(df, bSFcolumn:str)
    # returned value : 0.weightName 1.updated dataframe

    According to BTV group, the applied scale factor should not change the integrations.
    Such as a normalization required on btagging sf.

    The formula: SIGMA_i( w^orig_i ) / SIGMA_i( w^orig_i * bSF_i )
    '''
    columnname_tmp = f'_wgt_{bSFcolumn}'
    d = df.Define(columnname_tmp, f'event_weight*{bSFcolumn}')
    integral_wgt = d.Sum('event_weight').GetValue()
    integral_wgt_with_bSF = d.Sum(columnname_tmp).GetValue()
    renorm = integral_wgt / integral_wgt_with_bSF
    print(f'renorm = {renorm}')

    columnname_new = outCOLname
    return d.Define(columnname_new, f'{columnname_tmp} * {renorm}')

evtwgt_WPbLCentral = 'evtwgt_WPbLCentral'
evtwgt_SFcShapeCentral = 'evtwgt_SFcShapeCentral'

def _hist_shape(histPOOL, name):
    h = getattr(histPOOL, name)
    h.SetName(name)
    # scale afterhand
    #if h.Integral() < 1e-8: return
    #h.Scale(1./h.Integral())
