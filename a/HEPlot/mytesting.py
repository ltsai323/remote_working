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
def getBinCenter(h:HistSet, extraBINs:bool=False) -> list:
    bin_centers = h.hist.axes.centers[0]
    if extraBINs:
        print('use of extra bins')
        try:
            intervalL = 5. * (bin_centers[1]-bin_centers[0])
            intervalR = 5. * (bin_centers[-1]-bin_centers[-2])
            underflow_bin = bin_centers[0] - intervalL
            overflow_bin = bin_centers[-1] + intervalR
            bin_centers = np.insert(bin_centers,  0,underflow_bin)
            bin_centers = np.append(bin_centers, overflow_bin)
            return bin_centers
        except IndexError as e:
            mesg =f'[PossibleReason] Checking to len(bin_centers) = {len(bin_centers)}. Is it a very small value?'
            print(mesg)
            raise IndexError(e)
    return bin_centers
def getBinWidth(h:HistSet, extraBINs:bool=False) -> list:
    bin_widths = h.hist.axes.widths[0]
    if extraBINs:
        bin_widths = np.insert(bin_widths,  0, 1e-4)
        bin_widths = np.append(bin_widths, 1e-4)
        return bin_widths
    return bin_widths
def getBinData(h:HistSet, extraBINs:bool = False) -> list:
    ''' return a list of ufloat(). Get bin content with bin error '''
    values_with_OF_UF = h.orig_obj.values(flow=True)
    errors_with_OF_UF = h.orig_obj.errors(flow=True)
    #values_with_OF_UF[0] = 1e8
    #values_with_OF_UF[-1] = 1e8
    if extraBINs:
        return unumpy.uarray(values_with_OF_UF, errors_with_OF_UF)
    else:
        return unumpy.uarray(values_with_OF_UF[1:-1], errors_with_OF_UF[1:-1]) # remove under flow and over flow bins
def getBinContent(h:HistSet, extraBINs:bool=False) -> list:
    return unumpy.nominal_values(getBinData(h,extraBINs))
def getBinError(h:HistSet, extraBINs:bool=False) -> list:
    return unumpy.std_devs(getBinData(h,extraBINs))


def Scale(h:HistSet, scaleFACTOR:float):
    h.orig_obj._values *= scaleFACTOR
    h.orig_obj._variances *= scaleFACTOR*scaleFACTOR
    h.hist = h.orig_obj.to_hist() # update hist.Hist object
def ScaleWithInfo(h:HistSet, scaleFACTOR:float):
    Scale(h,scaleFACTOR)
    h.desc += f' (SF={scaleFACTOR:.1f})'
    

def getHistMinForVisualization(h:HistSet, outTYPE:str) -> float:
    if outTYPE == 'linear':
        return 0
    if outTYPE == 'log':
        try:
            c = getBinContent(h, True)
            return np.min(c[c!=0]) * 0.1
        except ValueError as e:
            print(f'\n\n[Unable to find minimun] use 1e-6 as lower bond')
            print(f'errors:\n    {e}')
            return 1e-6
    if outTYPE == 'original':
        return min(getBinContent(h, True))
    raise IOError(f'[InvalidArgument] getHistMinForVisualization() got outTYPE == "{ outTYPE }".')

def getHistMaxForVisualization(h:HistSet, outTYPE:str) -> float:
    if outTYPE == 'linear':
        return max(getBinContent(h)) * 2.0
    if outTYPE == 'log':
        return max(getBinContent(h)) * 1e3
    if outTYPE == 'original':
        return max(getBinContent(h))
    raise IOError(f'[InvalidArgument] getHistMaxForVisualization() got outTYPE == "{ outTYPE }".')

    




def getScaleFactor_QCD_LOtoNLO(hDATA:HistSet, hSIGN:HistSet, hQCD:HistSet):
    ''' SF = (N_data-N_sig) / N_QCD. And this SF is only applied on QCD, which compensates LO / NLO calculations. '''
    data_value = getBinData(hDATA, True)
    sign_value = getBinData(hSIGN, True)
    fake_value = getBinData(hQCD , True)

    qcd_scale_factor = ( np.sum( unumpy.nominal_values(data_value) ) - np.sum( unumpy.nominal_values(sign_value) ) )\
                       / np.sum( unumpy.nominal_values(fake_value) )
    return float(f'{qcd_scale_factor:.1f}')

    

