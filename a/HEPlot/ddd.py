import uproot
import numpy as np
import mplhep as hep
import matplotlib.pyplot as plt
import math
import mplhep as hep
from uncertainties import ufloat, unumpy
from pprint import pprint




def getOrder(maxNUMBER:float) -> float:
    index_to_10 = int(math.log10(maxNUMBER))
    return 10**index_to_10


# Create a ratio plot function
class HistSet:
    def __init__(self, hist, **xargs):
        self.hist = hist
        for name, val in xargs.items():
            setattr(self, name, val)
def getBinCenter(h:HistSet) -> list:
    return h.hist.axes.centers[0]
def getBinWidth(h:HistSet) -> list:
    return h.hist.axes.widths[0]
def getBinData(h:HistSet) -> list:
    ''' return a list of ufloat(). Get bin content with bin error '''
    #return unumpy.uarray( h.hist.values(), h.hist.errors() )
    return unumpy.uarray( h.orig_obj.values(), h.orig_obj.errors() )
def getBinContent(h:HistSet) -> list:
    return unumpy.nominal_values(getBinData(h))
def getBinError(h:HistSet) -> list:
    return unumpy.std_devs(getBinData(h))

def Scale(h:HistSet, scaleFACTOR:float):
    #pprint(h.orig_obj._values)
    h.orig_obj._values *= scaleFACTOR
    h.orig_obj._variances *= scaleFACTOR*scaleFACTOR
    h.hist = h.orig_obj.to_hist() # update hist.Hist object
    #pprint(h.hist.values)
    h.desc += f' (SF={scaleFACTOR:.1f})'
def ScaleWithoutAdditionalInfo(h:HistSet, scaleFACTOR:float):
    h.orig_obj._values *= scaleFACTOR
    h.orig_obj._variances *= scaleFACTOR*scaleFACTOR
    h.hist = h.orig_obj.to_hist() # update hist.Hist object

def getHistMinForVisualization(h:HistSet, outTYPE:str) -> float:
    if outTYPE == 'linear':
        return 0
    if outTYPE == 'log':
        try:
            return min( [ v for v in getBinContent(h) if v != 0. ] ) * 0.1
        except ValueError as e:
            print(f'\n\n[Unable to find minimun] use 1e-6 as lower bond')
            print(f'errors:\n    {e}')
            return 1e-6
    if outTYPE == 'original':
        return min(getBinContent(h))
    raise IOError(f'[InvalidArgument] getHistMinForVisualization() got outTYPE == "{ outTYPE }".')

def getHistMaxForVisualization(h:HistSet, outTYPE:str) -> float:
    if outTYPE == 'linear':
        return max(getBinContent(h)) * 2.0
    if outTYPE == 'log':
        return max(getBinContent(h)) * 1000.
    if outTYPE == 'original':
        return max(getBinContent(h))
    raise IOError(f'[InvalidArgument] getHistMaxForVisualization() got outTYPE == "{ outTYPE }".')

    




def getScaleFactor_QCD_LOtoNLO(hDATA:HistSet, hSIGN:HistSet, hQCD:HistSet):
    ''' SF = (N_data-N_sig) / N_QCD. And this SF is only applied on QCD, which compensates LO / NLO calculations. '''
    data_value = getBinData(hDATA)
    sign_value = getBinData(hSIGN)
    fake_value = getBinData(hQCD)

    qcd_scale_factor = ( np.sum( unumpy.nominal_values(data_value) ) - np.sum( unumpy.nominal_values(sign_value) ) )\
                       / np.sum( unumpy.nominal_values(fake_value) )
    return float(f'{qcd_scale_factor:.1f}')

    

PLOTSTYLE_DATA = { 'linestyle': 'None', 'color': 'black', 'marker': 'o' }
PLOTSTYLE_HIST = { 'histtype': 'fill', 'edgecolor': '1', 'linewidth': 0.5 }

