import os
from cosmo_data_tools.cmb.CMB import CMBPowerSpectrum
import numpy as np
import pandas as pd
from cosmo_data_tools import _ROOT

class SPT3G_2018_TTEE(CMBPowerSpectrum):

    data_path = os.path.join(_ROOT, "data/cmb/spt3g/bp_for_plotting_v3.txt")

    def __init__(self):
        if not os.path.isfile(SPT3G_2018_TTEE.data_path):
            os.system('wget -O {} "https://pole.uchicago.edu/public/data/dutcher21/bp_for_plotting_v3.txt"'.format(SPT3G_2018_TTEE.data_path))
        self.path = SPT3G_2018_TTEE.data_path

        d = self.get_data()
        df = pd.DataFrame(d)
        df.attrs = {"ell_factor": d["ell"]*(d["ell"]+1)/(2*np.pi),
                    "uK2": SPT3G_2018_TTEE.Tcmb**2}
        super().__init__(df)

    def get_data(self):
        pass

    def bibtex(self):
        bibtex_string = '''@article{SPT-3G:2021eoc,
        author = "Dutcher, D. and others",
        collaboration = "SPT-3G",
        title = "{Measurements of the E-mode polarization and temperature-E-mode correlation of the CMB from SPT-3G 2018 data}",
        eprint = "2101.01684",
        archivePrefix = "arXiv",
        primaryClass = "astro-ph.CO",
        reportNumber = "FERMILAB-PUB-21-137-AE",
        doi = "10.1103/PhysRevD.104.022003",
        journal = "Phys. Rev. D",
        volume = "104",
        number = "2",
        pages = "022003",
        year = "2021"
        }
        '''
        print(bibtex_string)

class spt3g_2018_TE(SPT3G_2018_TTEE):

    def get_data(self):
        raw_data= np.loadtxt(self.path)
        d = {"ell": raw_data[:,2],
             "Cl": raw_data[:,3],
             "Cl_err":raw_data[:,4],
             }
        return d
    
class spt3g_2018_EE(SPT3G_2018_TTEE):

    def get_data(self):
        raw_data= np.loadtxt(self.path)
        d = {"ell": raw_data[:,5],
             "Cl": raw_data[:,6],
             "Cl_err":raw_data[:,7],
             }
        return d