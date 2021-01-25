import numpy as np 
import matplotlib.pyplot as plt

branch_names = [ "ElectronCHS", "MuonTightCHS"] #["Jet", "ElectronCHS", "MuonTightCHS"]

for branch_name in branch_names:
    data = np.load("cut_data_pair_" + branch_name + ".npy")
    print(data.shape)
    names  = ["Pt", "Eta", "Phi"] # list of values to plot
    names_ranges = [ [0, 500],  [-3,3], [-3.2, 3.2]] # list of ranges for the respective values
    print(data.shape)
    for name_idx in range(len(names)):
        bins = np.linspace(names_ranges[name_idx][0], names_ranges[name_idx][1], 300)
        plt.hist(data[name_idx,:], bins, label =branch_name+" "+names[name_idx])
        plt.title(branch_name+" "+names[name_idx])
        plt.savefig(branch_name+" "+names[name_idx]+".png")
        plt.clf()
    