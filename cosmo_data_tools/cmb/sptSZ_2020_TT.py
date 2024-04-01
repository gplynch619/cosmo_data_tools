import os
from cosmo_data_tools.cmb.CMB import CMBPowerSpectrum
import numpy as np
import pandas as pd
from cosmo_data_tools import _ROOT

class SPTSZ_2020_TT(CMBPowerSpectrum):

    data_path = os.path.join(_ROOT, "data/cmb/sptSZ/plotting_bandpowers.txt")

    def __init__(self):
        if not os.path.isfile(SPTSZ_2020_TT.data_path):
            #os.system('wget -O {} "https://lambda.gsfc.nasa.gov/data/suborbital/SPT/spt_3g/SPT3G_2018_TTTEEE_MV_bdp.txt"'.format(SPT3G_2018_TTTEEE.data_path))
            os.system('curl "https://lambda.gsfc.nasa.gov/data/suborbital/SPT/reichardt_2020/plotting_bandpowers.txt" --create-dirs -o {}'.format(SPTSZ_2020_TT.data_path))

        self.path = SPTSZ_2020_TT.data_path

        d = self.get_data()
        df = pd.DataFrame(d)
        df.attrs = {"ell_factor": lambda l: l*(l+1)/(2*np.pi),
                    "uK2": SPTSZ_2020_TT.Tcmb**2}
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

    def get_data(self):
        raw_data= np.genfromtxt(self.path)
        d = {"ell": raw_data[:,1],
             "Cl": raw_data[:,8],
             "Cl_err":raw_data[:,9],
             }
        return d
