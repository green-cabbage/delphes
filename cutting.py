import ROOT
import math
import numpy as np

filename = "TTJets_DiLept_TuneCUETP8M1_14TeV-madgraphMLM-pythia8_326_0.root"

file = ROOT.TFile.Open(filename, "read")
tree = file.Get("Delphes")
n_entries = tree.GetEntries()
print(n_entries)
print (ROOT.__version__)
data = np.empty((0,6,6)) #np input array stack initialization


v_leptons = ROOT.std.vector('ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<float>>')()
tree.SetBranchAddress("ElectronCHS", v_leptons)

for event_entry in range(n_entries):
    tree.GetEntry(event_entry) # obtain the data
    v_leptons.clear() # clear previous assginments if any

#     if v_leptons[0].Pt() > 30:
#         continue
# row = np.zeros((1,6,6)) #initialization of input for filling
# data = np.vstack((data, row))