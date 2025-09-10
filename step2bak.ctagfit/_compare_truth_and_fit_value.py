#!/usr/bin/env python3
import ROOT
from uncertainties import ufloat
from extract_fit_value import GetSnapshotAtMultiDimFit, make_hist, info, Info
import yaml
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
        o['numC'] = Info(value=loadedVALUE.cval.nominal_value, error=loadedVALUE.cval.std_dev)
        o['numB'] = Info(value=loadedVALUE.bval.nominal_value, error=loadedVALUE.bval.std_dev)
        if hasattr(loadedVALUE, 'fake'):
            o['numFAKE'] = Info(value=loadedVALUE.fake.nominal_value, error=loadedVALUE.fake.std_dev)
        return o
    except Exception as e:
        raise Exception('[Error] loadedvalue_adapter() got erroes') from e
def loadedvalue_adapter_CandBonly(loadedVALUE:LoadedValue) -> dict:
    try:
        o = {}
        o['numC'] = Info(value=loadedVALUE.cval.nominal_value, error=loadedVALUE.cval.std_dev)
        o['numB'] = Info(value=loadedVALUE.bval.nominal_value, error=loadedVALUE.bval.std_dev)
        return o
    except Exception as e:
        raise Exception('[Error] loadedvalue_adapter() got erroes') from e
        
    

def get_integral_from_hist(h) -> ufloat:
    val = h.Integral()
    unc = sum( h.GetBinError(idx+1) ** 2 for idx in range(h.GetNbinsX()) ) ** 0.5
    return ufloat(val,unc)
    

def load_truth(iFILEname, Ljet, Cjet, Bjet, fake=None) -> LoadedValue:
    ### disable uncertainties in truth histogram
    tfile = ROOT.TFile.Open(iFILEname)

    hL = tfile.Get(Ljet)
    hC = tfile.Get(Cjet)
    hB = tfile.Get(Bjet)
    
    integralFAKE = None
    
    valF = None
    if fake and fake in tfile.GetListOfKeys():
        hFAKE = tfile.Get(fake)
        integralFAKE = get_integral_from_hist(hFAKE)
        valF = ufloat(integralFAKE.nominal_value,1e-3)

    valL = ufloat(get_integral_from_hist(hL).nominal_value,1e-3)
    valC = ufloat(get_integral_from_hist(hC).nominal_value,1e-3)
    valB = ufloat(get_integral_from_hist(hB).nominal_value,1e-3)

    return LoadedValue( valL, valC, valB, valF )

def get_fitinfo_from_postfit_yamls(inYAMLs):
    loaded_vars = {}
    for inYAML in inYAMLs:
        with open(inYAML, 'r') as fIN:
            in_vars = yaml.safe_load(fIN)

            for var_name, var_content in in_vars.items():
                loaded_vars[var_name] = ufloat(var_content['value'], var_content['error'])

    if 'numL' not in loaded_vars: raise IOError(f'[VarNotFound] input yaml files {inYAMLs} does not contain variable "numL"')
    if 'numC' not in loaded_vars: raise IOError(f'[VarNotFound] input yaml files {inYAMLs} does not contain variable "numC"')
    if 'numB' not in loaded_vars: raise IOError(f'[VarNotFound] input yaml files {inYAMLs} does not contain variable "numB"')
    return LoadedValue(loaded_vars['numL'],loaded_vars['numC'],loaded_vars['numB'],loaded_vars.get('numFAKE',None))



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
        if isinstance(v,ROOT.RooRealVar):
            output[loadedVAR] = Info(
                    value = v.getVal(),
                    error = v.getError(),
                    errUp = v.getErrorHi(),
                    errDn = v.getErrorLo(),
                    )
    inFILE.Close()
    #return output
    log.debug(f'''[GetInfoFromWS] file {inputFILEname} got
            numL {ufloat( output['numL'].value, output['numL'].error ) if 'numL' in output else ufloat(1e-3,1e-3)}
            numC {ufloat( output['numC'].value, output['numC'].error )}
            numB {ufloat( output['numB'].value, output['numB'].error )}
            numF {ufloat( output['numFAKE'].value, output['numFAKE'].error ) if 'numFAKE' in output else None}
            ''')

    return LoadedValue(
            ufloat( output['numL'].value, output['numL'].error ) if 'numL' in output else ufloat(1e-3,1e-3),
            ufloat( output['numC'].value, output['numC'].error ),
            ufloat( output['numB'].value, output['numB'].error ),
            ufloat( output['numFAKE'].value, output['numFAKE'].error ) if 'numFAKE' in output else None
            )




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

def disable_truth_uncertainties(truthINFOdict:dict) -> dict:
    return { varNAME:Info(recINFO.value, 0) for varNAME,recINFO in truthINFOdict.items() } # only record the value and ignore all errors

def mainfunc_extractfitandmakecomparison(fitVALUE, truthVALUE):
    info_truth = loadedvalue_adapter(truthVALUE)
    #info_truth = disable_truth_uncertainties(info_truth_)
    info_fit   = loadedvalue_adapter(fitVALUE)
    write_SigOnly = True
    if write_SigOnly:
        siginfo_truth = loadedvalue_adapter_CandBonly(truthVALUE)
        #siginfo_truth = disable_truth_uncertainties(siginfo_truth_)
        siginfo_fit   = loadedvalue_adapter_CandBonly(fitVALUE)

    if len(info_truth.keys()) != len(info_fit.keys()):
        raise KeyError(f'[InvalidInformation] infomation read from truth "{info_truth}" and fit "{info_fit}" does not has the same length')
    log.debug(f'[FitInfo] Get info_fit = {info_fit}')

    outROOTfilename = 'compare_truth_and_fit_value.root'
    file_out = ROOT.TFile(outROOTfilename, 'recreate')
    file_out.cd()
    hTruth = make_hist('truthinfo',info_truth)
    hFit = make_hist('fitinfo', info_fit)
    if write_SigOnly:
        hSigTruth = make_hist('truthinfo_sigONLY',siginfo_truth)
        hSigFit = make_hist('fitinfo_sigONLY', siginfo_fit)

    ratio = ROOT.TGraphAsymmErrors()
    ratio.SetName('ratioinfo')
    ratio.Divide(hFit,hTruth,'pois')
    if write_SigOnly:
        sigratio = ROOT.TGraphAsymmErrors()
        sigratio.SetName('ratioinfo_sigONLY')
        sigratio.Divide(hSigFit,hSigTruth,'pois')

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
    if write_SigOnly:
        hSigTruth.Write()
        hSigFit.Write()
        sigratio.Write()


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



    if '.yaml' in sys.argv[2]:
        profiledNLL_yamls = sys.argv[2:]
        fit_value = get_fitinfo_from_postfit_yamls(profiledNLL_yamls)
    if '.root' in sys.argv[2]:
        combineRESULT = sys.argv[2]
        fitVARs = sys.argv[3:]
        fit_value = getinfo_from_workspace(combineRESULT, fitVARs)





    mainfunc_extractfitandmakecomparison(fit_value, truth_value)


    print(f'[LoadFile] Truth value loaded from {truth_file}')
    show_value(truth_value, 'truth')
    show_frac (truth_value, 'truth')
    print(f'[LoadFile] Fit value loaded from {config["fit_info"]["file"]}')
    show_value(fit_value  , 'fit  ')
    show_frac (fit_value  , 'fit  ')
