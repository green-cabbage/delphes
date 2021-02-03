import ROOT
import math
import numpy as np
import uproot
import awkward as ak
from typing import TypeVar, List

TTree = TypeVar('TTree')   
ak_array = TypeVar('ak_array')   
np_array = TypeVar('np_array')   

def get_array(
    tree : TTree,
    branch_name : str,
    flag_idx : int) -> List[float]:
    """
    param tree : a uproot TTree variable
    param branch_name : name of the TBranch of the TTree
    param flag_idx : indicator of the values to obtain
    0 -> Pt, 1 -> Eta, 2 -> Phi, 3 -> Charge
    return: 2 D unregular ak array
    """
    flag_values = ["PT", "Eta", "Phi", "Charge"]
    long_ass_key = branch_name + "." + flag_values[flag_idx]
    # print((tree[branch_name][long_ass_key].array()))
    return (tree[branch_name][long_ass_key].array())

def delta_eta(eta1, eta2):
    return np.abs(eta1 - eta2)

def delta_phi(phi1, phi2):
    """
    This code is taken from Jason
    """
    dphi = phi1 - phi2
    if dphi > math.pi:
        dphi = dphi - 2*math.pi        
    if dphi < -math.pi:
        dphi = dphi + 2*math.pi        
    return np.abs(dphi)

def lepton_pairing(
    Electron : List[ak_array],
    Muon : List[ak_array]) -> (List[float], List[float], List[float]) :
    """
    Electron and Muon contains values of ["PT", "Eta", "Phi", "Charge"] respectively
    """
    return_Electron = ak.Array([])
    return_Muon = ak.Array([])
    delta_etas = []
    delta_phis = []

    Electron = ak.to_list(Electron)
    Muon = ak.to_list(Muon)
    n_events = len(Electron[0]) # each particle has same n of events but may have 
    # different n of particles in each event
    for idx in range(n_events): # for each event
        for electron_jdx in range(len(Electron[0][idx])):
            for muon_jdx in range(len(Muon[0][idx])):
                print("Electron[-1][idx][electron_jdx]: ", Electron[-1][idx][electron_jdx])
                print("Muon[-1][idx][muon_jdx]: ", Muon[-1][idx][muon_jdx])
                if (Electron[-1][idx][electron_jdx] == -Muon[-1][idx][muon_jdx] ):
                    # if charge sign of electron is opposite of muon, then pairing is made and
                    # add the relevant values to the final return value
                    e_placeholder = []
                    for value in Electron:
                        e_placeholder.append(value[idx][electron_jdx])
                    return_Electron = ak.concatenate((return_Electron, ak.Array([e_placeholder])), axis =0)
                    # print(ak.to_numpy(return_Electron).shape)
                    # print("return_Electron: ", return_Electron)
                    m_placeholder = []
                    for value in Muon:
                        m_placeholder.append(value[idx][muon_jdx])
                    return_Muon = ak.concatenate((return_Muon, ak.Array([m_placeholder])), axis =0)
                    # print(ak.to_numpy(return_Muon).shape)
                    # print("return_Muon: ", return_Muon)
                    # add delta eta and phi values
                    delta_etas.append(delta_eta(Electron[1][idx][electron_jdx], Muon[1][idx][muon_jdx]))
                    delta_phis.append(delta_phi(Electron[-2][idx][electron_jdx], Muon[-2][idx][muon_jdx]))

                    # assign the respective charges as 10 (arbitrary number) to signify that they
                    # have been chosen already, and don't get detected next time
                    # print(type(Electron[-1][idx][electron_jdx]))
                    Electron[-1][idx][electron_jdx] = 10.0
                    Muon[-1][idx][muon_jdx] = 10.0

    delta_package = np.array([delta_etas, delta_phis])
    return (ak.to_numpy(return_Electron), ak.to_numpy(return_Muon), delta_package)


filename = "TTJets_DiLept_TuneCUETP8M1_14TeV-madgraphMLM-pythia8_326_0.root"
# filename = "ttbarsignalplustau_fromDilepton_0.root"

# file = ROOT.TFile.Open(filename, "read")
file = uproot.open(filename)
# print(file.keys())


tree = file['Delphes']

branch_names = [ "ElectronCHS", "MuonTightCHS"] #"Jet",
# final_indexes = [] # initialization of list of indexes that passed the cutting test
cut_data = {}
for branch_name in branch_names:
    # print(tree[branch_name].keys())
    pt_array = get_array(tree, branch_name, 0) # extract pt values
    eta_array = get_array(tree, branch_name, 1) # extract eta values
    phi_array = get_array(tree, branch_name, 2) # extract phi values
    charge_array = get_array(tree, branch_name, 3) # extract phi values
    # print("charge_array: ", charge_array)
    Pts = ak.Array([])
    Etas = ak.Array([])
    Phis = ak.Array([])
    Charges = ak.Array([])
    n_events = len(pt_array) # prev len(pt_array)
    # for idx in range(len(tree["Jet"]["Jet.PT"].array())):
    for idx in range(n_events): # loop through events prev 
        Pts_per_event = []
        Etas_per_event = []
        Phis_per_event = []
        Charges_per_event = []
        for jdx in range(len(pt_array[idx])): # loop through each particle in each event

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
            Pts_per_event.append(pt_array[idx][jdx])
            Etas_per_event.append(eta_array[idx][jdx])
            Phis_per_event.append(phi_array[idx][jdx])
            Charges_per_event.append(charge_array[idx][jdx])
        # now add the cut values as a new row
        Pts = ak.concatenate((Pts, ak.Array([Pts_per_event])), axis =0)
        Etas = ak.concatenate((Etas, ak.Array([Etas_per_event])), axis =0)
        Phis = ak.concatenate((Phis, ak.Array([Phis_per_event])), axis =0)
        Charges = ak.concatenate((Charges, ak.Array([Charges_per_event])), axis =0)
        assert( len(Pts) == len(Etas) and len(Etas) == len(Phis) )
        # print(Pts) 
    # print("Charges: ", Charges)
    cut_data[branch_name] = [Pts, Etas, Phis, Charges]
    # np.save("cut_data_" + branch_name + ".npy", cut_data[branch_name])

cut_data["ElectronCHS"],  cut_data["MuonTightCHS"], delta_package = lepton_pairing(cut_data["ElectronCHS"],cut_data["MuonTightCHS"])

np.save("cut_data_pair_" + "ElectronCHS" + ".npy", cut_data["ElectronCHS"])
np.save("cut_data_pair_" + "MuonTightCHS" + ".npy", cut_data["MuonTightCHS"])
np.save("cut_data_deltas.npy", delta_package)
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