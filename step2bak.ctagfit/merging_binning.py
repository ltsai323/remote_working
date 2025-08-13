#!/usr/bin/env python3
import logging
import ROOT
import uncertainties

log = logging.getLogger(__name__)

class Binning:
    def __init__(self, inSTR):
        log.debug(f'[Input] Binning() Get input "{ inSTR }"')
        if '__' not in inSTR:
            raise IOError(f'[InvalidInput] getfilename() reqiuires input filename like "makehisto_binned_ctagfit_data__0_0_1000_1500.root". Input "{ inSTR }" is invalid')
        ii = inSTR.find('__') + 2
        jj = inSTR[ii:].find('.root') # if .root not found, got -1
        binned_str = inSTR[ii:ii+jj] if jj != -1 else inSTR[ii:]

        binnings = binned_str.split('_')
        log.debug(f'[Analyze] Binning() get result "{ binned_str }". It should be like "0_0_210_230" format')
        self.binned_str = binned_str
        if len(binnings) == 3:
            log.debug(f'[GotBinning] Binning() got a jEtaBin - jPtL - jPtR')
            self.jEtaBin = int(binnings[0])
            self.jPtL = int(binnings[1])
            self.jPtR = int(binnings[2])
        if len(binnings) == 4:
            log.debug(f'[GotBinning] Binning() got a pEtaBin - jEtaBin - pPtL - pPtR')
            self.pEtaBin = int(binnings[0])
            self.jEtaBin = int(binnings[1])
            self.pPtL = int(binnings[2])
            self.pPtR = int(binnings[3])
        if not hasattr(self, 'jEtaBin'):
            raise IOError(f'[InvalidInputStr] Binning() cannot analyze the input "{ inSTR }". The available value like "makehisto_binned_ctagfit_data__0_0_1000_1500.root"')
    def __str__(self):
        return self.binned_str
    def __repr__(self):
        return self.__str__()

def getfilename(binning:Binning, filename='datafit_fitinfo.yaml') -> str:
    return f'binned_{binning}/{filename}'


def testfunc_inarg():
    inARGs = [
	    'makehisto_binned_ctagfit_data__0_0_1000_1500.root',
	    'makehisto_binned_ctagfit_data__0_0_210_230.root',
	    'makehisto_binned_ctagfit_data__0_0_230_250.root',
	    'makehisto_binned_ctagfit_data__0_0_250_300.root',
	    'makehisto_binned_ctagfit_data__0_0_300_400.root',
    ]
    from pprint import pprint
    inBINNINGs = [ Binning(inFILE) for inFILE in inARGs ]
    pprint( inBINNINGs )

    pprint( [getfilename(b) for b in inBINNINGs] )


import yaml
class YamlRecords:
    def __init__(self, yamlDICT, loadVARs:list):
        ### if input yamlDICT is empty, return an empty YamlRecords
        if len(yamlDICT) == 0:
            self.isempty = True
            return
        self.isempty = False
        for loadVAR in loadVARs:
            try:
                value = uncertainties.ufloat( yamlDICT[loadVAR]['value'], yamlDICT[loadVAR]['error'] )
            except KeyError as e:
                raise KeyError(f'[InvalidKey] YamlRecords() cannot get yamlDICT[{ loadVAR }][value] from yamlDICT "{ yamlDICT }"') from e
            setattr(self, loadVAR, value)
            log.debug(f'[LoadVar] YamlRecords() load variable "{ loadVAR }" with value "{ value }"')
    def __str__(self):
        return f'YamlRecords({ {varname:varinst for varname,varinst in vars(self).items() } })' if self.isempty else 'YamlRecords(Empty)'
    def __repr__(self):
        return self.__str__()

YAMLREC_EMPTY_VAL = -999
YAMLREC_EMPTY_ERR = 999
EMPTY_UFLOAT = uncertainties.ufloat(YAMLREC_EMPTY_VAL,YAMLREC_EMPTY_ERR)
def get_var_from(yamlREC:YamlRecords, varNAME) -> uncertainties.ufloat:
    if yamlREC.isempty: return EMPTY_UFLOAT
    if not hasattr(yamlREC, varNAME):
        raise KeyError(f'[InvalidVar] variable "{ varNAME }" not found in "{ yamlREC }"')
    return getattr(yamlREC,varNAME)
def is_empty_ufloat(uFLOAT:uncertainties.ufloat) -> bool:
    if uFLOAT == EMPTY_UFLOAT: return True
    if uFLOAT.nominal_value == YAMLREC_EMPTY_VAL and uFLOAT.std_dev == YAMLREC_EMPTY_ERR: return True
    return False

import os
def load_yaml_file(yamlFILE:str)->dict:
    try:
        with open(yamlFILE, 'r') as fIN:
            return yaml.safe_load(fIN)
    except FileNotFoundError as e:
        log.warning(f'[SkipFile] load_yaml_file() cannot get "{ yamlFILE }" in system, skip')
        return {} # return empty dictionary once system cannot get file. Skip this file without break the code
        #raise FileNotFoundError(f'[FileNotFound] load_yaml_file() get file "{ yamlFILE }" not in system')

