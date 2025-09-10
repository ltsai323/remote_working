#!/usr/bin/env python3
import ROOT
from uncertainties import ufloat
from extract_fit_value import GetSnapshotAtMultiDimFit, make_hist, info, Info
import yaml
#!/usr/bin/env python3
import logging

log = logging.getLogger(__name__)



class LoadedValue:
    def __init__(self, lVAL, cVAL, bVAL, fakeVAL = None):
        self.lval = lVAL
        self.cval = cVAL
        self.bval = bVAL
        if fakeVAL is not None:
            self.fake = fakeVAL
        tot = lVAL + cVAL + bVAL
        self.lfrac = lVAL / tot
        self.cfrac = cVAL / tot
        self.bfrac = bVAL / tot

def loadedvalue_adapter(loadedVALUE:LoadedValue) -> dict:
    try:
        o = {}
        o['numL'] = Info(value=loadedVALUE.lval.nominal_value, error=loadedVALUE.lval.std_dev)
        o['numC'] = Info(value=loadedVALUE.cval.nominal_value, error=loadedVALUE.lval.std_dev)
        o['numB'] = Info(value=loadedVALUE.bval.nominal_value, error=loadedVALUE.lval.std_dev)
        if hasattr(loadedVALUE, 'fake'):
            o['numFAKE'] = Info(value=loadedVALUE.fake.nominal_value, error=loadedVALUE.fake.std_dev)
        return o
    except Exception as e:
        raise Exception('[Error] loadedvalue_adapter() got erroes') from e
        
    

def get_integral_from_hist(h) -> ufloat:
    val = h.Integral()
    unc = sum( h.GetBinError(idx+1) ** 2 for idx in range(h.GetNbinsX()) ) ** 0.5
    return ufloat(val,unc)
    

def load_truth(iFILEname, Ljet, Cjet, Bjet, fake=None) -> LoadedValue:
    tfile = ROOT.TFile.Open(iFILEname)

    hL = tfile.Get(Ljet)
    hC = tfile.Get(Cjet)
    hB = tfile.Get(Bjet)
    
    integralFAKE = None
    
    if fake and fake in tfile.GetListOfKeys():
        hFAKE = tfile.Get(fake)
        integralFAKE = get_integral_from_hist(hFAKE)

    return LoadedValue(
            get_integral_from_hist(hL),
            get_integral_from_hist(hC),
            get_integral_from_hist(hB),
            integralFAKE)

def load_fit_from_postfit(iFILEname) -> LoadedValue:
    print(iFILEname)

    tfile = ROOT.TFile.Open(iFILEname)

    hL = tfile.Get('Ljet')
    hC = tfile.Get('Cjet')
    hB = tfile.Get('Bjet')
    integralFake = None
    if 'fake' in tfile.GetListOfKeys():
        hFAKE = tfile.Get('fake')
        integralFake = get_integral_from_hist(hFAKE)

    return LoadedValue(
            get_integral_from_hist(hL),
            get_integral_from_hist(hC),
            get_integral_from_hist(hB),
            integralFake
            )



def show_value(info, tag):
    print(f'LoadValue({tag}, l({info.lval:10.2f}),  c({info.cval:10.2f}),  b({info.bval:10.2f}) )')
def show_frac(info, tag):
    print(f'LoadFrac ({tag}, l({info.lfrac:.4f}),  c({info.cfrac:.4f}),  b({info.bfrac:.4f}) )')

def getinfo_from_workspace(inputFILEname:str, loadedVARs:list) -> dict:
    inFILE = ROOT.TFile.Open(inputFILEname)
    ws = inFILE.Get('w')
    snapshot = GetSnapshotAtMultiDimFit(ws)

    output = {}
    for loadedVAR in loadedVARs:
        v = snapshot.find(loadedVAR)
        output[loadedVAR] = Info(
                value = v.getVal(),
                error = v.getError(),
                errUp = v.getErrorHi(),
                errDn = v.getErrorLo(),
                )
    log.debug(f'[LoadedVars] file {inputFILEname} got {output}')
    return output




def testfunc_getinfo():
    getinfo_from_workspace('psuedofit_higgsCombineTest.MultiDimFit.mH120.root', ['numL','numC','numB'] )
    exit()


def get_hist_label(hist):
    return [ hist.GetXaxis().GetBinLabel(binidx+1) for binidx in range(hist.GetNbinsX()) ]
