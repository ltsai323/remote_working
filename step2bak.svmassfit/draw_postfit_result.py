#!/usr/bin/env python3

import ROOT

def LOG(*args):
    print('[check.ctaggingVars-LOG] ', *args)
printbug = False
def BUG(*args):
    if printbug:
        print('[check.ctaggingVars-BUGGING] ', *args)



def GetHist(
    iFILE:ROOT.TFile, histNAME:str,
    lineCOLOR:int = 2,
    lineWIDTH:int = 0,
    fillCOLOR:int = 0,
    fillSTYLE:int = 1,
    markerCOLOR:int = 1,
    markerSTYLE:int = 33,
    markerSIZE:int = 0,
    xAXISname:str = '',
    ):
    LOG(f'GetHist() : Loading {histNAME}')
    h = iFILE.Get(histNAME)
    h.SetLineColor(lineCOLOR)
    h.SetLineWidth(lineWIDTH)
    h.SetFillColor(fillCOLOR)
    h.SetFillStyle(fillSTYLE)

    h.SetMarkerColor(markerCOLOR)
    h.SetMarkerStyle(markerSTYLE)
    h.SetMarkerSize(markerSIZE)

    if xAXISname == 'hist.GetTitle()':
        h.GetXaxis().SetTitle(h.GetTitle())
    else:
        h.GetXaxis().SetTitle(xAXISname)

    return h



class CommonVars:
    def __init__(self, inFILE, numPLOTs = 1):
        self.ifile = inFILE

        from xPhoton.analysis.MyCanvas import MassiveRatioCanvasSetup
        self.canv, self.allpads = MassiveRatioCanvasSetup(numRATIOplot=numPLOTs)
        self.drawables = {}


    def SetDiJetYield(self, bkgYIELD):
        self.fake_yield = bkgYIELD
    def SetBinDesc(self, *bins):
        self.pEtaDesc, self.jEtaDesc, self.pPtDesc = bins
    def SetCurrentPad(self, padIDX):
        if padIDX >= len(self.allpads): raise OverflowError(
                f'SetCurrentPad():: input idx {padIDX} is larger than pads length {len(self.allpads)}')
        self.upperpad = self.allpads[padIDX][0]
        self.lowerpad = self.allpads[padIDX][1]
    def keep_drawing_obj(self, label, drawABLEs):
        self.drawables[label] = drawABLEs
    def get_bin_desc(self):
        return ','.join([self.pEtaDesc,self.jEtaDesc,self.pPtDesc])

class CurrentDrawings:
    outTag = ''
    hdata = None
    hsign = None
    hfake = None
    useLogScale = False
    legTitle = ''




def merge_hist(newname, hists):
    h = hists[0].Clone()
    h.SetName(newname)

    hists.pop(0)
    for hist in hists: h.Add(hist)
    return h

def scale_hist_according_to_dijet_fit_yield(hDATA, hSIGN, hFAKE, dijetFITyield):
    yield_fake = dijetFITyield
    yield_sign = hDATA.Integral() - yield_fake
    hFAKE.Scale(yield_fake / hFAKE.Integral())
    hSIGN.Scale(yield_sign / hSIGN.Integral())
def scale_hist_according_to_k_factor(hDATA, hSIGN, hFAKE, fakeORIGyield):
    the_factor = round(hDATA.Integral() / (hSIGN.Integral()+fakeORIGyield),2)
    print(f'[BUGGING] tunned scale factor : {the_factor}')
    hSIGN.Scale(the_factor)
    hFAKE.Scale(the_factor * fakeORIGyield / hFAKE.Integral())
    return the_factor