def testfunc_LoadYaml_psuedofit():
    inARGs = [
	    'makehisto_binned_ctagfit_data__0_0_1000_1500.root',
	    'makehisto_binned_ctagfit_data__0_0_210_230.root',
	    'makehisto_binned_ctagfit_data__0_0_230_250.root',
	    'makehisto_binned_ctagfit_data__0_0_250_300.root',
	    'makehisto_binned_ctagfit_data__0_0_300_400.root',
    ]
    from pprint import pprint
    inBINNINGs = [ Binning(inFILE) for inFILE in inARGs ]
    loadYamlFiles = [ getfilename(b, 'compare_truth_and_fit_value.yaml') for b in inBINNINGs ]
    ''' content of compare_truth_and_fit_value.yaml
fitinfo:
  numB:
    composition: 0
    errDn: 0
    errUp: 0
    error: 63.31231367732636
    value: 411.57623291015625
  numC:
    composition: 0
    errDn: 0
    errUp: 0
    error: 112.9720744928909
    value: 6530.7373046875
  numL:
    composition: 0
    errDn: 0
    errUp: 0
    error: 78.99158910268636
    value: 1946.64990234375
ratio:
  numB:
    composition: 0
    errDn: 0
    errUp: 0
    error: 0.15968653270987615
    value: 0.8673324786398994
  numC:
    composition: 0
    errDn: 0
    errUp: 0
    error: 0.01835460918570912
    value: 1.0091277549950879
  numL:
    composition: 0
    errDn: 0
    errUp: 0
    error: 0.04517274066801496
    value: 1.0049129141338708
truthinfo:
  numB:
    composition: 0
    errDn: 0
    errUp: 0
    error: 32.78014239180523
    value: 474.5310974121094
  numC:
    composition: 0
    errDn: 0
    errUp: 0
    error: 32.78014239180523
    value: 6471.66552734375
  numL:
    composition: 0
    errDn: 0
    errUp: 0
    error: 32.78014239180523
    value: 1937.1329345703125
    '''
    yamlContents = [ load_yaml_file(f) for f in loadYamlFiles ]
    load_fitinfo   = [ YamlRecords(conf.get('fitinfo',{})  , ['numL','numC','numB']) for conf in yamlContents ]
    load_truthinfo = [ YamlRecords(conf.get('truthinfo',{}), ['numL','numC','numB']) for conf in yamlContents ]
    load_ratio     = [ YamlRecords(conf.get('ratio',{})    , ['numL','numC','numB']) for conf in yamlContents ]


    log.info(f'load fitinfo')
    pprint(load_fitinfo)
    log.info(f'load truthinfo')
    pprint(load_truthinfo)
    log.info(f'load ratio')
    pprint(load_ratio)
                        
def testfunc_LoadYaml_data():
    inARGs = [
	    'makehisto_binned_ctagfit_data__0_0_1000_1500.root',
	    'makehisto_binned_ctagfit_data__0_0_210_230.root',
	    'makehisto_binned_ctagfit_data__0_0_230_250.root',
	    'makehisto_binned_ctagfit_data__0_0_250_300.root',
	    'makehisto_binned_ctagfit_data__0_0_300_400.root',
    ]
    from pprint import pprint
    inBINNINGs = [ Binning(inFILE) for inFILE in inARGs ]
    loadYamlFiles = [ getfilename(b, 'datafit_fitinfo.yaml') for b in inBINNINGs ]
    ''' content of datafit_fitinfo.yaml
numB:
  composition: 0
  errDn: -22.545060934408212
  errUp: 22.545060934408212
  error: 22.545060934408212
  value: 475.7562028358829
numC:
  composition: 0
  errDn: -119.40214418305209
  errUp: 119.40214418305209
  error: 119.40214418305209
  value: 4107.197048056608
numL:
  composition: 0
  errDn: -134.04069580223222
  errUp: 134.04069580223222
  error: 134.04069580223222
  value: 21189.57507158708
    '''
    yamlContents = [ load_yaml_file(f) for f in loadYamlFiles ]
    load_fitinfo   = [ YamlRecords(conf, ['numL','numC','numB']) for conf in yamlContents ]


    log.info(f'load fitinfo')
    pprint(load_fitinfo)

from array import array
def makehist(histNAME:str, binINFO:dict, accessENTRYfunc = None):
    log.debug(f'[GotBinInfo] makehist() got binINFO "{ binINFO }"')
    ptL = set([int(thebin.pPtL) for thebin,rec in binINFO.items() ])
    ptR = set([int(thebin.pPtR) for thebin,rec in binINFO.items() ])
    log.debug(f'[HistPtArrayL] makehist() got ptL "{ptL}"')
    log.debug(f'[HistPtArrayR] makehist() got ptR "{ptR}"')
    pt_array = array('f', sorted(ptL|ptR))
    log.debug(f'[HistPtArray] makehist() got pt array = "{pt_array}"')

    if len(pt_array) == 0:
        log.warning(f'[EmptyArray] makehist() tried to make "{ histNAME }" but array contains nothing. Skip')
        return None

    hist = ROOT.TH1F(histNAME, '', len(pt_array)-1, pt_array)
    for thebin,rec in binINFO.items():
        binIdx = hist.FindBin(thebin.pPtL+1e-6)
        #variable = get_var_from(rec, varNAME)
        variable = accessENTRYfunc(rec) if accessENTRYfunc is not None else rec

        if isinstance(rec, YamlRecords):
            if rec.isempty: continue
        if variable is None: continue
        if is_empty_ufloat(variable): continue
        hist.SetBinContent(binIdx, variable.nominal_value)
        hist.SetBinError  (binIdx, variable.std_dev)
    return hist