def hist_to_yaml_rec(hist):
    if isinstance(hist, ROOT.TH1):
        outDICT = {}
        for binIdx in range(1, hist.GetNbinsX() + 1 ):
            bin_label = hist.GetXaxis().GetBinLabel(binIdx)
            bin_content = hist.GetBinContent(binIdx)
            bin_error   = hist.GetBinError  (binIdx)
            outDICT[bin_label] = Info(
                    value = bin_content,
                    error = bin_error,
                    errUp = 0,
                    errDn = 0
                    ).to_dict()
        return outDICT
    raise ValueError(f'[InvalidInput] hist_to_yaml_rec() only accepts histogram, input parameter "{ type(hist) }" is invalid.')
def tgrapherror_to_yaml_rec(hist, labels):
    if isinstance(hist, ROOT.TGraphAsymmErrors):
        outDICT = {}
        for binIdx in range(hist.GetN()):
            bin_label = labels[binIdx]
            bin_content = hist.GetPointY(binIdx)
            bin_error   = hist.GetErrorY(binIdx)
            outDICT[bin_label] = Info(
                    value = bin_content,
                    error = bin_error,
                    errUp = 0,
                    errDn = 0
                    ).to_dict()
        return outDICT

    raise ValueError(f'[InvalidInput] tgrapherror_to_yaml_rec() only accepts tgraph, input parameter "{ type(hist) }" is invalid.')

def mainfunc_extractfitandmakecomparison(higgsbineFITTEDresult, fitVARs, truthVALUE):
    info_truth = loadedvalue_adapter(truthVALUE)
    info_fit   = getinfo_from_workspace(higgscombineFITTEDresult, fitVARs)

    if len(info_truth.keys()) != len(info_fit.keys()):
        raise KeyError(f'[InvalidInformation] infomation read from truth "{info_truth}" and fit "{info_fit}" does not has the same length')

    outROOTfilename = 'compare_truth_and_fit_value.root'
    file_out = ROOT.TFile(outROOTfilename, 'recreate')
    file_out.cd()
    hTruth = make_hist('truthinfo',info_truth)
    hFit = make_hist('fitinfo', info_fit)

    ratio = ROOT.TGraphAsymmErrors()
    ratio.SetName('ratioinfo')
    ratio.Divide(hFit,hTruth,'pois')

    outYAMLfilename = outROOTfilename.replace('.root','.yaml')
    with open(outYAMLfilename, 'w') as yamlOUT:
        oDICT = {}
        oDICT['truthinfo'] = hist_to_yaml_rec(hTruth)
        oDICT['fitinfo'] = hist_to_yaml_rec(hFit)
        bin_labels = get_hist_label(hTruth)
        oDICT['ratio'] = tgrapherror_to_yaml_rec(ratio, bin_labels)
        yaml.dump(oDICT, yamlOUT, default_flow_style=False)
        info(f'[GenerateYAML] file "{ outYAMLfilename }" generated')



    hTruth.Write()
    hFit.Write()
    ratio.Write()


    file_out.Close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG,
                        format='[basicCONFIG] %(levelname)s - %(message)s',
                        datefmt='%H:%M:%S')
    import sys
    import yaml

    with open(sys.argv[1], 'r') as iFILE:
        print(f'[LoadYamlFile] {sys.argv[1]}')
        config = yaml.safe_load(iFILE)

    truth_file = config['inputFILE']

    truth_value = load_truth(
            config['inputFILE'],
            **config['truth_info'])

    fit_value = load_fit_from_postfit(
            config['fit_info']['file'])


    higgscombineFITTEDresult = sys.argv[2]
    fitVARs = sys.argv[3:]
    #info_fit   = getinfo_from_workspace('psuedofit_higgsCombineTest.MultiDimFit.mH120.root', ['numL','numC','numB'] )
    mainfunc_extractfitandmakecomparison(higgscombineFITTEDresult, fitVARs, truth_value)


    print(f'[LoadFile] Truth value loaded from {truth_file}')
    show_value(truth_value, 'truth')
    show_frac (truth_value, 'truth')
    print(f'[LoadFile] Fit value loaded from {config["fit_info"]["file"]}')
    show_value(fit_value  , 'fit  ')
    show_frac (fit_value  , 'fit  ')