def drawhist1_ctag_var_calb(folderNAME:str, commonobj:CommonVars, jettagIDX:int):
    inFILE = commonobj.ifile
    jet_tag_names = ['bScore', 'CvsL', 'CvsB']

    varName = f'jettag{jettagIDX:d}'
    xAxisName = jet_tag_names[jettagIDX]
    hdata = GetHist(inFILE,f'{folderNAME}/{varName}_data_signalRegion',
                    markerCOLOR=1, markerSIZE=2, xAXISname=xAxisName)
    hsign1= GetHist(inFILE,f'{folderNAME}/{varName}_gjet_GJetsL_signalRegion_central',
                    lineCOLOR=1 , lineWIDTH=2, fillCOLOR=2 , fillSTYLE=1001, xAXISname=xAxisName)
    hsign2= GetHist(inFILE,f'{folderNAME}/{varName}_gjet_GJetsC_signalRegion_central',
                    lineCOLOR=1 , lineWIDTH=2, fillCOLOR=2 , fillSTYLE=1001, xAXISname=xAxisName)
    hsign3= GetHist(inFILE,f'{folderNAME}/{varName}_gjet_GJetsB_signalRegion_central',
                    lineCOLOR=1 , lineWIDTH=2, fillCOLOR=2 , fillSTYLE=1001, xAXISname=xAxisName)
    hfake1= GetHist(inFILE,f'{folderNAME}/{varName}_QCD_DiJetL_signalRegion_central',
                    lineCOLOR=1 , lineWIDTH=2, fillCOLOR=38, fillSTYLE=1001, xAXISname=xAxisName)
    hfake2= GetHist(inFILE,f'{folderNAME}/{varName}_QCD_DiJetC_signalRegion_central',
                    lineCOLOR=1 , lineWIDTH=2, fillCOLOR=38, fillSTYLE=1001, xAXISname=xAxisName)
    hfake3= GetHist(inFILE,f'{folderNAME}/{varName}_QCD_DiJetB_signalRegion_central',
                    lineCOLOR=1 , lineWIDTH=2, fillCOLOR=38, fillSTYLE=1001, xAXISname=xAxisName)
    hside = GetHist(inFILE,f'{folderNAME}/{varName}_data_dataSideband',
                    lineCOLOR=1 , lineWIDTH=2, fillCOLOR=38, fillSTYLE=1001, xAXISname=xAxisName)
    hsign = merge_hist(f'{varName}_gjet_signalRegion_central', [hsign1,hsign2,hsign3])
    #hfake = merge_hist(f'{varName}_QCD_signalRegion_central',  [hfake1,hfake2,hfake3])
    hfake = hfake1.Clone(f'{varName}_QCD_signalRegion_central')
    hfake.Add(hfake2)
    hfake.Add(hfake3)

    scale_hist_according_to_dijet_fit_yield(hdata,hsign,hside, commonobj.fake_yield)
    hdata.SetTitle( 'data in 19.52 fb^{-1}')
    hsign.SetTitle(f'gjet MC {hsign.Integral():.1f}')
    hside.SetTitle(f'di-jet {hside.Integral():.1f}')


    output = CurrentDrawings()
    output.outTag = varName
    output.hdata = hdata
    output.hsign = hsign
    output.hfake = hside
    output.useLogScale = True
    return output