def makehist_dividePtEtaBinWidth(histNAME:str, binINFO:dict, etaBINwidth:float, accessENTRYfunc = None):
    log.debug(f'[GotBinInfo] makehist() got binINFO "{ binINFO }"')
    ptL = set([int(thebin.pPtL) for thebin,rec in binINFO.items() ])
    ptR = set([int(thebin.pPtR) for thebin,rec in binINFO.items() ])
    log.debug(f'[HistPtArrayL] makehist() got ptL "{ptL}"')
    log.debug(f'[HistPtArrayR] makehist() got ptR "{ptR}"')
    pt_array = array('f', sorted(ptL|ptR))
    log.debug(f'[HistPtArray] makehist() got pt array = "{pt_array}"')

    if len(pt_array) == 0:
        log.warning(f'[EmptyArray] makehist() tried to make "{ histNAME }" but array contains nothing. Skip')
        return None

    hist = ROOT.TH1F(histNAME, '', len(pt_array)-1, pt_array)
    for thebin,rec in binINFO.items():
        binIdx = hist.FindBin(thebin.pPtL+1e-6)
        #variable = get_var_from(rec, varNAME)
        variable = accessENTRYfunc(rec) if accessENTRYfunc is not None else rec

        if isinstance(rec, YamlRecords):
            if rec.isempty: continue
        if variable is None: continue
        if is_empty_ufloat(variable): continue
        pt_binwidth = hist.GetBinWidth(1)
        ptandeta_binwidth = pt_binwidth * etaBINwidth
        variable = variable / ptandeta_binwidth
        hist.SetBinContent(binIdx, variable.nominal_value)
        hist.SetBinError  (binIdx, variable.std_dev)
    return hist
def dividehist(newHISTname, hU, hD) -> ROOT.TH1F:
    h = hU.Clone(newHISTname)
    h.Divide(hD)
    return h


def testfunc_LoadYaml_data_makehist():
    inARGs = [
	    'makehisto_binned_ctagfit_data__0_0_1000_1500.root',
	    'makehisto_binned_ctagfit_data__0_0_210_230.root',
	    'makehisto_binned_ctagfit_data__0_0_230_250.root',
	    'makehisto_binned_ctagfit_data__0_0_250_300.root',
	    'makehisto_binned_ctagfit_data__0_0_300_400.root',
    ]
    from pprint import pprint
    inBINNINGs = [ Binning(inFILE) for inFILE in inARGs ]
    loadYamlFiles = [ getfilename(b, 'datafit_fitinfo.yaml') for b in inBINNINGs ]
    ''' content of datafit_fitinfo.yaml
numB:
  composition: 0
  errDn: -22.545060934408212
  errUp: 22.545060934408212
  error: 22.545060934408212
  value: 475.7562028358829
numC:
  composition: 0
  errDn: -119.40214418305209
  errUp: 119.40214418305209
  error: 119.40214418305209
  value: 4107.197048056608
numL:
  composition: 0
  errDn: -134.04069580223222
  errUp: 134.04069580223222
  error: 134.04069580223222
  value: 21189.57507158708
    '''
    yamlContents = [ load_yaml_file(f) for f in loadYamlFiles ]
    load_fitinfo   = [ YamlRecords(conf, ['numL','numC','numB']) for conf in yamlContents ]

    bin00 = [ (idx,inbin) for idx,inbin in enumerate(inBINNINGs) if inbin.pEtaBin==0 and inbin.jEtaBin==0 ]
    bin01 = [ (idx,inbin) for idx,inbin in enumerate(inBINNINGs) if inbin.pEtaBin==0 and inbin.jEtaBin==1 ]
    bin10 = [ (idx,inbin) for idx,inbin in enumerate(inBINNINGs) if inbin.pEtaBin==1 and inbin.jEtaBin==0 ]
    bin11 = [ (idx,inbin) for idx,inbin in enumerate(inBINNINGs) if inbin.pEtaBin==1 and inbin.jEtaBin==1 ]

    h00 = makehist( 'bin00', { inbin:load_fitinfo[idx] for idx,inbin in bin00 }, 'numL' )
    h01 = makehist( 'bin01', { inbin:load_fitinfo[idx] for idx,inbin in bin01 }, 'numL' )
    h10 = makehist( 'bin10', { inbin:load_fitinfo[idx] for idx,inbin in bin10 }, 'numL' )
    h11 = makehist( 'bin11', { inbin:load_fitinfo[idx] for idx,inbin in bin11 }, 'numL' )

    canv = ROOT.TCanvas("c1",'',600,400)
    h00.Draw()
    canv.SaveAs("hi.png")


def merge_hist(newHISTname, hists):
    if len(hists) == 0:
        raise IOError(f'[UnableToMergeHist] merge_hist() cannot merge hist because nothing put into hists')
    h = hists[0].Clone(newHISTname)
    for hh in hists[1:]:
        h.Add(hh)
    return h

class histCollection:
    def __init__(self):
        pass
    @classmethod
    def merge_overflow_underflow_bin(cls,h):
        binU = 0 # underflow bin
        bin1 = 1
        binE = h.GetNbinsX()
        binO = h.GetNbinsX() + 1 # overflow bin
        histCollection.merge_bin(h, bin1, binU)
        histCollection.merge_bin(h, binE, binO)

    @classmethod
    def merge_bin(cls, h, binON, binOFF):
        valOFF = h.GetBinContent(binOFF)
        errOFF = h.GetBinError  (binOFF)
        valON  = h.GetBinContent(binON)
        errON  = h.GetBinError  (binON)
        h.SetBinContent(binOFF, 0)
        h.SetBinError  (binOFF, 0)
        h.SetBinContent(binON, valON+valOFF)
        h.SetBinError  (binON, (errON**2+errOFF**2)**0.5)



    def WriteAllHists(self, fOUT,writeOVERFLOWbin=False):
        fOUT.cd()
        for hname, inst in vars(self).items():
            if   isinstance(inst, ROOT.TH1):
                log.debug(f'[WriteHist] write hist "{ inst.GetName() }" from histCollection.{hname}')
                if writeOVERFLOWbin: histCollection.merge_overflow_underflow_bin(inst)
                inst.Write()
            elif isinstance(inst, list) or isinstance(inst, tuple):
                for h in inst:
                    if isinstance(h, ROOT.TH1):
                        log.debug(f'[WriteHist] write hist "{ h.GetName() }" from histCollection.{hname} list/tuple')
                        if writeOVERFLOWbin: histCollection.merge_overflow_underflow_bin(h)
                        h.Write()
            elif isinstance(inst, list) or isinstance(inst, dict):
                for varname,h in inst.items():
                    if isinstance(h, ROOT.TH1):
                        if writeOVERFLOWbin: histCollection.merge_overflow_underflow_bin(h)
                        log.debug(f'[WriteHist] write hist "{ h.GetName() }" from histCollection.{hname} dictionary key {varname}')
                        h.Write()
            else:
                log.warn(f'[UnableToWrite] histCollection.WriteAllHists() cannot write histogram from "{ hname }"')

