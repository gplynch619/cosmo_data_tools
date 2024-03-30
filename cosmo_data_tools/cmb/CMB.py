import pandas as pd
import numpy as np
from cosmo_data_tools.CosmoData import CosmoData
from scipy.interpolate import CubicSpline

class CMBPowerSpectrum(CosmoData):

    Tcmb = 2725500.0

    def __init__(self, df):
        #self.ell_factor = pd.Series(df["ell"].values*(df["ell"].values+1)/(2*np.pi), index=df["ell"])
        self.ell_factor = df["ell"].values*(df["ell"].values+1)/(2*np.pi)
        self.lmin=df["ell"].min()
        self.lmax=df["ell"].max()
        try:
            assert "Cl" in df.columns
        except AssertionError as e:
            print("Dataframe does not contain a Dl or Cl column. Unexpected behavior may occur.")
        self.original_units = {k:v for k,v in df.attrs.items() if k!="ell_factor"}
        self.attrs = df.attrs
        self._to_cl(df) # Power spectra are stored as Cl's, converted to Dl's upon request

        if "Cl_err" in df.columns:
            yerr=df["Cl_err"]
        else:
            yerr=None
        super().__init__(df["ell"], df["Cl"], yerr=yerr)

    def _to_cl(self, df):
        """
        Converts dataframe to Cl's (does nothing if already in Cl form), same units
        """
        if "ell_factor" in df.attrs.keys():
            df["Cl"] /= self.ell_factor
            if "Cl_err" in df.columns:
                df["Cl_err"] /= self.ell_factor
            del df.attrs["ell_factor"]

    def Cl(self, l=None):
        return self.get_y(l)        

    def Dl(self, l=None):
        if l is None:
            return self.get_y()*self.ell_factor
        else:
            return self.get_y(l)*(l*(l+1)/(2*np.pi))    

    def Dl_err(self):
        return self.get_yerr()*self.ell_factor

    def Cl_err(self):
        return self.get_yerr()

    def ell(self):
        return self.data["x"].to_numpy()

    def units(self):
        unit_string = "*".join(list(self.attrs.keys()))
        return unit_string
    
    def _to_units(self, target_units):
        if target_units=="dimensionless":
            conversion_factor = 1./np.product(list(self.attrs.values()))
            self.attrs={}
        else:
            conversion_factor = np.product(list(target_units.values()))/np.product(list(self.attrs.values()))
            self.attrs = target_units

        self.data["y"]*=conversion_factor
        if "yerr" in self.data.columns:
            self.data["yerr"]*=conversion_factor

    def bibtex(self):
        pass

class Binner():

    def __init__(self, bin_edges):
        """
        bin_edges: array of bin edges

        for N bins there should be N+1 bin_edges (fence post problem)

        a bin [l, l+dl) contains values l, l+1, ... , l+dl-1

        for example [30, 35, 40] specifies two bins:
            bin 1 contains 30, 31, 32, 33, 34
            bin 2 35, 36, 37, 38, 39
        """
        self.bin_edges = bin_edges
        self.bins = list(zip(bin_edges[:-1], bin_edges[1:]))
        self.nbins = len(self.bins)
        self.lmin = self.bin_edges[0]
        self.lmax = self.bin_edges[-1] # not included


    def bin_data(self, data, weights="uniform"):
        if weights=="planck":
            self.planck_bin_weights_matrix()
        elif weights=="uniform":
            self.uniform_bin_weights_matrix()

        df = data.data.copy(deep=True)
        df = df[df["x"].between(self.lmin, self.lmax)]
        ell_b = np.matmul(self.bm, df["x"])
        Cl_b = np.matmul(self.bm, df["y"])
        var = df["yerr"]**2
        var_b = np.diag(np.matmul(self.bm, np.matmul(np.diag(var), self.bm.T)))
        d = {"ell": ell_b,
             "Cl": Cl_b,
             "Cl_err": np.sqrt(var_b)}
        df = pd.DataFrame(d)
        df.attrs={k:v for k,v in data.attrs.items() if k!="ell_factor"}
        return CMBPowerSpectrum(df)

    def planck_bin_weights_matrix(self):
        lrange = np.arange(self.lmin, self.lmax)
        self.bm = np.zeros((len(self.bins), len(lrange)))
        for i,bin in enumerate(self.bins):
            offset = bin[0]-self.lmin
            ells_in_bin = np.arange(bin[0], bin[-1])
            bin_weight_norm = np.sum([l*(l+1) for l in ells_in_bin])
            for j,ell in enumerate(ells_in_bin):
                self.bm[i,offset+j] = ell*(ell+1)/bin_weight_norm

    def uniform_bin_weights_matrix(self):
        lrange = np.arange(self.lmin, self.lmax)
        self.bm = np.zeros((len(self.bins), len(lrange)))
        for i,bin in enumerate(self.bins):
            offset = bin[0]-self.lmin
            ells_in_bin = np.arange(bin[0], bin[-1])
            bin_weight_norm = (bin[-1]-bin[0])
            for j,ell in enumerate(ells_in_bin):
                self.bm[i,offset+j] = 1.0/bin_weight_norm

