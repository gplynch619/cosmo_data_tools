import os
from cosmo_data_tools.cmb.CMB import CMBLensingSpectrum
import numpy as np
import pandas as pd
from cosmo_data_tools import _ROOT

class planck_2022_NPIPE_PhiPhi(CMBLensingSpectrum):

    data_path = os.path.join(_ROOT, "data/cmb/planck_npipe/NPIPE_lensing_MV_bandpowers.txt")

    def __init__(self):
        if not os.path.isfile(planck_2022_NPIPE_PhiPhi.data_path):
            #os.system('curl "https://lambda.gsfc.nasa.gov/data/suborbital/SPT/sptpol_2019/bandpowers.dat" --create-dirs -o {}'.format(planck_2022_NPIPE_PhiPhi.data_path))
            raise FileNotFoundError("NPIPE lensing file not found. Please place it at {}".format(planck_2022_NPIPE_PhiPhi.data_path))

        self.path = planck_2022_NPIPE_PhiPhi.data_path
        d = self.get_data()
        df = pd.DataFrame(d)
   
        df.attrs = {"ell_factor": lambda l: (l*(l+1))**2/(2*np.pi),
                    "1e7": 1e7}
        super().__init__(df)

    def bibtex(self):
        bibtex_string = '''@article{Carron:2022eyg,
    author = "Carron, Julien and Mirmelstein, Mark and Lewis, Antony",
    title = "{CMB lensing from Planck PR4~maps}",
    eprint = "2206.07773",
    archivePrefix = "arXiv",
    primaryClass = "astro-ph.CO",
    doi = "10.1088/1475-7516/2022/09/039",
    journal = "JCAP",
    volume = "09",
    pages = "039",
    year = "2022"
}
        '''
        print(bibtex_string)

    def get_data(self):
        raw_data = np.loadtxt(self.path)
        d = {"ell": raw_data[:,1],
             "Cl": raw_data[:,4]*raw_data[:,3],
             "Cl_err": raw_data[:,5]*raw_data[:,3],
             }
        return d    