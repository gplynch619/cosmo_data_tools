import os
from cosmo_data_tools.cmb.CMB import CMBPowerSpectrum
import numpy as np
import pandas as pd
from cosmo_data_tools import _ROOT

class SPT3G_2018_TTTEEE(CMBPowerSpectrum):

    data_path = os.path.join(_ROOT, "data/cmb/spt3g/SPT3G_2018_TTTEEE_MV_bdp.txt")

    def __init__(self):
        if not os.path.isfile(SPT3G_2018_TTTEEE.data_path):
            os.system('wget -O {} "https://lambda.gsfc.nasa.gov/data/suborbital/SPT/spt_3g/SPT3G_2018_TTTEEE_MV_bdp.txt"'.format(SPT3G_2018_TTTEEE.data_path))
        self.path = SPT3G_2018_TTTEEE.data_path

        d = self.get_data()
        df = pd.DataFrame(d)
        df.attrs = {"ell_factor": d["ell"]*(d["ell"]+1)/(2*np.pi),
                    "uK2": SPT3G_2018_TTTEEE.Tcmb**2}
        super().__init__(df)

    def get_data(self):
        pass

    def bibtex(self):
        bibtex_string = '''@article{SPT-3G:2022hvq,
        author = "Balkenhol, L. and others",
        collaboration = "SPT-3G",
        title = "{Measurement of the CMB temperature power spectrum and constraints on cosmology from the SPT-3G 2018 TT, TE, and EE dataset}",
        eprint = "2212.05642",
        archivePrefix = "arXiv",
        primaryClass = "astro-ph.CO",
        reportNumber = "FERMILAB-PUB-22-953-PPD",
        doi = "10.1103/PhysRevD.108.023510",
        journal = "Phys. Rev. D",
        volume = "108",
        number = "2",
        pages = "023510",
        year = "2023"
        }
        '''
        print(bibtex_string)



class spt3g_2018_TT(SPT3G_2018_TTTEEE):

    def get_data(self):
        raw_data= np.loadtxt(self.path)
        d = {"ell": raw_data[9:,2],
             "Cl": raw_data[9:,3],
             "Cl_err":raw_data[9:,4],
             }
        return d
    
class spt3g_2018_TE(SPT3G_2018_TTTEEE):

    def get_data(self):
        raw_data= np.loadtxt(self.path)
        d = {"ell": raw_data[:,5],
             "Cl": raw_data[:,6],
             "Cl_err":raw_data[:,7],
             }
        return d
    
class spt3g_2018_EE(SPT3G_2018_TTTEEE):

    def get_data(self):
        raw_data= np.loadtxt(self.path)
        d = {"ell": raw_data[8:,8],
             "Cl": raw_data[8:,9],
             "Cl_err":raw_data[8:,10],
             }
        return d