def drawhist1_ctag_var_orig(folderNAME:str, commonobj:CommonVars, jettagIDX:int):
    inFILE = commonobj.ifile
    jet_tag_names = ['bScore', 'CvsL', 'CvsB']

    varName = f'jettag{jettagIDX:d}'
    xAxisName = jet_tag_names[jettagIDX]
    hdata = GetHist(inFILE,f'{folderNAME}/{varName}_data_signalRegion',
                    markerCOLOR=1, markerSIZE=2, xAXISname=xAxisName)
    hsign1= GetHist(inFILE,f'{folderNAME}/{varName}_gjet_GJetsL_signalRegion_original',
                    lineCOLOR=1 , lineWIDTH=2, fillCOLOR=2 , fillSTYLE=1001, xAXISname=xAxisName)
    hsign2= GetHist(inFILE,f'{folderNAME}/{varName}_gjet_GJetsC_signalRegion_original',
                    lineCOLOR=1 , lineWIDTH=2, fillCOLOR=2 , fillSTYLE=1001, xAXISname=xAxisName)
    hsign3= GetHist(inFILE,f'{folderNAME}/{varName}_gjet_GJetsB_signalRegion_original',
                    lineCOLOR=1 , lineWIDTH=2, fillCOLOR=2 , fillSTYLE=1001, xAXISname=xAxisName)
    hfake1= GetHist(inFILE,f'{folderNAME}/{varName}_QCD_DiJetL_signalRegion_original',
                    lineCOLOR=1 , lineWIDTH=2, fillCOLOR=38, fillSTYLE=1001, xAXISname=xAxisName)
    hfake2= GetHist(inFILE,f'{folderNAME}/{varName}_QCD_DiJetC_signalRegion_original',
                    lineCOLOR=1 , lineWIDTH=2, fillCOLOR=38, fillSTYLE=1001, xAXISname=xAxisName)
    hfake3= GetHist(inFILE,f'{folderNAME}/{varName}_QCD_DiJetB_signalRegion_original',
                    lineCOLOR=1 , lineWIDTH=2, fillCOLOR=38, fillSTYLE=1001, xAXISname=xAxisName)
    hside = GetHist(inFILE,f'{folderNAME}/{varName}_data_dataSideband',
                    lineCOLOR=1 , lineWIDTH=2, fillCOLOR=38, fillSTYLE=1001, xAXISname=xAxisName)
    hsign = merge_hist(f'{varName}_gjet_signalRegion_original', [hsign1,hsign2,hsign3])
    hfake = merge_hist(f'{varName}_QCD_signalRegion_original',  [hfake1,hfake2,hfake3])

    ''' scaling section '''
    scale_hist_according_to_dijet_fit_yield(hdata,hsign,hside, commonobj.fake_yield)
    hdata.SetTitle( 'data in 19.52 fb^{-1}')
    hsign.SetTitle(f'gjet MC sample {hsign.Integral():.1f}')
    hside.SetTitle(f'di-jet contribution {hside.Integral():.1f}')

    #k_factor = scale_hist_according_to_k_factor(hdata, hsign, hside, hfake.Integral())
    #hdata.SetTitle( 'data in 19.52 fb^{-1}')
    #hsign.SetTitle(f'gjet MC sample (#times{k_factor})')
    #hfake.SetTitle(f'QCD MC samele (#times{k_factor})')
    #hside.SetTitle(f'di-jet contribution from data sideband')
    ''' scaling section end'''

    output = CurrentDrawings()
    output.outTag = varName + 'orig'
    output.hdata = hdata
    output.hsign = hsign
    output.hfake = hside
    output.useLogScale = True
    return output

def drawhist1_subvtxmass(folderNAME:str, commonobj:CommonVars):
    inFILE = commonobj.ifile

    varName = 'jettag3'
    xAxisName = 'subVtxMass'
    hdata = GetHist(inFILE,f'{folderNAME}/{varName}_data_signalRegion',
                    markerCOLOR=1, markerSIZE=2, xAXISname=xAxisName)
    hsign1= GetHist(inFILE,f'{folderNAME}/{varName}_gjet_GJetsL_signalRegion',
                    lineCOLOR=1 , lineWIDTH=2, fillCOLOR=2 , fillSTYLE=1001, xAXISname=xAxisName)
    hsign2= GetHist(inFILE,f'{folderNAME}/{varName}_gjet_GJetsC_signalRegion',
                    lineCOLOR=1 , lineWIDTH=2, fillCOLOR=2 , fillSTYLE=1001, xAXISname=xAxisName)
    hsign3= GetHist(inFILE,f'{folderNAME}/{varName}_gjet_GJetsB_signalRegion',
                    lineCOLOR=1 , lineWIDTH=2, fillCOLOR=2 , fillSTYLE=1001, xAXISname=xAxisName)
    hfake1= GetHist(inFILE,f'{folderNAME}/{varName}_QCD_DiJetL_signalRegion',
                    lineCOLOR=1 , lineWIDTH=2, fillCOLOR=38, fillSTYLE=1001, xAXISname=xAxisName)
    hfake2= GetHist(inFILE,f'{folderNAME}/{varName}_QCD_DiJetC_signalRegion',
                    lineCOLOR=1 , lineWIDTH=2, fillCOLOR=38, fillSTYLE=1001, xAXISname=xAxisName)
    hfake3= GetHist(inFILE,f'{folderNAME}/{varName}_QCD_DiJetB_signalRegion',
                    lineCOLOR=1 , lineWIDTH=2, fillCOLOR=38, fillSTYLE=1001, xAXISname=xAxisName)
    hside = GetHist(inFILE,f'{folderNAME}/{varName}_data_dataSideband',
                    lineCOLOR=1 , lineWIDTH=2, fillCOLOR=38, fillSTYLE=1001, xAXISname=xAxisName)
    hsign = merge_hist(f'{varName}_gjet_signalRegion', [hsign1,hsign2,hsign3])
    hfake = merge_hist(f'{varName}_QCD_signalRegion',  [hfake1,hfake2,hfake3])

    scale_hist_according_to_dijet_fit_yield(hdata,hsign,hside, commonobj.fake_yield)
    hdata.SetTitle( 'data in 19.52 fb^{-1}')
    hsign.SetTitle(f'gjet MC sample {hsign.Integral():.1f}')
    hside.SetTitle(f'di-jet contribution {hside.Integral():.1f}')

    output = CurrentDrawings()
    output.outTag = varName
    output.hdata = hdata
    output.hsign = hsign
    output.hfake = hside
    output.useLogScale = True
    return output

