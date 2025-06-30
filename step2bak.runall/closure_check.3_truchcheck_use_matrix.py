import ROOT
from pprint import pprint

def example_matrix_inverse():
    # Create a 3x3 matrix
    matrix = ROOT.TMatrixD(3, 3)
    matrix[0][0] = 1; matrix[0][1] = 2; matrix[0][2] = 3
    matrix[1][0] = 0; matrix[1][1] = 1; matrix[1][2] = 4
    matrix[2][0] = 5; matrix[2][1] = 6; matrix[2][2] = 0

    # Print the original matrix
    print("Original Matrix:")
    matrix.Print()
    return matrix

    # Check if the matrix is invertible
    if matrix.Determinant() == 0:
        print("Matrix is singular and cannot be inverted.")
        return

    # Invert the matrix
    inverse = ROOT.TMatrixD(matrix)  # Make a copy of the original matrix
    inverse.Invert()

    # Print the inverse matrix
    print("Inverse Matrix:")
    inverse.Print()


class EffMatrix:
    def __init__(self, name,
            WPcL, WPcC, WPcB,
            WPbL, WPbC, WPbB,
            ):
        self.name = name
        self.matrix = ROOT.TMatrixD(3,3)
        self.matrix[0][0] = 1.  ; self.matrix[0][1] = 1.  ; self.matrix[0][2] = 1.
        self.matrix[1][0] = WPcL; self.matrix[1][1] = WPcC; self.matrix[1][2] = WPcB
        self.matrix[2][0] = WPbL; self.matrix[2][1] = WPbC; self.matrix[2][2] = WPbB

        if self.matrix.Determinant() == 0:
            print(f'[UnableToInvertMatrix] Matrix {self.name} got 0 determinant')
            return
        self.inverse = ROOT.TMatrixD(self.matrix) # make a copy of the original matrix
        self.inverse.Invert()
    def InvertMatrix(self):
        return getattr(self, 'inverse') if hasattr(self, 'inverse') else None
    def EffMatrix(self):
        return self.matrix

def Multiply(mat, vec):
    '''
    Multiply a matrix and vector
    '''
    if mat == None: return None
    outvec = ROOT.TVectorD(vec)

    for i in range(3):
        v = 0.
        for j in range(3):
            v += mat[i][j] * vec[j]
        outvec[i] = v
    return outvec


class FitInfo:
    def __init__(self, N0, NWPc, NWPb):
        self.vec = ROOT.TVectorD(3)
        self.vec[0] = N0
        self.vec[1] = NWPc
        self.vec[2] = NWPb
    def Unfold(self, effMATRIX):
        invMatrix = effMATRIX.InvertMatrix()
        self.unable_to_inv_matrix = (invMatrix == None)
        if self.error: return
        self.unfold_vec = Multiply( invMatrix, self.vec )
    @property
    def error(self):
        return self.unable_to_inv_matrix

    @property
    def Nl(self):
        if hasattr(self,'unfold_vec'):
            return getattr(self, 'unfold_vec')[0]
        return -999999
    @property
    def Nc(self):
        if hasattr(self,'unfold_vec'):
            return getattr(self, 'unfold_vec')[1]
        return -999999

    @property
    def Nb(self):
        if hasattr(self,'unfold_vec'):
            return getattr(self, 'unfold_vec')[2]
        return -999999


def ReadCSV(inCSV:str) -> list:
    import csv

    with open(inCSV, 'r') as fIN:
        read_entries = csv.DictReader(fIN)
        entries = [ entry for entry in read_entries ]
    #pprint(entries)
    return entries
class Binning:
    def __init__(self, pETAbin, jETAbin, pPTbin):
        self.pEtaBin = int(pETAbin)
        self.jEtaBin = int(jETAbin)
        self.pPtBin = int(pPTbin)
    def __str__(self):
        return f'Binning({self.pEtaBin},{self.jEtaBin},{self.pPtBin})'
    def __eq__(self,obj):
        return self.pEtaBin == obj.pEtaBin and self.jEtaBin == obj.jEtaBin and self.pPtBin == obj.pPtBin

