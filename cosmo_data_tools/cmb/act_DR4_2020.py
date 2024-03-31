import os
import tarfile
from cosmo_data_tools.cmb.CMB import CMBPowerSpectrum
import numpy as np
import pandas as pd
from inspect import cleandoc
from cosmo_data_tools import _ROOT

class ACT_DR4(CMBPowerSpectrum):

    tar_file = os.path.join(_ROOT, "data/cmb/act/act_dr4.01_cmbonly_spectra.tar.gz")

    def __init__(self):
        
        d = self.get_data()

        df = pd.DataFrame(d)
        df.attrs = {"ell_factor": lambda l: l*(l+1)/(2*np.pi),
                    "uK2": ACT_DR4.Tcmb**2}
        super().__init__(df)

    def bibtex(self):
        bibtex_string = '''@article{Planck:2018vyg,
        author = "Aghanim, N. and others",
        collaboration = "Planck",
        title = "{Planck 2018 results. VI. Cosmological parameters}",
        eprint = "1807.06209",
        archivePrefix = "arXiv",
        primaryClass = "astro-ph.CO",
        doi = "10.1051/0004-6361/201833910",
        journal = "Astron. Astrophys.",
        volume = "641",
        pages = "A6",
        year = "2020",
        note = "[Erratum: Astron.Astrophys. 652, C4 (2021)]"
        } '''
        print(bibtex_string)

    def get_data(self):
        pass

class act_dr4_TT(ACT_DR4):

    data_path = os.path.join(_ROOT, "data/cmb/act/cmbonly_spectra_dr4.01/act_dr4.01_D_ell_TT_cmbonly.txt")
    def get_data(self):
        if not os.path.isfile(self.data_path):
            if not os.path.isfile(ACT_DR4.tar_file):    
                os.system('curl "https://lambda.gsfc.nasa.gov/data/suborbital/ACT/ACT_dr4/spectra/act_dr4.01_cmbonly_spectra.tar.gz" --create-dirs -o {}'.format(ACT_DR4.tar_file))
            os.system('cd {} && tar -xvzf {}'.format(os.path.dirname(ACT_DR4.tar_file), ACT_DR4.tar_file))

        raw_data= np.loadtxt(self.data_path)
        d = {"ell": raw_data[:,0],
             "Cl": raw_data[:,1],
             "Cl_err": raw_data[:,2] #only support for symmetric errors right now
            }
        return d
    
class act_dr4_TE(ACT_DR4):

    data_path = os.path.join(_ROOT, "data/cmb/act/cmbonly_spectra_dr4.01/act_dr4.01_D_ell_TE_cmbonly.txt")
    def get_data(self):
        if not os.path.isfile(self.data_path):
            if not os.path.isfile(ACT_DR4.tar_file):    
                os.system('curl "https://lambda.gsfc.nasa.gov/data/suborbital/ACT/ACT_dr4/spectra/act_dr4.01_cmbonly_spectra.tar.gz" --create-dirs -o {}'.format(ACT_DR4.tar_file))
            os.system('cd {} && tar -xvzf {}'.format(os.path.dirname(ACT_DR4.tar_file), ACT_DR4.tar_file))

        raw_data= np.loadtxt(self.data_path)
        d = {"ell": raw_data[:,0],
             "Cl": raw_data[:,1],
             "Cl_err": raw_data[:,2] #only support for symmetric errors right now
            }
        return d
    
class act_dr4_EE(ACT_DR4):

    data_path = os.path.join(_ROOT, "data/cmb/act/cmbonly_spectra_dr4.01/act_dr4.01_D_ell_EE_cmbonly.txt")
    def get_data(self):
        if not os.path.isfile(self.data_path):
            if not os.path.isfile(ACT_DR4.tar_file):    
                os.system('curl "https://lambda.gsfc.nasa.gov/data/suborbital/ACT/ACT_dr4/spectra/act_dr4.01_cmbonly_spectra.tar.gz" --create-dirs -o {}'.format(ACT_DR4.tar_file))
            os.system('cd {} && tar -xvzf {}'.format(os.path.dirname(ACT_DR4.tar_file), ACT_DR4.tar_file))

        raw_data= np.loadtxt(self.data_path)
        d = {"ell": raw_data[:,0],
             "Cl": raw_data[:,1],
             "Cl_err": raw_data[:,2] #only support for symmetric errors right now
            }
        return d