def drawhist1_bdt_score(folderNAME:str, commonobj:CommonVars):
    inFILE = commonobj.ifile
    varName='BDTscore'
    hdata = GetHist(inFILE,f'{folderNAME}/BDT_data_signalRegion',
                    markerCOLOR=1, markerSIZE=2, xAXISname=varName)
    hsign = GetHist(inFILE,f'{folderNAME}/BDT_gjet_signalRegion',
                    lineCOLOR=1 , lineWIDTH=2, fillCOLOR=2 , fillSTYLE=1001, xAXISname=varName)
    #hfake = GetHist(inFILE,f'{folderNAME}/BDT_QCD_signalRegion',
    #                lineCOLOR=1 , lineWIDTH=2, fillCOLOR=38, fillSTYLE=1001, xAXISname=varName)
    hside = GetHist(inFILE,f'{folderNAME}/BDT_data_dataSideband',
                    lineCOLOR=1 , lineWIDTH=2, fillCOLOR=38, fillSTYLE=1001, xAXISname=varName)

    scale_hist_according_to_dijet_fit_yield(hdata,hsign,hside, commonobj.fake_yield)

    hdata.SetTitle( 'data in 19.52 fb^{-1}')
    hsign.SetTitle(f'gjet MC sample')
    #hfake.SetTitle(f'QCD MC samele')
    hside.SetTitle(f'di-jet contribution from data sideband')

    output = CurrentDrawings()
    output.outTag = varName
    output.hdata = hdata
    output.hsign = hsign
    output.hfake = hside
    output.useLogScale = False
    return output

def drawhist1_ctag_postfit(folderNAME:str, commonobj:CommonVars):
    inFILE = commonobj.ifile

    varName = folderNAME
    xAxisName = 'hist.GetTitle()'
    hdata = GetHist(inFILE,f'{folderNAME}/data_obs',
                    markerCOLOR=1, markerSIZE=2, xAXISname=xAxisName)
    h_fit = GetHist(inFILE,f'{folderNAME}/TotalProcs',
                    lineCOLOR=1 , lineWIDTH=2, fillCOLOR=38, fillSTYLE=1001, xAXISname=xAxisName)

    hsign = GetHist(inFILE,f'{folderNAME}/TotalSig',
                    lineCOLOR=1 , lineWIDTH=2, fillCOLOR=2 , fillSTYLE=1001, xAXISname=xAxisName)
    hside = GetHist(inFILE,f'{folderNAME}/TotalBkg',
                    lineCOLOR=1 , lineWIDTH=2, fillCOLOR=38, fillSTYLE=1001, xAXISname=xAxisName)

    hsignL= GetHist(inFILE,f'{folderNAME}/signal_L',
                    lineCOLOR=1 , lineWIDTH=2, fillCOLOR=2 , fillSTYLE=1001, xAXISname=xAxisName)
    hsignC= GetHist(inFILE,f'{folderNAME}/signal_C',
                    lineCOLOR=1 , lineWIDTH=2, fillCOLOR=2 , fillSTYLE=1001, xAXISname=xAxisName)
    hsignB= GetHist(inFILE,f'{folderNAME}/signal_B',
                    lineCOLOR=1 , lineWIDTH=2, fillCOLOR=2 , fillSTYLE=1001, xAXISname=xAxisName)


    hdata.SetTitle( 'data in 19.52 fb^{-1}')
    hsign.SetTitle(f'signal MC fitting {hsign.Integral():.1f}')
    hside.SetTitle(f'di-jet contribution {hside.Integral():.1f}')

    output = CurrentDrawings()
    output.outTag = varName
    output.hdata = hdata
    output.hsign = hsign
    output.hfake = hside
    output.useLogScale = False
    return output