INFO_CMS_PRELIMIILARY_UL2016PREVFP  = {'label':'Prelimilary', 'data':True, 'lumi':19.52, 'year':'UL2016preVFP' , 'loc':2}
INFO_CMS_PRELIMIILARY_UL2016POSTVFP = {'label':'Prelimilary', 'data':True, 'lumi':16.81, 'year':'UL2016postVFP', 'loc':2}
INFO_CMS_PRELIMIILARY_RUN2022EE = {'label':'Prelimilary', 'data':True, 'lumi':26.81, 'year':'2022EE', 'loc':2}
def ratio_plot(hDATA:HistSet, hist1:list, xLABEL, ylabel, ySCALE, figNAME:str=''):
    hep.style.use(hep.style.ROOT) # For now ROOT defaults to CMS
    hep.style.use("CMS") # string aliases work too
    fig, (ax, ax_ratio) = plt.subplots(2, 1, gridspec_kw={'height_ratios': [3, 1]}, sharex=True)

    data_value = getBinData(hDATA)
    sign_value = getBinData(hist1[0])
    fake_value = getBinData(hist1[1])

    #qcd_scale_factor = ( np.sum( unumpy.nominal_values(data_value) ) - np.sum( unumpy.nominal_values(sign_value) ) )\
    #                   / np.sum( unumpy.nominal_values(fake_value) )

    #qcd_sf = float(f'{qcd_scale_factor:.2f}')
    #fake_value *= qcd_sf
    #Scale(hist1[1], qcd_sf)

    xerr = getBinWidth(hDATA) / 2


    # Main plot
    bin_center = getBinCenter(hDATA)
    hep.histplot([ h.hist for h in hist1],label=[h.desc for h in hist1],
                 color=[h.color for h in hist1],
                 ax=ax, stack=True, **PLOTSTYLE_HIST )


    ax.errorbar(
            bin_center,
            unumpy.nominal_values(data_value),
            xerr = xerr,
            yerr = unumpy.std_devs(data_value),
            label=hDATA.desc,
            **PLOTSTYLE_DATA )


    ax.set_xlabel('')
    #ax.set_ylabel(ylabel, fontsize=14, labelpad=18)
    ax.set_ylabel(ylabel)
    #max_num = max(getBinContent(hDATA))
    #order = getOrder(max_num)
    #ax.yaxis.set_major_locator(plt.MultipleLocator(order))
    #ax.yaxis.set_minor_locator(plt.MultipleLocator(0.2*order))
    ax.set_ylim(getHistMinForVisualization(hDATA, ySCALE), getHistMaxForVisualization(hDATA, ySCALE))
    ax.legend()
    if ySCALE == 'log':
        ax.set_yscale(ySCALE)
    else:
        ax.ticklabel_format(style='sci', axis='y', scilimits=(0,3), useMathText=True)

    ratio = [ u/d if d != 0 else ufloat(0,0) for u,d in zip(data_value, sign_value+fake_value) ]



    ax_ratio.errorbar(
        bin_center, unumpy.nominal_values(ratio), xerr=xerr, yerr=unumpy.std_devs(ratio), **PLOTSTYLE_DATA
    )
    #ax_ratio.xaxis.set_major_locator(plt.MultipleLocator(0.5))
    #ax_ratio.xaxis.set_minor_locator(plt.MultipleLocator(0.1))
    ax_ratio.set_xlabel(xLABEL)
    #ax_ratio.set_xlabel(xLABEL, fontsize=14, labelpad=5)

    ax_ratio.set_ylabel('data/MC')
    #ax_ratio.set_ylabel('data/MC', fontsize=14, labelpad=10)
    ax_ratio.set_ylim(0.5,1.5)
    ax_ratio.axhline(1, color='gray', linestyle='--')  # Reference line at ratio = 1

    plt.suptitle('')
    plt.subplots_adjust(hspace=0.1, top=0.92, left=0.15)

    hep.cms.label(ax=ax, **INFO_CMS_PRELIMIILARY_RUN2022EE)

    if figNAME:
        plt.savefig(figNAME)
        print(f'[SavedOutput] {figNAME}')
    else:
        plt.show()
        current_figsize = fig.get_size_inches()
        print(f"[AdjustedFigureSize] {current_figsize[0]} inches x {current_figsize[1]} inches")

if __name__ == "__main__":

# Open the ROOT file
    #file = uproot.open("dataMCcomp.root")
    #f_data = uproot.open('outfile_dataE_sideband.root')
    #f_sign = uproot.open('osig.root')
    #f_fake = uproot.open('obkg.root')
    f_data_= uproot.open('data_datasideband.root')
    f_data = uproot.open('data_signalregion.root')
    f_fake = uproot.open('qcd_madgraph.root')
    f_sign = uproot.open('sign_gjetmadgraph.root')

