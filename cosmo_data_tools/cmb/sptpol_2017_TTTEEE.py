import os
from cosmo_data_tools.cmb.CMB import CMBPowerSpectrum
import numpy as np
import pandas as pd
from cosmo_data_tools import _ROOT

class SPTpol_2017_TTTEEE(CMBPowerSpectrum):

    data_path = os.path.join(_ROOT, "data/cmb/sptpol/bandpowers_sptpol_500deg2_TTEETE.txt")

    def __init__(self):
        if not os.path.isfile(SPTpol_2017_TTTEEE.data_path):
            #os.system('wget -O {} "https://lambda.gsfc.nasa.gov/data/suborbital/SPT/spt_3g/SPT3G_2018_TTTEEE_MV_bdp.txt"'.format(SPT3G_2018_TTTEEE.data_path))
            os.system('curl "https://lambda.gsfc.nasa.gov/data/suborbital/SPT/sptpol_2017/bandpowers_sptpol_500deg2_TTEETE.txt" --create-dirs -o {}'.format(SPTpol_2017_TTTEEE.data_path))

        self.path = SPTpol_2017_TTTEEE.data_path

        d = self.get_data()
        df = pd.DataFrame(d)
        df.attrs = {"ell_factor": lambda l: l*(l+1)/(2*np.pi),
                    "uK2": SPTpol_2017_TTTEEE.Tcmb**2}
        super().__init__(df)

    def get_data(self):
        pass

    def bibtex(self):
        bibtex_string = '''@article{SPT:2017jdf,
    author = "Henning, J. W. and others",
    collaboration = "SPT",
    title = "{Measurements of the Temperature and E-Mode Polarization of the CMB from 500 Square Degrees of SPTpol Data}",
    eprint = "1707.09353",
    archivePrefix = "arXiv",
    primaryClass = "astro-ph.CO",
    reportNumber = "FERMILAB-PUB-17-297-AE",
    doi = "10.3847/1538-4357/aa9ff4",
    journal = "Astrophys. J.",
    volume = "852",
    number = "2",
    pages = "97",
    year = "2018"
}
        '''
        print(bibtex_string)



class sptpol_2017_TT(SPTpol_2017_TTTEEE):

    def get_data(self):
        raw_data= np.loadtxt(self.path)
        d = {"ell": raw_data[:,2],
             "Cl": raw_data[:,3],
             "Cl_err":raw_data[:,4],
             }
        return d
    
class sptpol_2017_TE(SPTpol_2017_TTTEEE):

    def get_data(self):
        raw_data= np.loadtxt(self.path)
        d = {"ell": raw_data[:,8],
             "Cl": raw_data[:,9],
             "Cl_err":raw_data[:,10],
             }
        return d
    
class sptpol_2017_EE(SPTpol_2017_TTTEEE):

    def get_data(self):
        raw_data= np.loadtxt(self.path)
        d = {"ell": raw_data[:,5],
             "Cl": raw_data[:,6],
             "Cl_err":raw_data[:,7],
             }
        return d