def drawhist9_postfit(folderNAME:str, commonobj:CommonVars):
    inFILE = commonobj.ifile

    varName = folderNAME
    xAxisName = 'hist.GetTitle()'
    hdata = GetHist(inFILE,f'{folderNAME}/data_obs',
                    markerCOLOR=1, markerSIZE=2, xAXISname=xAxisName)
    h_fit = GetHist(inFILE,f'{folderNAME}/TotalProcs',
                    lineCOLOR=1 , lineWIDTH=2, fillCOLOR=38, fillSTYLE=1001, xAXISname=xAxisName)

    hsign = GetHist(inFILE,f'{folderNAME}/TotalSig',
                    lineCOLOR=1 , lineWIDTH=2, fillCOLOR=2 , fillSTYLE=1001, xAXISname=xAxisName)
    hside = GetHist(inFILE,f'{folderNAME}/TotalBkg',
                    lineCOLOR=1 , lineWIDTH=2, fillCOLOR=38, fillSTYLE=1001, xAXISname=xAxisName)

    hsignL= GetHist(inFILE,f'{folderNAME}/signal_L',
                    lineCOLOR=1 , lineWIDTH=2, fillCOLOR=2 , fillSTYLE=1001, xAXISname=xAxisName)
    hsignC= GetHist(inFILE,f'{folderNAME}/signal_C',
                    lineCOLOR=1 , lineWIDTH=2, fillCOLOR=2 , fillSTYLE=1001, xAXISname=xAxisName)
    hsignB= GetHist(inFILE,f'{folderNAME}/signal_B',
                    lineCOLOR=1 , lineWIDTH=2, fillCOLOR=2 , fillSTYLE=1001, xAXISname=xAxisName)


    hdata.SetTitle( 'data in 19.52 fb^{-1}')
    hsign.SetTitle(f'signal MC fitting {hsign.Integral():.1f}')
    hside.SetTitle(f'di-jet contribution {hside.Integral():.1f}')

    output = CurrentDrawings()
    output.outTag = varName
    output.hdata = hdata
    output.hsign = hsign
    output.hfake = hside
    output.useLogScale = False
    return output

def drawhist1_bdt_score(folderNAME:str, commonobj:CommonVars):
    inFILE = commonobj.ifile
    varName='BDTscore'
    hdata = GetHist(inFILE,f'{folderNAME}/BDT_data_signalRegion',
                    markerCOLOR=1, markerSIZE=2, xAXISname=varName)
    hsign = GetHist(inFILE,f'{folderNAME}/BDT_gjet_signalRegion',
                    lineCOLOR=1 , lineWIDTH=2, fillCOLOR=2 , fillSTYLE=1001, xAXISname=varName)
    #hfake = GetHist(inFILE,f'{folderNAME}/BDT_QCD_signalRegion',
    #                lineCOLOR=1 , lineWIDTH=2, fillCOLOR=38, fillSTYLE=1001, xAXISname=varName)
    hside = GetHist(inFILE,f'{folderNAME}/BDT_data_dataSideband',
                    lineCOLOR=1 , lineWIDTH=2, fillCOLOR=38, fillSTYLE=1001, xAXISname=varName)

    scale_hist_according_to_dijet_fit_yield(hdata,hsign,hside, commonobj.fake_yield)

    hdata.SetTitle( 'data in 19.52 fb^{-1}')
    hsign.SetTitle(f'gjet MC sample')
    #hfake.SetTitle(f'QCD MC samele')
    hside.SetTitle(f'di-jet contribution from data sideband')

    output = CurrentDrawings()
    output.outTag = varName
    output.hdata = hdata
    output.hsign = hsign
    output.hfake = hside
    output.useLogScale = True
    return output

