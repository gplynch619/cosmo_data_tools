import os
from cosmo_data_tools.cmb.CMB import CMBPowerSpectrum
import numpy as np
import pandas as pd
from inspect import cleandoc
from cosmo_data_tools import _ROOT

class Planck2018(CMBPowerSpectrum):

    def __init__(self, path):
        self.path = path
        raw_data= np.loadtxt(path)
        d = {"ell": raw_data[:,0],
             "Cl": raw_data[:,1],
             "Cl_err": (raw_data[:,2]+raw_data[:,3])/2 #only support for symmetric errors right now
            }
        df = pd.DataFrame(d)
        df.attrs = {"ell_factor": d["ell"]*(d["ell"]+1)/(2*np.pi),
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



class planck_2018_highl_TT(Planck2018):

    data_path = os.path.join(_ROOT, "data/cmb/planck/COM_PowerSpect_CMB-TT-binned_R3.01.txt")

    def __init__(self):
        if not os.path.isfile(planck_2018_highl_TT.data_path):
            os.system('wget -O {} "http://pla.esac.esa.int/pla/aio/product-action?COSMOLOGY.FILE_ID=COM_PowerSpect_CMB-TT-binned_R3.01.txt"'.format(planck_2018_highl_TT.data_path))
        super().__init__(planck_2018_highl_TT.data_path)

class planck_2018_highl_TE(Planck2018):

    data_path = os.path.join(_ROOT, "data/cmb/planck/COM_PowerSpect_CMB-TE-binned_R3.02.txt")

    def __init__(self):
        if not os.path.isfile(planck_2018_highl_TE.data_path):
            os.system('wget -O {} "http://pla.esac.esa.int/pla/aio/product-action?COSMOLOGY.FILE_ID=COM_PowerSpect_CMB-TE-binned_R3.02.txt"'.format(planck_2018_highl_TE.data_path))
        super().__init__(planck_2018_highl_TE.data_path)

class planck_2018_highl_EE(Planck2018):

    data_path = os.path.join(_ROOT, "data/cmb/planck/COM_PowerSpect_CMB-EE-binned_R3.02.txt")

    def __init__(self):
        if not os.path.isfile(planck_2018_highl_EE.data_path):
            os.system('wget -O {} "http://pla.esac.esa.int/pla/aio/product-action?COSMOLOGY.FILE_ID=COM_PowerSpect_CMB-EE-binned_R3.02.txt"'.format(planck_2018_highl_EE.data_path))
        super().__init__(planck_2018_highl_EE.data_path)

class planck_2018_highl_TT_unbinned(Planck2018):

    data_path = os.path.join(_ROOT, "data/cmb/planck/COM_PowerSpect_CMB-TT-full_R3.01.txt")

    def __init__(self):
        if not os.path.isfile(planck_2018_highl_TT_unbinned.data_path):
            os.system('wget -O {} "http://pla.esac.esa.int/pla/aio/product-action?COSMOLOGY.FILE_ID=COM_PowerSpect_CMB-TT-full_R3.01.txt"'.format(planck_2018_highl_TT_unbinned.data_path))
        super().__init__(planck_2018_highl_TT_unbinned.data_path)

class planck_2018_highl_TE_unbinned(Planck2018):

    data_path = os.path.join(_ROOT, "data/cmb/planck/COM_PowerSpect_CMB-TE-full_R3.01.txt")

    def __init__(self):
        if not os.path.isfile(planck_2018_highl_TE_unbinned.data_path):
            os.system('wget -O {} "http://pla.esac.esa.int/pla/aio/product-action?COSMOLOGY.FILE_ID=COM_PowerSpect_CMB-TE-full_R3.01.txt"'.format(planck_2018_highl_TE_unbinned.data_path))
        super().__init__(planck_2018_highl_TE_unbinned.data_path)

class planck_2018_highl_EE_unbinned(Planck2018):

    data_path = os.path.join(_ROOT, "data/cmb/planck/COM_PowerSpect_CMB-TE-full_R3.01.txt")

    def __init__(self):
        if not os.path.isfile(planck_2018_highl_EE_unbinned.data_path):
            os.system('wget -O {} "http://pla.esac.esa.int/pla/aio/product-action?COSMOLOGY.FILE_ID=COM_PowerSpect_CMB-EE-full_R3.01.txt"'.format(planck_2018_highl_EE_unbinned.data_path))
        super().__init__(planck_2018_highl_EE_unbinned.data_path)