#!/usr/bin/env python3
import ROOT
from uncertainties import ufloat
import csv

FILE_IDENTIFIER = 'calculate_xs'
DEBUG_MODE = False
def BUG(mesg):
    if DEBUG_MODE:
        print(f'b-{FILE_IDENTIFIER}@ {mesg}')
def info(mesg):
    print(f'i-{FILE_IDENTIFIER}@ {mesg}')




class Binning:
    def __init__(self, pETAbin, jETAbin, pPTbin):
        self.pEtaBin = int(pETAbin)
        self.jEtaBin = int(jETAbin)
        self.pPtBin = int(pPTbin)
def pho_eta_width(etaBIN:int):
    if etaBIN == 0: return 2. * 1.4442
    if etaBIN == 1: return 2. * (2.5 - 1.566)
    raise IOError(f'[InvalidBin] photon eta bin "{ etaBIN }" is not defined')
def jet_eta_width(etaBIN:int):
    if etaBIN == 0: return 2. * 1.5
    if etaBIN == 1: return 2. * (2.5 - 1.5)
    raise IOError(f'[InvalidBin] jet eta bin "{ etaBIN }" is not defined')

HELP_MESSAGE = '''
arguments:
    1. pEtaBin : int
    2. jEtaBin : int
    3. pPtBin  : int
    4. N0 : float. Fit value without WP cut
    5. Nc : float. Fit value with WPc Medium cut
    6. Nb : float. Fit value with WPb Loose cut
'''
#  
#  class IOArgs:
#      def __init__(self, argv):
#          try:
#              self.pETAbin = int(argv[1])
#              self.jETAbin = int(argv[2])
#              self.pPTbin  = int(argv[3])
#  
#              self.N0 = float(argv[4])
#              self.Nc = float(argv[5])
#              self.Nb = float(argv[6])
#          except Exception as e:
#              raise IOError(HELP_MESSAGE) from e
def CalculateNcNbFromGJetFit(effFILE:ROOT.TFile, binning:Binning,
                  fitN_nocut, fitN_WPc, fitN_WPb): # value might be float or ufloat
    N0 = fitN_nocut
    Nc = fitN_WPc
    Nb = fitN_WPb


    def _get_eff_(ge, pPTbin):
        value = ge.GetPointY(pPTbin)
        error = ge.GetErrorY(pPTbin)
        return ufloat(value, error)
    def get_eff_WPc(qTYPE):
        graphname_WPc = lambda qTYPE_,pETAbin_,jETAbin_: f'bin{pETAbin_:1d}{jETAbin_:1d}{qTYPE_}_WPcM_eff'
        graph_WPc = effFILE.Get( graphname_WPc(qTYPE, binning.pEtaBin, binning.jEtaBin) )
        return _get_eff_(graph_WPc, binning.pPtBin)
    def get_eff_WPb(qTYPE):
        graphname_WPb = lambda qTYPE_,pETAbin_,jETAbin_: f'bin{pETAbin_:1d}{jETAbin_:1d}{qTYPE_}_WPbL_eff'
        graph_WPb = effFILE.Get( graphname_WPb(qTYPE, binning.pEtaBin, binning.jEtaBin) )
        return _get_eff_(graph_WPb, binning.pPtBin)


    ### get efficiencies from tgraph error
    effL_WPc = get_eff_WPc('L')
    effL_WPb = get_eff_WPb('L')

    effC_WPc = get_eff_WPc('C')
    effC_WPb = get_eff_WPb('C')

    effB_WPc = get_eff_WPc('B')
    effB_WPb = get_eff_WPb('B')
    
    




    ### derived variables
    AcB = effB_WPc - effL_WPc
    AcC = effC_WPc - effL_WPc

    AbB = effB_WPb - effL_WPb
    AbC = effC_WPb - effL_WPb

    ### apply formula
    _Nc_Nb = -1. * (AcB*Nb - AbB*Nc - (AcB*effL_WPb - AbB*effL_WPc)*N0) / (AcC*Nb - AbC*Nc - (AcC*effL_WPb - AbC*effL_WPc)*N0)
    _Nc = (AcB*Nb - AbB*Nc - (AcB*effL_WPb - AbB*effL_WPc)*N0) / (AcB*AbC - AbB*AcC)
    _Nb = (AcC*Nb - AbC*Nc - (AcC*effL_WPb - AbC*effL_WPc)*N0) / (AbB*AcC - AcB*AbC)

    BUG(f'[CalculatedValues] Nc({_Nc}), Nb({_Nb}), Nc/Nb({_Nc_Nb})')

    return _Nc, _Nb, _Nc_Nb