def make_ratio(uVAR:uncertainties.ufloat,dVAR:uncertainties.ufloat) -> uncertainties.ufloat:
    ''' take ratio  uVAR / dVAR '''
    if not isinstance(uVAR, uncertainties.core.Variable):
        raise IOError(f'[InvalidInputVar] make_ratio() requires an complex number with type uncertainties.ufloat. First input var "{ type(uVAR) }" is invalid')
    if not (isinstance(dVAR, uncertainties.core.Variable) or isinstance(dVAR,float)):
        raise IOError(f'[InvalidInputVar] make_ratio() requires an complex number with type uncertainties.ufloat or float. Second input var "{ type(dVAR) }" is invalid')
    if is_empty_ufloat(uVAR) or is_empty_ufloat(dVAR): return EMPTY_UFLOAT
    return uVAR / dVAR

class mainfunc_datafit_LCB:
    name = 'datafit_LCB'
    load_file = 'datafit_fitinfo.yaml'
    load_vars = ['numL','numC','numB']

    load_file_BDT = 'datafit_fitinfo.BDT.yaml'
    load_vars_BDT = ['numSIGN','numFAKE']
    ofile = 'merging_binning_result.datafit_LCB.root'
    def __init__(self, inARGs:list):
        self.args = inARGs
        ''' # content of datafit_fitinfo.yaml
numB:
    composition: 0
    errDn: -22.545060934408212
    errUp: 22.545060934408212
    error: 22.545060934408212
    value: 475.7562028358829
numC:
    composition: 0
    errDn: -119.40214418305209
    errUp: 119.40214418305209
    error: 119.40214418305209
    value: 4107.197048056608
numL:
    composition: 0
    errDn: -134.04069580223222
    errUp: 134.04069580223222
    error: 134.04069580223222
    value: 21189.57507158708
        '''

    def exec(self):
        inBINNINGs = [ Binning(inFILE) for inFILE in self.args ]
        loadYamlFiles = [ getfilename(b, self.load_file) for b in inBINNINGs ]
        yamlContents = [ load_yaml_file(f) for f in loadYamlFiles ]
        load_fitinfo   = [ YamlRecords(conf, self.load_vars) for conf in yamlContents ]

        yamlFileNameBDT = [ getfilename(b, self.load_file_BDT) for b in inBINNINGs ]
        yamlContentsBDT = [ load_yaml_file(f) for f in yamlFileNameBDT ]
        load_fitinfoBDT = [ YamlRecords(conf, self.load_vars_BDT) for conf in yamlContentsBDT ]

        bin00 = [ (idx,inbin) for idx,inbin in enumerate(inBINNINGs) if inbin.pEtaBin==0 and inbin.jEtaBin==0 ]
        bin01 = [ (idx,inbin) for idx,inbin in enumerate(inBINNINGs) if inbin.pEtaBin==0 and inbin.jEtaBin==1 ]
        bin10 = [ (idx,inbin) for idx,inbin in enumerate(inBINNINGs) if inbin.pEtaBin==1 and inbin.jEtaBin==0 ]
        bin11 = [ (idx,inbin) for idx,inbin in enumerate(inBINNINGs) if inbin.pEtaBin==1 and inbin.jEtaBin==1 ]

        ### load_fitinfo[idx] is a YamlRecords. So it needs a functioin to access ufloat
        varL = lambda dictENTRY: get_var_from(dictENTRY,'numL') ## method to access dictionary entry of load_fitinfo[idx]
        varC = lambda dictENTRY: get_var_from(dictENTRY,'numC')
        varB = lambda dictENTRY: get_var_from(dictENTRY,'numB')
        ofile = ROOT.TFile( self.ofile, 'recreate')
        hists = histCollection()
        hists.bin00_numL = makehist( 'bin00_numL', { inbin:load_fitinfo[idx] for idx,inbin in bin00 }, varL )
        hists.bin01_numL = makehist( 'bin01_numL', { inbin:load_fitinfo[idx] for idx,inbin in bin01 }, varL )
        hists.bin10_numL = makehist( 'bin10_numL', { inbin:load_fitinfo[idx] for idx,inbin in bin10 }, varL )
        hists.bin11_numL = makehist( 'bin11_numL', { inbin:load_fitinfo[idx] for idx,inbin in bin11 }, varL )

        hists.bin00_numC = makehist( 'bin00_numC', { inbin:load_fitinfo[idx] for idx,inbin in bin00 }, varC )
        hists.bin01_numC = makehist( 'bin01_numC', { inbin:load_fitinfo[idx] for idx,inbin in bin01 }, varC )
        hists.bin10_numC = makehist( 'bin10_numC', { inbin:load_fitinfo[idx] for idx,inbin in bin10 }, varC )
        hists.bin11_numC = makehist( 'bin11_numC', { inbin:load_fitinfo[idx] for idx,inbin in bin11 }, varC )

        hists.bin00_numB = makehist( 'bin00_numB', { inbin:load_fitinfo[idx] for idx,inbin in bin00 }, varB )
        hists.bin01_numB = makehist( 'bin01_numB', { inbin:load_fitinfo[idx] for idx,inbin in bin01 }, varB )
        hists.bin10_numB = makehist( 'bin10_numB', { inbin:load_fitinfo[idx] for idx,inbin in bin10 }, varB )
        hists.bin11_numB = makehist( 'bin11_numB', { inbin:load_fitinfo[idx] for idx,inbin in bin11 }, varB )

        compositionL = lambda fitINFO, fitINFObdt: make_ratio( get_var_from(fitINFO,'numL'), get_var_from(fitINFObdt, 'numSIGN') )
        compositionC = lambda fitINFO, fitINFObdt: make_ratio( get_var_from(fitINFO,'numC'), get_var_from(fitINFObdt, 'numSIGN') )
        compositionB = lambda fitINFO, fitINFObdt: make_ratio( get_var_from(fitINFO,'numB'), get_var_from(fitINFObdt, 'numSIGN') )
        hists.bin00_compositionL = makehist( 'bin00_compositionL', { inbin:compositionL(load_fitinfo[idx],load_fitinfoBDT[idx]) for idx,inbin in bin00 } )
        hists.bin01_compositionL = makehist( 'bin01_compositionL', { inbin:compositionL(load_fitinfo[idx],load_fitinfoBDT[idx]) for idx,inbin in bin01 } )
        hists.bin10_compositionL = makehist( 'bin10_compositionL', { inbin:compositionL(load_fitinfo[idx],load_fitinfoBDT[idx]) for idx,inbin in bin10 } )
        hists.bin11_compositionL = makehist( 'bin11_compositionL', { inbin:compositionL(load_fitinfo[idx],load_fitinfoBDT[idx]) for idx,inbin in bin11 } )

        hists.bin00_compositionC = makehist( 'bin00_compositionC', { inbin:compositionC(load_fitinfo[idx],load_fitinfoBDT[idx]) for idx,inbin in bin00 } )
        hists.bin01_compositionC = makehist( 'bin01_compositionC', { inbin:compositionC(load_fitinfo[idx],load_fitinfoBDT[idx]) for idx,inbin in bin01 } )
        hists.bin10_compositionC = makehist( 'bin10_compositionC', { inbin:compositionC(load_fitinfo[idx],load_fitinfoBDT[idx]) for idx,inbin in bin10 } )
        hists.bin11_compositionC = makehist( 'bin11_compositionC', { inbin:compositionC(load_fitinfo[idx],load_fitinfoBDT[idx]) for idx,inbin in bin11 } )

        hists.bin00_compositionB = makehist( 'bin00_compositionB', { inbin:compositionB(load_fitinfo[idx],load_fitinfoBDT[idx]) for idx,inbin in bin00 } )
        hists.bin01_compositionB = makehist( 'bin01_compositionB', { inbin:compositionB(load_fitinfo[idx],load_fitinfoBDT[idx]) for idx,inbin in bin01 } )
        hists.bin10_compositionB = makehist( 'bin10_compositionB', { inbin:compositionB(load_fitinfo[idx],load_fitinfoBDT[idx]) for idx,inbin in bin10 } )
        hists.bin11_compositionB = makehist( 'bin11_compositionB', { inbin:compositionB(load_fitinfo[idx],load_fitinfoBDT[idx]) for idx,inbin in bin11 } )

        hists.bin0C_endcap_barrel = dividehist( 'bin0C_endcap_barrel', hists.bin01_numC, hists.bin00_numC )
        hists.bin1C_endcap_barrel = dividehist( 'bin1C_endcap_barrel', hists.bin11_numC, hists.bin10_numC )

        hists.bin0compC_endcap_barrel = dividehist( 'bin0compC_endcap_barrel', hists.bin01_compositionC, hists.bin00_compositionC )
        hists.bin1compC_endcap_barrel = dividehist( 'bin1compC_endcap_barrel', hists.bin11_compositionC, hists.bin10_compositionC )



        hists.WriteAllHists(ofile)
        ofile.Close()
        log.info(f'[OutputHistograms] Root file "{ self.ofile }" generated')
