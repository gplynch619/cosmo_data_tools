import os
from cosmo_data_tools.cmb.CMB import CMBLensingSpectrum
import numpy as np
import pandas as pd
from cosmo_data_tools import _ROOT

class SPTpol_2019_PhiPhi(CMBLensingSpectrum):

    data_path = os.path.join(_ROOT, "data/cmb/sptpol/bandpowers.dat")

    def __init__(self):
        if not os.path.isfile(SPTpol_2019_PhiPhi.data_path):
            #os.system('wget -O {} "https://lambda.gsfc.nasa.gov/data/suborbital/SPT/spt_3g/SPT3G_2018_TTTEEE_MV_bdp.txt"'.format(SPT3G_2018_TTTEEE.data_path))
            os.system('curl "https://lambda.gsfc.nasa.gov/data/suborbital/SPT/sptpol_2019/bandpowers.dat" --create-dirs -o {}'.format(SPTpol_2019_PhiPhi.data_path))

        self.path = SPTpol_2019_PhiPhi.data_path
        d = self.get_data()
        df = pd.DataFrame(d)
   
        df.attrs = {"ell_factor": lambda l: (l*(l+1))**2/(2*np.pi),
                    }
        super().__init__(df)

    def bibtex(self):
        bibtex_string = '''@article{SPT:2019fqo,
    author = "Bianchini, F. and others",
    collaboration = "SPT",
    title = "{Constraints on Cosmological Parameters from the 500 deg$^2$ SPTpol Lensing Power Spectrum}",
    eprint = "1910.07157",
    archivePrefix = "arXiv",
    primaryClass = "astro-ph.CO",
    reportNumber = "FERMILAB-PUB-19-535-AE-PPD",
    doi = "10.3847/1538-4357/ab6082",
    journal = "Astrophys. J.",
    volume = "888",
    pages = "119",
    year = "2020"
        }
        '''
        print(bibtex_string)

    def get_data(self):
        raw_data = np.loadtxt(self.path)
        d = {"ell": raw_data[:,3],
             "Cl": raw_data[:,4]*raw_data[:,6],
             "Cl_err": raw_data[:,5]*raw_data[:,6],
             }
        return d    