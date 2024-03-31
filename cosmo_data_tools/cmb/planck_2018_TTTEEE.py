import os
from cosmo_data_tools.cmb.CMB import CMBPowerSpectrum
import numpy as np
import pandas as pd
from inspect import cleandoc
from cosmo_data_tools import _ROOT

class Planck2018(CMBPowerSpectrum):

    def __init__(self):
        
        d = self.get_data()

        df = pd.DataFrame(d)
        df.attrs = {"ell_factor": lambda l: l*(l+1)/(2*np.pi),
                    "uK2": Planck2018.Tcmb**2}
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

class planck_2018_TT(Planck2018):

    data_path = os.path.join(_ROOT, "data/cmb/planck/COM_PowerSpect_CMB-TT-binned_R3.01.txt")

    def get_data(self):
        if not os.path.isfile(self.data_path):
            os.system('curl "http://pla.esac.esa.int/pla/aio/product-action?COSMOLOGY.FILE_ID=COM_PowerSpect_CMB-TT-binned_R3.01.txt" --create-dirs -o {}'.format(self.data_path))
        
        raw_data= np.loadtxt(self.data_path)
        d = {"ell": raw_data[:,0],
             "Cl": raw_data[:,1],
             "Cl_err": (raw_data[:,2]+raw_data[:,3])/2 #only support for symmetric errors right now
            }
        return d


class planck_2018_TE(Planck2018):

    data_path = os.path.join(_ROOT, "data/cmb/planck/COM_PowerSpect_CMB-TE-binned_R3.02.txt")

    def get_data(self):
        if not os.path.isfile(self.data_path):
            os.system('curl "http://pla.esac.esa.int/pla/aio/product-action?COSMOLOGY.FILE_ID=COM_PowerSpect_CMB-TE-binned_R3.02.txt" --create-dirs -o {}'.format(self.data_path))
        
        raw_data= np.loadtxt(self.data_path)
        d = {"ell": raw_data[:,0],
             "Cl": raw_data[:,1],
             "Cl_err": (raw_data[:,2]+raw_data[:,3])/2 #only support for symmetric errors right now
            }
        return d

class planck_2018_EE(Planck2018):

    data_path = os.path.join(_ROOT, "data/cmb/planck/COM_PowerSpect_CMB-EE-binned_R3.02.txt")

    def get_data(self):
        if not os.path.isfile(self.data_path):
            os.system('curl "http://pla.esac.esa.int/pla/aio/product-action?COSMOLOGY.FILE_ID=COM_PowerSpect_CMB-EE-binned_R3.02.txt" --create-dirs -o {}'.format(self.data_path))
        
        raw_data= np.loadtxt(self.data_path)
        d = {"ell": raw_data[:,0],
             "Cl": raw_data[:,1],
             "Cl_err": (raw_data[:,2]+raw_data[:,3])/2 #only support for symmetric errors right now
            }
        return d
    
class planck_2018_TT_unbinned(Planck2018):

    data_path = os.path.join(_ROOT, "data/cmb/planck/COM_PowerSpect_CMB-TT-full_R3.01.txt")

    def get_data(self):
        if not os.path.isfile(self.data_path):
            os.system('curl "http://pla.esac.esa.int/pla/aio/product-action?COSMOLOGY.FILE_ID=COM_PowerSpect_CMB-TT-full_R3.01.txt" --create-dirs -o {}'.format(self.data_path))
        
        raw_data= np.loadtxt(self.data_path)
        d = {"ell": raw_data[:,0],
             "Cl": raw_data[:,1],
             "Cl_err": (raw_data[:,2]+raw_data[:,3])/2 #only support for symmetric errors right now
            }
        return d

class planck_2018_TE_unbinned(Planck2018):

    data_path = os.path.join(_ROOT, "data/cmb/planck/COM_PowerSpect_CMB-TE-full_R3.01.txt")

    def get_data(self):
        if not os.path.isfile(self.data_path):
            os.system('curl "http://pla.esac.esa.int/pla/aio/product-action?COSMOLOGY.FILE_ID=COM_PowerSpect_CMB-TE-full_R3.01.txt" --create-dirs -o {}'.format(self.data_path))
        
        raw_data= np.loadtxt(self.data_path)
        d = {"ell": raw_data[:,0],
             "Cl": raw_data[:,1],
             "Cl_err": (raw_data[:,2]+raw_data[:,3])/2 #only support for symmetric errors right now
            }
        return d

class planck_2018_EE_unbinned(Planck2018):

    data_path = os.path.join(_ROOT, "data/cmb/planck/COM_PowerSpect_CMB-EE-full_R3.01.txt")

    def get_data(self):
        if not os.path.isfile(self.data_path):
            os.system('curl "http://pla.esac.esa.int/pla/aio/product-action?COSMOLOGY.FILE_ID=COM_PowerSpect_CMB-EE-full_R3.01.txt" --create-dirs -o {}'.format(self.data_path))
        
        raw_data= np.loadtxt(self.data_path)
        d = {"ell": raw_data[:,0],
             "Cl": raw_data[:,1],
             "Cl_err": (raw_data[:,2]+raw_data[:,3])/2 #only support for symmetric errors right now
            }
        return d
    
class Planck2018_bestfit(Planck2018):

    data_path = os.path.join(_ROOT, "data/cmb/planck/COM_PowerSpect_CMB-base-plikHM-TTTEEE-lowl-lowE-lensing-minimum-theory_R3.01.txt")
    cal_planck_bf = 0.1000442E+01 # from PLA

class planck_2018_TT_bestfit(Planck2018_bestfit):

    def get_data(self):
        if not os.path.isfile(self.data_path):
            os.system('curl http://pla.esac.esa.int/pla/aio/product-action?COSMOLOGY.FILE_ID=COM_PowerSpect_CMB-base-plikHM-TTTEEE-lowl-lowE-lensing-minimum-theory_R3.01.txt --create-dirs -o {}'.format(self.data_path))
  
        raw_data = np.loadtxt(self.data_path)
        d = {"ell": raw_data[:,0],
             "Cl": raw_data[:,1]/self.cal_planck_bf**2}

        return d
    
class planck_2018_TE_bestfit(Planck2018_bestfit):

    def get_data(self):
        if not os.path.isfile(self.data_path):
            os.system('curl http://pla.esac.esa.int/pla/aio/product-action?COSMOLOGY.FILE_ID=COM_PowerSpect_CMB-base-plikHM-TTTEEE-lowl-lowE-lensing-minimum-theory_R3.01.txt --create-dirs -o {}'.format(self.data_path))
  
        raw_data = np.loadtxt(self.data_path)
        d = {"ell": raw_data[:,0],
             "Cl": raw_data[:,2]/self.cal_planck_bf**2}

        return d
    
class planck_2018_EE_bestfit(Planck2018_bestfit):

    def get_data(self):
        if not os.path.isfile(self.data_path):
            os.system('curl http://pla.esac.esa.int/pla/aio/product-action?COSMOLOGY.FILE_ID=COM_PowerSpect_CMB-base-plikHM-TTTEEE-lowl-lowE-lensing-minimum-theory_R3.01.txt --create-dirs -o {}'.format(self.data_path))
  
        raw_data = np.loadtxt(self.data_path)
        d = {"ell": raw_data[:,0],
             "Cl": raw_data[:,3]/self.cal_planck_bf**2}

        return d