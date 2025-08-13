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
                max_bin = hinst.GetNbinsX()
                hinst.SetBinContent(1, hinst.GetBinContent(0) + hinst.GetBinContent(1) )
                hinst.SetBinContent(max_bin, hinst.GetBinContent(max_bin) + hinst.GetBinContent(max_bin+1) )

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



cutWPcANDfitbTag = True
cutWPANDfitSVMass = False




def CreateJetPtSF_toTH1( usedDF, createINTERMEDIATEhist=None ):
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
    pt_data = usedDF.dfSR.Histo1D('jet_pt', 'event_weight').Clone('hdata')
    nbin = pt_data.GetNbinsX()
    xmin = pt_data.GetBinLowEdge(1)
    xmax = pt_data.GetBinLowEdge(nbin+1)


    ### use the same binning for histograms
    pt_mcsign = usedDF.dfsign.Histo1D( ('hmcsign','', nbin, xmin,xmax), 'jet_pt', 'event_weight').GetValue()
    pt_mcfake = usedDF.dffake.Histo1D( ('hmcfake','', nbin, xmin,xmax), 'jet_pt', 'event_weight').GetValue()

    pt_mc0 = pt_mcsign.Clone('hmc0')
    pt_mc1 = pt_mcsign.Clone('hmc1')
    pt_mc1.Add(pt_mcfake)

    ### rebin hist
    pt_data.Rebin(4)
    pt_mc0.Rebin(4)
    pt_mc1.Rebin(4)


    ### calculate data / sign
    gerr0 = ROOT.TGraphAsymmErrors()
    gerr0.Divide( pt_data, pt_mc0, 'pois')
    gerr0.SetName('sfjet_dataOVERGJet')

    ### calculate data / sign+QCD
    gerr1 = ROOT.TGraphAsymmErrors()
    gerr1.Divide( pt_data, pt_mc1, 'pois')
    gerr1.SetName('sfjet_dataOVERGJetandQCD')



    sffile = ROOT.TFile('sfhist_jetpt.root', 'recreate')
    sffile.cd()
    gerr0.Write()
    gerr1.Write()
    sffile.Close()

    if createINTERMEDIATEhist is not None:
        intermediatefile = 'fraghist_CreateJetPtSF_toTH1.root'
        f = ROOT.TFile(intermediatefile, 'recreate')
        f.cd()
        pt_data.Write()
        pt_mcsign.Write()
        pt_mcfake.Write()
        pt_mc0.Write()
        pt_mc1.Write()
        f.Close()
        print(f'[ROOTGenerated] CreateJetPtSF_toTH1() generates {intermediatefile} for checking intermediate histograms.')

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

def UpdateEvtWeight_ReweightJetPtFromGJet(df, makehistoADDITIONALfunctions_LOADED = False):
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

    return df.Define( 'jetpt_sf',  "pt_sfGJet(jet_pt)" ) \
             .Define( 'event_weight_orig', 'event_weight') \
             .Redefine('event_weight', 'jetpt_sf * event_weight')
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
    .. function: Define_NormalizeBTagSF(df, bSFcolumn:str)
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