def EntryInfo(entry:dict) -> FitInfo:
    return FitInfo(
            float(entry['N_WP0']),
            float(entry['N_WPc']),
            float(entry['N_WPb']),
            )
def TruthInfo(entries:list, binning:Binning) -> FitInfo:
    for entry in entries:
        this_bin = EntryBinning(entry)
        if not (this_bin == binning): continue

        return FitInfo(
                float(entry['numL']),
                float(entry['numC']),
                float(entry['numB']),
                )
    return None

def EntryBinning(entry:dict) -> Binning:
    return Binning(
            entry['pEtaBin'],
            entry['jEtaBin'],
            entry['pPtBin'])

def mainfunc(inFILE, inCSV, truthCSV, WPc, WPb):
    fIN = ROOT.TFile.Open(inFILE)
    entries = ReadCSV(inCSV)
    truth_entries = ReadCSV(truthCSV)


    for entry in entries:
        binning = EntryBinning(entry)
        truthinfo = TruthInfo(truth_entries, binning)

    # Run the example
        pPTbin = binning.pPtBin
        geteff = lambda effNAME: fIN.Get(effNAME).GetPointY(pPTbin)

        effWPcName = lambda qFLAV: f'bin{binning.pEtaBin}{binning.jEtaBin}{qFLAV}_{WPc}_eff'
        effWPbName = lambda qFLAV: f'bin{binning.pEtaBin}{binning.jEtaBin}{qFLAV}_{WPb}_eff'
        eff = EffMatrix( f'{WPc} {WPb}',
            geteff( effWPcName('L') ),
            geteff( effWPcName('C') ),
            geteff( effWPcName('B') ),

            geteff( effWPbName('L') ),
            geteff( effWPbName('C') ),
            geteff( effWPbName('B') ),
            )
        #eff.EffMatrix().Print()
        #eff.InvertMatrix().Print()

        #fitinfo = FitInfo(7178.674377362004,1783.125397787557,922.3100691099536)
        fitinfo = EntryInfo(entry)
        fitinfo.Unfold(eff)
        if fitinfo.error: continue
        print('\n')
        print(f'[Binning] {binning}')
        print('')
        print(f'[OrigValue] N0 = {fitinfo.vec[0]}')
        print(f'[OrigValue] NWPc = {fitinfo.vec[1]}')
        print(f'[OrigValue] NWPb = {fitinfo.vec[2]}')
        eff.EffMatrix().Print()
        print(f'[UnfoldedValue] Nl = {fitinfo.Nl} [TruthValue] Nl = {truthinfo.vec[0]}')
        print(f'[UnfoldedValue] Nc = {fitinfo.Nc} [TruthValue] Nc = {truthinfo.vec[1]}')
        print(f'[UnfoldedValue] Nb = {fitinfo.Nb} [TruthValue] Nb = {truthinfo.vec[2]}')
        print('\n\n\n')



    fIN.Close()


def testfunc():
    m = example_matrix_inverse()

    # Step 3: Define a 3D vector
    vector = ROOT.TVectorD(3)
    vector[0] = 1
    vector[1] = 2
    vector[2] = 3

    print("Original Vector:")
    vector.Print()

    m.Print()
    # Step 4: Multiply inverse matrix by vector
    result_vector = ROOT.TVectorD(3)
    result_vector = m * vector

    print("Result Vector (Inverse Matrix × Vector):")
    result_vector.Print()

if __name__ == "__main__":
    WPc = 'WPcL'
    WPb = 'WPbL'
    #eff_file = 'WPeff_2022GJetPythiaFlat.root'
    eff_file = 'WPeff_2022GJetMadgraph.root'
    fit_csv = f'scanres_{WPc}_{WPb}/fake_merged_fitinfo.csv'
    truth_csv = f'scanres_{WPc}_{WPb}/fake_merged_truthinfo.csv'
    mainfunc(eff_file,fit_csv, truth_csv, WPc, WPb)
    #testfunc2()