# Access the 'expdata' directory
    def getHistSet(tFILE, var, **xargs):
        h = tFILE[var]
        xargs['orig_obj'] = h
        return HistSet(h.to_hist(), **xargs)

    var_looping_info = [
            { 'var': 'b_HoverE',          'xLABEL': 'H / E'                      , 'figNAME': 'hB_HoverE.pdf'      ,'ySCALE': 'log'   },
            { 'var': 'b_sieie',           'xLABEL': '$\sigma_{i\eta i\eta}$'     , 'figNAME': 'hB_sieie.pdf'       ,'ySCALE': 'log'   },
            { 'var': 'b_sieip',           'xLABEL': '$\sigma_{i\eta i\phi}$'     , 'figNAME': 'hB_sieip.pdf'       ,'ySCALE': 'log'   },
            #{ 'var': 'b_pfChIso',         'xLABEL': 'charged Isolation [GeV]'    , 'figNAME': 'hB_chIso.pdf'       ,'ySCALE': 'log'   },
            #{ 'var': 'b_pfChIsoWorstVtx', 'xLABEL': 'chIso of worst vertex [GeV]', 'figNAME': 'hB_chIsoWorst.pdf'  ,'ySCALE': 'log'   },
            { 'var': 'b_r9',              'xLABEL': 'R9'                         , 'figNAME': 'hB_r9.pdf'          ,'ySCALE': 'log'   },
            { 'var': 'b_s4',              'xLABEL': 's4'                         , 'figNAME': 'hB_s4.pdf'          ,'ySCALE': 'log'   },
            { 'var': 'b_phiWidth',        'xLABEL': '$\phi$ width'               , 'figNAME': 'hB_phiWidth.pdf'    ,'ySCALE': 'log'   },
            { 'var': 'b_etaWidth',        'xLABEL': '$\eta$ width'               , 'figNAME': 'hB_etaWidth.pdf'    ,'ySCALE': 'log'   },
            { 'var': 'b_esEnergyOverRawE','xLABEL': 'ES energy over raw E'       , 'figNAME': 'hB_esEn_rawE.pdf'   ,'ySCALE': 'log'   },
            { 'var': 'b_energyRaw',       'xLABEL': 'raw Energy'                 , 'figNAME': 'hB_rawEnergy.pdf'   ,'ySCALE': 'log'   },
            { 'var': 'b_esEffSigmaRR',    'xLABEL': 'esEffSigmaRR'               , 'figNAME': 'hB_esEffSigmaRR.pdf','ySCALE': 'log'   },

            { 'var': 'e_HoverE',          'xLABEL': 'H / E'                      , 'figNAME': 'hE_HoverE.pdf'      ,'ySCALE': 'log'   },
            { 'var': 'e_sieie',           'xLABEL': '$\sigma_{i\eta i\eta}$'     , 'figNAME': 'hE_sieie.pdf'       ,'ySCALE': 'log'   },
            { 'var': 'e_sieip',           'xLABEL': '$\sigma_{i\eta i\phi}$'     , 'figNAME': 'hE_sieip.pdf'       ,'ySCALE': 'log'   },
            #{ 'var': 'e_pfChIso',         'xLABEL': 'charged Isolation [GeV]'    , 'figNAME': 'hE_chIso.pdf'       ,'ySCALE': 'log'   },
            #{ 'var': 'e_pfChIsoWorstVtx', 'xLABEL': 'chIso of worst vertex [GeV]', 'figNAME': 'hE_chIsoWorst.pdf'  ,'ySCALE': 'log'   },
            { 'var': 'e_r9',              'xLABEL': 'R9'                         , 'figNAME': 'hE_r9.pdf'          ,'ySCALE': 'log'   },
            { 'var': 'e_s4',              'xLABEL': 's4'                         , 'figNAME': 'hE_s4.pdf'          ,'ySCALE': 'log'   },
            { 'var': 'e_phiWidth',        'xLABEL': '$\phi$ width'               , 'figNAME': 'hE_phiWidth.pdf'    ,'ySCALE': 'log'   },
            { 'var': 'e_etaWidth',        'xLABEL': '$\eta$ width'               , 'figNAME': 'hE_etaWidth.pdf'    ,'ySCALE': 'log'   },
            { 'var': 'e_esEnergyOverRawE','xLABEL': 'ES energy over raw E'       , 'figNAME': 'hE_esEn_rawE.pdf'   ,'ySCALE': 'log'   },
            { 'var': 'e_energyRaw',       'xLABEL': 'raw Energy'                 , 'figNAME': 'hE_rawEnergy.pdf'   ,'ySCALE': 'log'   },
            { 'var': 'e_esEffSigmaRR',    'xLABEL': 'esEffSigmaRR'               , 'figNAME': 'hE_esEffSigmaRR.pdf','ySCALE': 'log'   },
    ]
    sf = -1.
    for var_info in var_looping_info:
        orig_sig_plot_name = var_info['var'].replace('_','orig_')
        orig_sig_fig_name = var_info['figNAME'].replace('_','orig_')
        
        hdata = getHistSet(f_data, f'{var_info["var"]}'   , desc='data'         , color='black')
        #hsign = getHistSet(f_sign, f'{var_info["var"]}'   , desc='sign', color='darkseagreen')
        hsignO= getHistSet(f_sign, orig_sig_plot_name     , desc='original sign', color='darkblue')
        hfake = getHistSet(f_fake, f'{var_info["var"]}'   , desc='QCD' , color='grey')

        #datalumi = 16.81
        datalumi = 26.6169
        ScaleWithoutAdditionalInfo(hfake, datalumi)
        #ScaleWithoutAdditionalInfo(hsign, datalumi)
        ScaleWithoutAdditionalInfo(hsignO, datalumi)
        #if sf < 0:
        #    sf = getScaleFactor_QCD_LOtoNLO(hdata, hsign,hfake)
        #sf = 16.81
        #Scale(hfake, sf)
        #Scale(hsign, sf)
        #ratio_plot(hdata, [hfake,hsign], xLABEL=var_info["xLABEL"], ylabel='Entries', ySCALE=var_info['ySCALE'], figNAME=var_info["figNAME"])
        ratio_plot(hdata, [hfake,hsignO], xLABEL=var_info["xLABEL"], ylabel='Entries', ySCALE=var_info['ySCALE'], figNAME=orig_sig_fig_name)
        plt.close()