def DrawHist(folderNAME:str, commonobj:CommonVars, drawVAR:str):
    if drawVAR == 'BDTscore':
        current_drawing = drawhist1_bdt_score(folderNAME, commonobj)
    if drawVAR == 'jettag0'+'orig':
        current_drawing = drawhist1_ctag_var_orig(folderNAME, commonobj,0)
    if drawVAR == 'jettag1'+'orig':
        current_drawing = drawhist1_ctag_var_orig(folderNAME, commonobj,1)
    if drawVAR == 'jettag2'+'orig':
        current_drawing = drawhist1_ctag_var_orig(folderNAME, commonobj,2)
    if drawVAR == 'jettag0'+'calb':
        current_drawing = drawhist1_ctag_var_calb(folderNAME, commonobj,0)
    if drawVAR == 'jettag1'+'calb':
        current_drawing = drawhist1_ctag_var_calb(folderNAME, commonobj,1)
    if drawVAR == 'jettag2'+'calb':
        current_drawing = drawhist1_ctag_var_calb(folderNAME, commonobj,2)
    if drawVAR == 'jettag3':
        current_drawing = drawhist1_subvtxmass(folderNAME, commonobj)
    if drawVAR == 'postfit':
        current_drawing = drawhist1_ctag_postfit(folderNAME, commonobj)
    if drawVAR == 'postfit9':
        current_drawing = drawhist9_postfit(folderNAME, commonobj)
    current_drawing.legTitle = commonobj.get_bin_desc()

    drawhist0_stackplot_comparison(current_drawing, commonobj)

def binning_info(pETAbin, jETAbin, pPTbin):
    # input file as the format: out_kinematics_0_1__ptcut_400_600.root
    pEtaName='PETAnotfound'
    if pETAbin == 0:
        pEtaName = '|\eta^{\gamma}| < 1.4442'
    if pETAbin == 1:
        pEtaName = '1.566 < |\eta^{\gamma}| < 2.5'

    jEtaName='JETAnotfound'
    if jETAbin == 0:
        jEtaName = '|\eta^{jet}| < 1.5'
    if jETAbin == 1:
        jEtaName = '1.5 < |\eta^{jet}| < 2.4'

    from py_pt_ranges_definition import PhoPtBinning
    pt_ranges = PhoPtBinning('UL2016PreVFP')
    pPTrange = [ pt_ranges[pPTbin],pt_ranges[pPTbin+1] ] if pPTbin+1 < len(pt_ranges) else [pt_ranges[pPTbin], 'inf']
    pPtName = f'p_{{T}}^{{\gamma}} = [{pPTrange[0]},{pPTrange[1]}] GeV'

    return ','.join([pEtaName,jEtaName,pPtName])
def extract_binning_info_from_filename(inFILE):
    fileFrag = inFILE.split('.')[0].split('_')
    if len(fileFrag) == 8:
        petabin = int(fileFrag[2])
        jetabin = int(fileFrag[3])
        pptrange = [ int(fileFrag[-2]), int(fileFrag[-1]) ]
        return binning_info(petabin,jetabin,pptrange)
    return 'FAILED_EXTRACTED_BINNING_INFO'

def funcFRAG1_chi2_calc( hDATA, hSTAK):
    chi2 = 0.
    for ibin in range(1,hDATA.GetNbinsX()+1):
        bincont = hDATA.GetBinContent(ibin)
        binerro = hDATA.GetBinError(ibin)

        bintarg = sum( [h.GetBinContent(ibin) for h in hSTAK.GetHists()] )
        if bincont == 0 and binerro == 0:
            continue
        chi = (bincont - bintarg) / binerro
        chi2 += chi * chi
    ndof = hDATA.GetNbinsX() - 1;
    return chi2 / ndof