#return { 'Nc': _Nc, 'Nb': _Nb, 'Nc_Nb': _Nc_Nb }



class CSVEntry:
    def __init__(self, csvDICT):
        try:
            self.binning = Binning( csvDICT['pEtaBin'],csvDICT['jEtaBin'],csvDICT['pPtBin'])

            self.fitN_WP0 = ufloat( float(csvDICT['N_WP0']),float(csvDICT['N_WP0error']) )
            self.fitN_WPc = ufloat( float(csvDICT['N_WPc']),float(csvDICT['N_WPcerror']) )
            self.fitN_WPb = ufloat( float(csvDICT['N_WPb']),float(csvDICT['N_WPberror']) )
        except Exception as e:
            raise IOError(HELP_MESSAGE) from e

def yield_to_xs_scale_factor(binning:Binning, ge) -> float:
    w_peta = pho_eta_width(binning.pEtaBin)
    w_jeta = jet_eta_width(binning.jEtaBin)
    w_ppt = ge.GetErrorX(binning.pPtBin) * 2
    return  1. / w_peta / w_jeta / w_ppt
def GetPtBinL(binning:Binning, ge) -> float:
    return ge.GetPointX(binning.pPtBin) - ge.GetErrorX(binning.pPtBin)
def GetPtBinR(binning:Binning, ge) -> float:
    return ge.GetPointX(binning.pPtBin) + ge.GetErrorX(binning.pPtBin)

def output_csv_file(csv_contents:list, outCSVfile:str):
    filename = outCSVfile

    with open(filename, 'w', newline='') as f_out:
        for csv_content in csv_contents:
            writer = csv.DictWriter(f_out, fieldnames=csv_content.keys())

            ### If the file is empty or newly created, write the header first
            if f_out.tell() == 0: writer.writeheader()

            writer.writerow(csv_content)
    info(f'[Export] put info into csv file "{ filename }"')

if __name__ == "__main__":
    import sys
    from collections import namedtuple
    InArgs = namedtuple('InArgs', 'dataERA effFILE inCSV')
    args = InArgs(*sys.argv[1:])

    efftfile = ROOT.TFile.Open(args.effFILE)
    grapherr = efftfile.Get('bin00L_WPcL_eff')

    inCSV = args.inCSV
    dataERA = args.dataERA

    outCSV = 'calculated_xs.csv'
    out_csv_content = []

    '''
    import EraVariables
    luminosity = EraVariables.luminosity(dataERA)
    sflumi = 1./luminosity
    '''

    with open(inCSV, 'r') as fIN:
        for csv_entry in csv.DictReader(fIN):
            entry = CSVEntry(csv_entry)

            Nc, Nb, Nc_Nb = CalculateNcNbFromGJetFit(efftfile, entry.binning,
                entry.fitN_WP0,
                entry.fitN_WPc,
                entry.fitN_WPb,
            )

            sf0 = yield_to_xs_scale_factor(entry.binning,grapherr)


            # sf = sf0 * sflumi

            sf = sf0

            out_csv_content.append( {
                'pEtaBin': entry.binning.pEtaBin,
                'jEtaBin': entry.binning.jEtaBin,
                'pPtBin' : entry.binning.pPtBin,
                'pPtL' : GetPtBinL(entry.binning, grapherr),
                'pPtR' : GetPtBinR(entry.binning, grapherr),
                'xs_c': Nc.nominal_value * sf,
                'xs_c_error': Nc.std_dev * sf,
                'xs_b': Nb.nominal_value * sf,
                'xs_b_error': Nb.std_dev * sf,
                'frac_c_b': Nc_Nb.nominal_value,
                'yield_c': Nc.nominal_value,
                'error_c': Nc.std_dev,
                'yield_b': Nb.nominal_value,
                'error_b': Nb.std_dev,
            } )


    if DEBUG_MODE:
        from pprint import pprint
        pprint(out_csv_content)
    output_csv_file(out_csv_content, outCSV)

