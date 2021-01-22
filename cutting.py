import ROOT
import math
import numpy as np
import uproot
import awkward as ak
from typing import TypeVar, List

TTree = TypeVar('TTree')   

def get_array(
    tree : TTree,
    branch_name : str,
    flag_idx : int) -> List[float]:
    """
    param tree : a uproot TTree variable
    param branch_name : name of the TBranch of the TTree
    param flag_idx : indicator of the values to obtain
    0 -> Pt, 1 -> Eta, 2 -> Phi
    return: 2 D unregular ak array
    """
    flag_values = ["PT", "Eta", "Phi"]
    long_ass_key = branch_name + "." + flag_values[flag_idx]
    # print((tree[branch_name][long_ass_key].array()))
    return (tree[branch_name][long_ass_key].array())


filename = "TTJets_DiLept_TuneCUETP8M1_14TeV-madgraphMLM-pythia8_326_0.root"
# filename = "ttbarsignalplustau_fromDilepton_0.root"

# file = ROOT.TFile.Open(filename, "read")
file = uproot.open(filename)
print(file.keys())


tree = file['Delphes']

branch_names = ["Jet", "ElectronCHS", "MuonTightCHS"]
# final_indexes = [] # initialization of list of indexes that passed the cutting test
cut_data = {}
for branch_name in branch_names:
    pt_array = get_array(tree, branch_name, 0) # extract pt values
    eta_array = get_array(tree, branch_name, 1) # extract eta values
    phi_array = get_array(tree, branch_name, 2) # extract phi values
    Pts = []
    Etas = []
    Phis = []
    # for idx in range(len(tree["Jet"]["Jet.PT"].array())):
    for idx in range(len(pt_array)): # loop through events
        for jdx in range(len(pt_array[idx])): # loop through each particle in each event
                temp_Pts = []
                temp_Etas = []
                temp_Phis = []
            # Pt cut
            if (branch_name == "Jet"):
                if (pt_array[idx][jdx] <= 30):
                    continue
            else: #if lepton
                if (pt_array[idx][jdx] <= 25):
                    continue
            # Eta cut
            eta_array = get_array(tree, branch_name, 1) # extract Eta values
            if (eta_array[idx][jdx] >= 2.5 or eta_array[idx][jdx] <= -2.5):
                    continue
            # if all tests are passed
            # print(pt_array[idx][jdx])
            temp_Pts.append(pt_array[idx][jdx])
            temp_Etas.append(eta_array[idx][jdx])
            temp_Phis.append(phi_array[idx][jdx])
    assert( len(Pts) == len(Etas) and len(Etas) == len(Phis) )
    cut_data[branch_name] = np.array([Pts, Etas, Phis])
    np.save("cut_data_" + branch_name + ".npy", cut_data[branch_name])
    print("data saved")




# final_indexes = np.array(final_indexes)
# cut_data_shape  = (len(final_indexes), len(branch_names), 3) # 3 elems for Pt, Eta, Phi
# cut_data_shape = (len(Pts), len(branch_names), 3) 
# cut_data = np.zeros(cut_data_shape)
# for idx in range(len(branch_names)):
#     for jdx in range(3):
#         cut_data[:, idx, jdx] =  get_array(tree, branch_names[idx], jdx)


# old code below that I might use later

# tree = file.Get("Delphes")
# tree = file.Get("writeNTuple/NTuple")
# print(len(tree.keys()))
# print(type(tree))
# n_entries = tree.GetEntries()
# print(n_entries)
# # print (ROOT.__version__)
# data = np.empty((0,3,4)) #np input array stack initialization


# v_leptons = ROOT.std.vector('ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<float>>')()
# tree.SetBranchAddress("ElectronCHS", v_leptons)
# # tree.SetBranchAddress("leptons", v_leptons)


# for branch in tree:
    # tree.GetEntry(event_entry) # obtain the data
    # v_leptons.clear() # clear previous assginments if any
    # print(type(branch.keys()))
    # a = branch["ElectronCHS"]
    # print(a)
    # print("it's working")
# print(tree["ElectronCHS"].keys())
# print(len(tree["ElectronCHS"]["ElectronCHS.PT"].array()))
# print(len(tree["ElectronCHS"]["ElectronCHS.Eta"].array()))
# print(len(tree["Jet"]["Jet.PT"].array()))
# print(len(tree["Jet"]["Jet.Eta"].array()))
# print(len(tree["MuonTightCHS"]["MuonTightCHS.PT"].array()))
# print(len(tree["MuonTightCHS"]["MuonTightCHS.Eta"].array()))
# #     if v_leptons[0].Pt() > 30:
# #         continue
# # row = np.zeros((1,6,6)) #initialization of input for filling
# # data = np.vstack((data, row))