PLOTSTYLE_DATA = { 'linestyle': 'None', 'color': 'black', 'marker': 'o' }
PLOTSTYLE_HIST = { 'histtype': 'fill', 'edgecolor': '1', 'linewidth': 0.5 }

INFO_CMS_PRELIMIILARY_UL2016PREVFP  = {'label':'Prelimilary', 'data':True, 'lumi':19.52, 'year':'UL2016preVFP' , 'loc':2}
INFO_CMS_PRELIMIILARY_UL2016POSTVFP = {'label':'Prelimilary', 'data':True, 'lumi':16.81, 'year':'UL2016postVFP', 'loc':2}
INFO_CMS_PRELIMIILARY_RUN2022EE = {'label':'Prelimilary', 'data':True, 'lumi':26.81, 'year':'2022EE', 'loc':2}
def ratio_plot(hDATA:HistSet, hist1:list, xLABEL, ylabel, ySCALE, extraBINs:bool=False, figNAME:str=''):
    hep.style.use(hep.style.ROOT) # For now ROOT defaults to CMS
    hep.style.use("CMS") # string aliases work too
    fig, (ax, ax_ratio) = plt.subplots(2, 1, gridspec_kw={'height_ratios': [3, 1]}, sharex=True)

    data_value = getBinData(hDATA, extraBINs)
    sign_value = getBinData(hist1[0], extraBINs)
    fake_value = getBinData(hist1[1], extraBINs)

    #qcd_scale_factor = ( np.sum( unumpy.nominal_values(data_value) ) - np.sum( unumpy.nominal_values(sign_value) ) )\
    #                   / np.sum( unumpy.nominal_values(fake_value) )

    #qcd_sf = float(f'{qcd_scale_factor:.2f}')
    #fake_value *= qcd_sf
    #Scale(hist1[1], qcd_sf)

    xerr = getBinWidth(hDATA, extraBINs) / 2


    # Main plot
    bin_center = getBinCenter(hDATA, extraBINs)


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
    f_data = uproot.open('data_datasideband.root')
    f_data_= uproot.open('data_signalregion.root')
    f_fake = uproot.open('qcd_madgraph.root')
    f_sign = uproot.open('sign_gjetmadgraph.root')

# Access the 'expdata' directory
    def getHistSet(tFILE, var, **xargs):
        h = tFILE[var]
        xargs['orig_obj'] = h
        return HistSet(h.to_hist(), **xargs)

    var_looping_info = [
            { 'var': 'bALL_PNetB',           'xLABEL':'B Score (ParticleNet)'       , 'figNAME': 'testhTagB_PNetB.pdf'    ,'ySCALE': 'log'   },
            { 'var': 'bALL_PNetCvsB',        'xLABEL':'CvsB Score (ParticleNet)'    , 'figNAME': 'testhTagB_PNetCvB.pdf'  ,'ySCALE': 'log'   },
            { 'var': 'bALL_PNetCvsL',        'xLABEL':'CvsL Score (ParticleNet)'    , 'figNAME': 'testhTagB_PNetCvL.pdf'  ,'ySCALE': 'log'   },
            { 'var': 'bALL_PNetQvsG',        'xLABEL':'QvsG Score (ParticleNet)'    , 'figNAME': 'testhTagB_PNetQvG.pdf'  ,'ySCALE': 'log'   },
    ]
    sf = -1.
    for var_info in var_looping_info:
        hdata = getHistSet(f_data, f'{var_info["var"]}'   , desc='data', color='black')
        hsign = getHistSet(f_sign, f'{var_info["var"]}'   , desc='sign', color='darkseagreen')
        hfake = getHistSet(f_fake, f'{var_info["var"]}'   , desc='QCD' , color='grey')

        datalumi = 26.6169
        Scale(hfake, datalumi)
        Scale(hsign, datalumi)
        #if sf < 0:
        #    sf = getScaleFactor_QCD_LOtoNLO(hdata, hsign,hfake)
        #sf = 16.81
        #ScaleWithInfo(hfake, sf)
        #ScaleWithInfo(hsign, sf)
        ratio_plot(hdata, [hfake,hsign], xLABEL=var_info["xLABEL"], ylabel='Entries', ySCALE=var_info['ySCALE'], figNAME=var_info["figNAME"], extraBINs=True)
        plt.close()