class mainfunc_comparetruth_LCB:
    name = 'comparetruth_LCB'
    load_file = 'compare_truth_and_fit_value.yaml'
    load_vars = ['numL','numC','numB']
    ofile = 'merging_binning_result.comparetruth_LCB.root'
    def __init__(self, inARGs:list):
        self.args = inARGs
        ''' content of compare_truth_and_fit_value.yaml
fitinfo:
  numB:
    composition: 0
    errDn: 0
    errUp: 0
    error: 63.31231367732636
    value: 411.57623291015625
  numC:
    composition: 0
    errDn: 0
    errUp: 0
    error: 112.9720744928909
    value: 6530.7373046875
  numL:
    composition: 0
    errDn: 0
    errUp: 0
    error: 78.99158910268636
    value: 1946.64990234375
ratio:
  numB:
    composition: 0
    errDn: 0
    errUp: 0
    error: 0.15968653270987615
    value: 0.8673324786398994
  numC:
    composition: 0
    errDn: 0
    errUp: 0
    error: 0.01835460918570912
    value: 1.0091277549950879
  numL:
    composition: 0
    errDn: 0
    errUp: 0
    error: 0.04517274066801496
    value: 1.0049129141338708
truthinfo:
  numB:
    composition: 0
    errDn: 0
    errUp: 0
    error: 32.78014239180523
    value: 474.5310974121094
  numC:
    composition: 0
    errDn: 0
    errUp: 0
    error: 32.78014239180523
    value: 6471.66552734375
  numL:
    composition: 0
    errDn: 0
    errUp: 0
    error: 32.78014239180523
    value: 1937.1329345703125
    '''

    def exec(self):
        inBINNINGs = [ Binning(inFILE) for inFILE in self.args ]
        loadYamlFiles = [ getfilename(b, self.load_file) for b in inBINNINGs ]
        yamlContents = [ load_yaml_file(f) for f in loadYamlFiles ]
        load_fitinfo   = [ YamlRecords(conf.get('fitinfo'  ,{}), self.load_vars) for conf in yamlContents ]
        load_truthinfo = [ YamlRecords(conf.get('truthinfo',{}), self.load_vars) for conf in yamlContents ]
        load_ratio     = [ YamlRecords(conf.get('ratio'    ,{}), self.load_vars) for conf in yamlContents ]


        bin00 = [ (idx,inbin) for idx,inbin in enumerate(inBINNINGs) if inbin.pEtaBin==0 and inbin.jEtaBin==0 ]
        bin01 = [ (idx,inbin) for idx,inbin in enumerate(inBINNINGs) if inbin.pEtaBin==0 and inbin.jEtaBin==1 ]
        bin10 = [ (idx,inbin) for idx,inbin in enumerate(inBINNINGs) if inbin.pEtaBin==1 and inbin.jEtaBin==0 ]
        bin11 = [ (idx,inbin) for idx,inbin in enumerate(inBINNINGs) if inbin.pEtaBin==1 and inbin.jEtaBin==1 ]

        ofile = ROOT.TFile( self.ofile, 'recreate')
        hists = histCollection()
        ### load_fitinfo[idx] is a YamlRecords. So it needs a functioin to access ufloat
        varL = lambda dictENTRY: get_var_from(dictENTRY,'numL') ## method to access dictionary entry of load_fitinfo[idx]
        varC = lambda dictENTRY: get_var_from(dictENTRY,'numC')
        varB = lambda dictENTRY: get_var_from(dictENTRY,'numB')
        hists.fitinfo_bin00_numL = makehist( 'fitinfo_bin00_numL', { inbin:load_fitinfo[idx] for idx,inbin in bin00 }, varL )
        hists.fitinfo_bin01_numL = makehist( 'fitinfo_bin01_numL', { inbin:load_fitinfo[idx] for idx,inbin in bin01 }, varL )
        hists.fitinfo_bin10_numL = makehist( 'fitinfo_bin10_numL', { inbin:load_fitinfo[idx] for idx,inbin in bin10 }, varL )
        hists.fitinfo_bin11_numL = makehist( 'fitinfo_bin11_numL', { inbin:load_fitinfo[idx] for idx,inbin in bin11 }, varL )

        hists.fitinfo_bin00_numC = makehist( 'fitinfo_bin00_numC', { inbin:load_fitinfo[idx] for idx,inbin in bin00 }, varC )
        hists.fitinfo_bin01_numC = makehist( 'fitinfo_bin01_numC', { inbin:load_fitinfo[idx] for idx,inbin in bin01 }, varC )
        hists.fitinfo_bin10_numC = makehist( 'fitinfo_bin10_numC', { inbin:load_fitinfo[idx] for idx,inbin in bin10 }, varC )
        hists.fitinfo_bin11_numC = makehist( 'fitinfo_bin11_numC', { inbin:load_fitinfo[idx] for idx,inbin in bin11 }, varC )

        hists.fitinfo_bin00_numB = makehist( 'fitinfo_bin00_numB', { inbin:load_fitinfo[idx] for idx,inbin in bin00 }, varB )
        hists.fitinfo_bin01_numB = makehist( 'fitinfo_bin01_numB', { inbin:load_fitinfo[idx] for idx,inbin in bin01 }, varB )
        hists.fitinfo_bin10_numB = makehist( 'fitinfo_bin10_numB', { inbin:load_fitinfo[idx] for idx,inbin in bin10 }, varB )
        hists.fitinfo_bin11_numB = makehist( 'fitinfo_bin11_numB', { inbin:load_fitinfo[idx] for idx,inbin in bin11 }, varB )



        hists.truthinfo_bin00_numL = makehist( 'truthinfo_bin00_numL', { inbin:load_truthinfo[idx] for idx,inbin in bin00 }, varL )
        hists.truthinfo_bin01_numL = makehist( 'truthinfo_bin01_numL', { inbin:load_truthinfo[idx] for idx,inbin in bin01 }, varL )
        hists.truthinfo_bin10_numL = makehist( 'truthinfo_bin10_numL', { inbin:load_truthinfo[idx] for idx,inbin in bin10 }, varL )
        hists.truthinfo_bin11_numL = makehist( 'truthinfo_bin11_numL', { inbin:load_truthinfo[idx] for idx,inbin in bin11 }, varL )

        hists.truthinfo_bin00_numC = makehist( 'truthinfo_bin00_numC', { inbin:load_truthinfo[idx] for idx,inbin in bin00 }, varC )
        hists.truthinfo_bin01_numC = makehist( 'truthinfo_bin01_numC', { inbin:load_truthinfo[idx] for idx,inbin in bin01 }, varC )
        hists.truthinfo_bin10_numC = makehist( 'truthinfo_bin10_numC', { inbin:load_truthinfo[idx] for idx,inbin in bin10 }, varC )
        hists.truthinfo_bin11_numC = makehist( 'truthinfo_bin11_numC', { inbin:load_truthinfo[idx] for idx,inbin in bin11 }, varC )

        hists.truthinfo_bin00_numB = makehist( 'truthinfo_bin00_numB', { inbin:load_truthinfo[idx] for idx,inbin in bin00 }, varB )
        hists.truthinfo_bin01_numB = makehist( 'truthinfo_bin01_numB', { inbin:load_truthinfo[idx] for idx,inbin in bin01 }, varB )
        hists.truthinfo_bin10_numB = makehist( 'truthinfo_bin10_numB', { inbin:load_truthinfo[idx] for idx,inbin in bin10 }, varB )
        hists.truthinfo_bin11_numB = makehist( 'truthinfo_bin11_numB', { inbin:load_truthinfo[idx] for idx,inbin in bin11 }, varB )


        hists.ratio_bin00_numL = makehist( 'ratio_bin00_numL', { inbin:load_ratio[idx] for idx,inbin in bin00 }, varL )
        hists.ratio_bin01_numL = makehist( 'ratio_bin01_numL', { inbin:load_ratio[idx] for idx,inbin in bin01 }, varL )
        hists.ratio_bin10_numL = makehist( 'ratio_bin10_numL', { inbin:load_ratio[idx] for idx,inbin in bin10 }, varL )
        hists.ratio_bin11_numL = makehist( 'ratio_bin11_numL', { inbin:load_ratio[idx] for idx,inbin in bin11 }, varL )

        hists.ratio_bin00_numC = makehist( 'ratio_bin00_numC', { inbin:load_ratio[idx] for idx,inbin in bin00 }, varC )
        hists.ratio_bin01_numC = makehist( 'ratio_bin01_numC', { inbin:load_ratio[idx] for idx,inbin in bin01 }, varC )
        hists.ratio_bin10_numC = makehist( 'ratio_bin10_numC', { inbin:load_ratio[idx] for idx,inbin in bin10 }, varC )
        hists.ratio_bin11_numC = makehist( 'ratio_bin11_numC', { inbin:load_ratio[idx] for idx,inbin in bin11 }, varC )

        hists.ratio_bin00_numB = makehist( 'ratio_bin00_numB', { inbin:load_ratio[idx] for idx,inbin in bin00 }, varB )
        hists.ratio_bin01_numB = makehist( 'ratio_bin01_numB', { inbin:load_ratio[idx] for idx,inbin in bin01 }, varB )
        hists.ratio_bin10_numB = makehist( 'ratio_bin10_numB', { inbin:load_ratio[idx] for idx,inbin in bin10 }, varB )
        hists.ratio_bin11_numB = makehist( 'ratio_bin11_numB', { inbin:load_ratio[idx] for idx,inbin in bin11 }, varB )


        
        def significance_calc(fitINFO,truthINFO, varNAME) -> float:
            ff = get_var_from(fitINFO,varNAME)
            tt = get_var_from(truthINFO,varNAME)

            if is_empty_ufloat(ff): return -1
            if is_empty_ufloat(tt): return -1
            return abs(ff.nominal_value-tt.nominal_value) / ff.std_dev
            
        calc_significanceL = [ significance_calc(fitinfo,truthinfo,'numL') for fitinfo,truthinfo in zip(load_fitinfo,load_truthinfo) ]
        calc_significanceC = [ significance_calc(fitinfo,truthinfo,'numC') for fitinfo,truthinfo in zip(load_fitinfo,load_truthinfo) ]
        calc_significanceB = [ significance_calc(fitinfo,truthinfo,'numB') for fitinfo,truthinfo in zip(load_fitinfo,load_truthinfo) ]

        def makehist_significance(histNAME, vals):
            h = ROOT.TH1F(histNAME, 'fit significance', 28, -0.6, 5.)
            for v in vals:
                h.Fill(v)
            return h
        hists.significanceL_bin00 = makehist_significance(f'significanceL_bin00', (calc_significanceL[idx] for idx,inbin in bin00) )
        hists.significanceL_bin01 = makehist_significance(f'significanceL_bin01', (calc_significanceL[idx] for idx,inbin in bin01) )
        hists.significanceL_bin10 = makehist_significance(f'significanceL_bin10', (calc_significanceL[idx] for idx,inbin in bin10) )
        hists.significanceL_bin11 = makehist_significance(f'significanceL_bin11', (calc_significanceL[idx] for idx,inbin in bin11) )
        hists.significanceL       = merge_hist('significanceL', [hists.significanceL_bin00,hists.significanceL_bin01,hists.significanceL_bin10,hists.significanceL_bin11] )

        hists.significanceC_bin00 = makehist_significance(f'significanceC_bin00', (calc_significanceC[idx] for idx,inbin in bin00) )
        hists.significanceC_bin01 = makehist_significance(f'significanceC_bin01', (calc_significanceC[idx] for idx,inbin in bin01) )
        hists.significanceC_bin10 = makehist_significance(f'significanceC_bin10', (calc_significanceC[idx] for idx,inbin in bin10) )
        hists.significanceC_bin11 = makehist_significance(f'significanceC_bin11', (calc_significanceC[idx] for idx,inbin in bin11) )
        hists.significanceC       = merge_hist('significanceC', [hists.significanceC_bin00,hists.significanceC_bin01,hists.significanceC_bin10,hists.significanceC_bin11] )

        hists.significanceB_bin00 = makehist_significance(f'significanceB_bin00', (calc_significanceB[idx] for idx,inbin in bin00) )
        hists.significanceB_bin01 = makehist_significance(f'significanceB_bin01', (calc_significanceB[idx] for idx,inbin in bin01) )
        hists.significanceB_bin10 = makehist_significance(f'significanceB_bin10', (calc_significanceB[idx] for idx,inbin in bin10) )
        hists.significanceB_bin11 = makehist_significance(f'significanceB_bin11', (calc_significanceB[idx] for idx,inbin in bin11) )
        hists.significanceB       = merge_hist('significanceB', [hists.significanceB_bin00,hists.significanceB_bin01,hists.significanceB_bin10,hists.significanceB_bin11] )

        rnd = ROOT.TRandom3(2398)
        def makehist_stackratio_generate_1000evt(histNAME, ratios):
            h = ROOT.TH1F(histNAME, 'Use Randome number representing uncertainties', 35, 0.8, 1.5)
            horig = ROOT.TH1F(histNAME+'orig', 'Direct fill fit/truth', 35, 0.8, 1.5)

            N_PSUEDODATA_GENERATED = 1000
            evt_weight = 1. / N_PSUEDODATA_GENERATED
            for ratio in ratios:
                if is_empty_ufloat(ratio): continue
                horig.Fill(ratio.nominal_value)
                for iGen in range(N_PSUEDODATA_GENERATED):
                    h.Fill( rnd.Gaus(ratio.nominal_value,ratio.std_dev), evt_weight )
            return (h,horig)
        hists.stackratioL_bin00 = makehist_stackratio_generate_1000evt( 'stackratioL_bin00', ( get_var_from(load_ratio[idx],'numL') for idx,inbin in bin00 )  )
        hists.stackratioL_bin01 = makehist_stackratio_generate_1000evt( 'stackratioL_bin01', ( get_var_from(load_ratio[idx],'numL') for idx,inbin in bin01 )  )
        hists.stackratioL_bin10 = makehist_stackratio_generate_1000evt( 'stackratioL_bin10', ( get_var_from(load_ratio[idx],'numL') for idx,inbin in bin10 )  )
        hists.stackratioL_bin11 = makehist_stackratio_generate_1000evt( 'stackratioL_bin11', ( get_var_from(load_ratio[idx],'numL') for idx,inbin in bin11 )  )
        hists.stackratioL       = merge_hist('stackratioL'    , [hists.stackratioL_bin00[0],hists.stackratioL_bin01[0],hists.stackratioL_bin10[0],hists.stackratioL_bin11[0]] )
        hists.stackratioLorig   = merge_hist('stackratioLorig', [hists.stackratioL_bin00[1],hists.stackratioL_bin01[1],hists.stackratioL_bin10[1],hists.stackratioL_bin11[1]] )

        hists.stackratioC_bin00 = makehist_stackratio_generate_1000evt( 'stackratioC_bin00', ( get_var_from(load_ratio[idx],'numC') for idx,inbin in bin00 )  )
        hists.stackratioC_bin01 = makehist_stackratio_generate_1000evt( 'stackratioC_bin01', ( get_var_from(load_ratio[idx],'numC') for idx,inbin in bin01 )  )
        hists.stackratioC_bin10 = makehist_stackratio_generate_1000evt( 'stackratioC_bin10', ( get_var_from(load_ratio[idx],'numC') for idx,inbin in bin10 )  )
        hists.stackratioC_bin11 = makehist_stackratio_generate_1000evt( 'stackratioC_bin11', ( get_var_from(load_ratio[idx],'numC') for idx,inbin in bin11 )  )
        hists.stackratioC       = merge_hist('stackratioC'    , [hists.stackratioC_bin00[0],hists.stackratioC_bin01[0],hists.stackratioC_bin10[0],hists.stackratioC_bin11[0]] )
        hists.stackratioCorig   = merge_hist('stackratioCorig', [hists.stackratioC_bin00[1],hists.stackratioC_bin01[1],hists.stackratioC_bin10[1],hists.stackratioC_bin11[1]] )

        hists.stackratioB_bin00 = makehist_stackratio_generate_1000evt( 'stackratioB_bin00', ( get_var_from(load_ratio[idx],'numB') for idx,inbin in bin00 )  )
        hists.stackratioB_bin01 = makehist_stackratio_generate_1000evt( 'stackratioB_bin01', ( get_var_from(load_ratio[idx],'numB') for idx,inbin in bin01 )  )
        hists.stackratioB_bin10 = makehist_stackratio_generate_1000evt( 'stackratioB_bin10', ( get_var_from(load_ratio[idx],'numB') for idx,inbin in bin10 )  )
        hists.stackratioB_bin11 = makehist_stackratio_generate_1000evt( 'stackratioB_bin11', ( get_var_from(load_ratio[idx],'numB') for idx,inbin in bin11 )  )
        hists.stackratioB       = merge_hist('stackratioB'    , [hists.stackratioB_bin00[0],hists.stackratioB_bin01[0],hists.stackratioB_bin10[0],hists.stackratioB_bin11[0]] )
        hists.stackratioBorig   = merge_hist('stackratioBorig', [hists.stackratioB_bin00[1],hists.stackratioB_bin01[1],hists.stackratioB_bin10[1],hists.stackratioB_bin11[1]] )






        hists.WriteAllHists(ofile,writeOVERFLOWbin=True)
        ofile.Close()
        log.info(f'[OutputHistograms] Root file "{ self.ofile }" generated')



    



if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format='[basicCONFIG] %(levelname)s - %(message)s',
                        datefmt='%H:%M:%S')

    #testfunc_inarg()
    #testfunc_LoadYaml_data()
    #testfunc_LoadYaml_data_makehist()

    import sys
    runmode = sys.argv[1]
    allbinningstrs = sys.argv[2:]

    mainfunc = None
    if runmode == mainfunc_datafit_LCB.name:
        mainfunc = mainfunc_datafit_LCB(allbinningstrs)
    if runmode == mainfunc_comparetruth_LCB.name:
        mainfunc = mainfunc_comparetruth_LCB(allbinningstrs)

    if mainfunc is None: raise IOError(f'[InvalidRunMode] runmode "{ runmode }" is invalid in merging_binning.py')
    mainfunc.exec()