def drawhist0_stackplot_comparison(
        currentDRAWINGs:CurrentDrawings,
        commonobj:CommonVars):
    ROOT.gROOT.SetBatch(True)
    hdata = currentDRAWINGs.hdata
    hsign = currentDRAWINGs.hsign
    hfake = currentDRAWINGs.hfake
    legendTITLE = currentDRAWINGs.legTitle
    outLABEL = currentDRAWINGs.outTag
    useLOGscale = currentDRAWINGs.useLogScale

    canv = commonobj.canv
    upperpad = commonobj.upperpad
    lowerpad = commonobj.lowerpad
    upperpad.cd()


    stackplot = ROOT.THStack('hs', '')
    stackplot.Add(hsign, "HIST")
    stackplot.Add(hfake, "HIST")
    stackplot.Draw()


    def HistFraming(h, varNAME):
        ''' Setup a TH1 like object.  '''
        binwidth = h.GetXaxis().GetBinWidth(1)
        from xPhoton.analysis.PlotObjectMgr import HistFraming as framingFUNC
        framingFUNC(h, xLABEL=varNAME,yLABEL=f'Entries / {binwidth}')
    HistFraming(stackplot, hsign.GetXaxis().GetTitle())

    minFACTOR = 0.1 if useLOGscale else 1e-2
    maxFACTOR = 1e3 if useLOGscale else 1.5
    upperpad.SetLogy(useLOGscale)
    stackplot.SetMinimum( hdata.GetMinimum() * minFACTOR)
    stackplot.SetMaximum( hdata.GetMaximum() * maxFACTOR)


    stackplot.Draw()
    hdata.Draw("E0 P SAME")

    from xPhoton.analysis.PlotObjectMgr import Legend
    leg = Legend( p0_=(0.10,0.65), p1_=(0.90,0.90), title=legendTITLE, useNDC=True)
    leg.SetNColumns(2)

    leg.AddEntry('', 'fit chi2 = %.1f'%funcFRAG1_chi2_calc(hdata, stackplot), '')
    leg.AddEntry(hsign, hsign.GetTitle(), 'f')
    leg.AddEntry(hdata, hdata.GetTitle(), 'p')
    leg.AddEntry(hfake, hfake.GetTitle(), 'f')
    leg.Draw()

    lowerpad.cd()

    hratio = hdata.Clone('dataOVERmc')
    hratio.Divide(hdata,stackplot.GetStack().Last())

    hratio.SetTitle('')
    hratio.SetStats(False)
    hratio.SetMinimum(0.5)
    hratio.SetMaximum(1.6)
    hratio.GetXaxis().SetTitleSize(0.11)
    hratio.GetXaxis().SetLabelSize(0.11)
    hratio.GetYaxis().SetTitleSize(0.11)
    hratio.GetYaxis().SetLabelSize(0.11)
    hratio.GetYaxis().SetTitleOffset(0.4)
    hratio.GetYaxis().SetNdivisions(905)
    hratio.GetYaxis().CenterTitle(True)
    hratio.SetLineColor(1)
    hratio.SetXTitle( stackplot.GetXaxis().GetTitle() )
    hratio.SetYTitle('Data/MC')
    hratio.Draw("P")



    refline = ROOT.TLine(
            hratio.GetXaxis().GetXmin(), 1.,
            hratio.GetXaxis().GetXmax(), 1.)
    refline.SetLineColor(1)
    refline.SetLineStyle(2) # dashed line
    refline.Draw("SAME")
    hratio.Draw("P SAME")

    commonobj.keep_drawing_obj(outLABEL, (hdata, stackplot, leg, hratio,refline))

if __name__ == "__main__":
    import sys
    pETAdesc,jETAdesc,pPTdesc, inputfile = sys.argv[1:]
    #inputfile = 'testregion/postfit.root'
    LOG(f'input file {inputfile}\n\n')


    import xPhoton.analysis.MyCanvas
    xPhoton.analysis.MyCanvas.isTransparent = True

    inFile = ROOT.TFile.Open(inputfile)
    numCTag = 3
    commonobj = CommonVars(inFile, numCTag)

    commonobj.SetBinDesc(pETAdesc,jETAdesc,pPTdesc)
    for idx in range(numCTag):
        commonobj.SetCurrentPad(idx)
        DrawHist(f'cat_{idx}_postfit',commonobj, 'postfit9')
    commonobj.canv.SaveAs(f"varcheck_allvars_ctag_Reweig.pdf")
