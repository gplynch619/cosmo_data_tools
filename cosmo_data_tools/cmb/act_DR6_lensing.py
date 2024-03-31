import os
from cosmo_data_tools.cmb.CMB import CMBLensingSpectrum
import numpy as np
import pandas as pd
from cosmo_data_tools import _ROOT

class ACT_DR6_PhiPhi(CMBLensingSpectrum):

    data_path = os.path.join(_ROOT, "data/cmb/act/ACT_DR6_lensing_bandpower.txt")

    def __init__(self):
        if not os.path.isfile(ACT_DR6_PhiPhi.data_path):
            #os.system('curl "https://lambda.gsfc.nasa.gov/data/suborbital/SPT/sptpol_2019/bandpowers.dat" --create-dirs -o {}'.format(planck_2022_NPIPE_PhiPhi.data_path))
            raise FileNotFoundError("ACT DR6 lensing file not found. Please place it at {}".format(ACT_DR6_PhiPhi.data_path))

        self.path = ACT_DR6_PhiPhi.data_path
        d = self.get_data()
        df = pd.DataFrame(d)
   
        df.attrs = {"ell_factor": lambda l: (l*(l+1))**2/(2*np.pi),
                    "1e7": 1e7,
                    "pi/2": np.pi/2}
        super().__init__(df)

    def bibtex(self):
        bibtex_string = '''@article{ACT:2023dou,
    author = "Qu, Frank J. and others",
    collaboration = "ACT",
    title = "{The Atacama Cosmology Telescope: A Measurement of the DR6 CMB Lensing Power Spectrum and Its Implications for Structure Growth}",
    eprint = "2304.05202",
    archivePrefix = "arXiv",
    primaryClass = "astro-ph.CO",
    reportNumber = "FERMILAB-PUB-23-237-PPD",
    doi = "10.3847/1538-4357/acfe06",
    journal = "Astrophys. J.",
    volume = "962",
    number = "2",
    pages = "112",
    year = "2024"
}
        '''
        print(bibtex_string)

    def get_data(self):
        raw_data = np.loadtxt(self.path)
        d = {"ell": raw_data[:,2],
             "Cl": raw_data[:,3],
             "Cl_err": raw_data[:,4],
             }
        return d    