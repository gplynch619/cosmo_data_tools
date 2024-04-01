import pandas as pd
import numpy as np
from cosmo_data_tools.CosmoData import CosmoData
from scipy.interpolate import CubicSpline

class CMBPowerSpectrum(CosmoData):

    Tcmb = 2725500.0

    def __init__(self, df):
        #self.ell_factor = pd.Series(df["ell"].values*(df["ell"].values+1)/(2*np.pi), index=df["ell"])
        self.lmin=df["ell"].min()
        self.lmax=df["ell"].max()
        try:
            assert "Cl" in df.columns
        except AssertionError as e:
            print("Dataframe does not contain a Dl or Cl column. Unexpected behavior may occur.")
        self._original_units = {k:v for k,v in df.attrs.items() if k!="ell_factor"}
        self.units = {k:v for k,v in df.attrs.items() if k!="ell_factor"}

        if not self._original_units:
            self._original_units = {"dimensionless": 1.0}
            self.units = {"dimensionless": 1.0}

        self._plot_fmt = {}

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
        for name,value in df.attrs.items():
            if name=="ell_factor":
                df["Cl"] /= value(df["ell"])
                if "Cl_err" in df.columns:
                    df["Cl_err"] /= value(df["ell"])
            else:
                df["Cl"] /= value
                if "Cl_err" in df.columns:
                    df["Cl_err"] /= value
            #del df.attrs["ell_factor"]

    def Cl(self, l=None):
        return self.unit_factor()*self.get_y(l)        

    def Dl(self, l=None):
        if l is None:
            return self.unit_factor()*self.get_y()*(self.ell()*(self.ell()+1))/(2*np.pi)
        else:
            return self.unit_factor()*self.get_y(l)*(l*(l+1)/(2*np.pi))    

    def Dl_err(self):
        return self.unit_factor()*self.get_yerr()*(self.ell()*(self.ell()+1))/(2*np.pi)

    def Cl_err(self):
        return self.unit_factor()*self.get_yerr()

    def ell(self):
        return self.data["x"].to_numpy()

    def subset(self, start, stop):
        d={}
        sub_data= self.data[self.data["x"].between(start, stop)]
        d["ell"] = sub_data["x"]
        d["Cl"] = self.unit_factor()*sub_data["y"]
        if "yerr" in self.data.columns:
            d["Cl_err"] = self.unit_factor()*sub_data["yerr"]
        df = pd.DataFrame(d)
        df.attrs = self.units
        return CMBPowerSpectrum(df)

    def print_units(self):
        unit_string = "*".join(list(self.units.keys()))
        print(unit_string)
    
    def unit_factor(self):
        return np.product(list(self.units.values()))

    def to_units(self, target_units):
        if target_units=="dimensionless":
            self.units={"dimensionless": 1.0}
        else:
            self.units = target_units
    
    @property
    def plot_fmt(self):
        return self._plot_fmt
    
    @plot_fmt.setter
    def plot_fmt(self, fmt):
        self._plot_fmt = fmt
    
    def bibtex(self):
        pass

class CMBLensingSpectrum(CMBPowerSpectrum):

    def Dl(self, l=None):
        if l is None:
            return self.unit_factor()*self.get_y()*(self.ell()*(self.ell()+1))**2/(2*np.pi)
        else:
            return self.unit_factor()*self.get_y(l)*((l*(l+1))**2/(2*np.pi))    

    def Dl_err(self):
        return self.unit_factor()*self.get_yerr()*(self.ell()*(self.ell()+1))**2/(2*np.pi)
    
    def L(self):
        return self.ell()
    
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


        sub_data = data.subset(self.lmin, self.lmax-1) # -1 to account for the fact that the right bin edge is not included
        df = sub_data.data.copy(deep=True)

        ell_b = np.matmul(self.bm, df["x"])
        Cl_b = np.matmul(self.bm, df["y"])
        var = df["yerr"]**2
        var_b = np.diag(np.matmul(self.bm, np.matmul(np.diag(var), self.bm.T)))
        d = {"ell": ell_b,
             "Cl": Cl_b,
             "Cl_err": np.sqrt(var_b)}
        df = pd.DataFrame(d)
        df.attrs={"dimensionless": 1.0}
        binned = CMBPowerSpectrum(df)
        binned.to_units(sub_data._original_units)
        return binned

    def planck_bin_weights_matrix(self):
        num_unbinned = self.lmax-self.lmin
        self.bm = np.zeros((len(self.bins), num_unbinned))
        for i,bin in enumerate(self.bins):
            offset = bin[0]-self.lmin
            ells_in_bin = np.arange(bin[0], bin[-1])
            bin_weight_norm = np.sum([l*(l+1) for l in ells_in_bin])
            for j,ell in enumerate(ells_in_bin):
                self.bm[i,offset+j] = ell*(ell+1)/bin_weight_norm

    def uniform_bin_weights_matrix(self):
        num_unbinned = self.lmax-self.lmin
        self.bm = np.zeros((len(self.bins), num_unbinned))
        for i,bin in enumerate(self.bins):
            offset = bin[0]-self.lmin
            ells_in_bin = np.arange(bin[0], bin[-1])
            bin_weight_norm = (bin[-1]-bin[0])
            for j,ell in enumerate(ells_in_bin):
                self.bm[i,offset+j] = 1.0/bin_weight_norm

