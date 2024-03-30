import numpy as np
import pandas as pd
from scipy.interpolate import CubicSpline

class CosmoData():

    def __init__(self, x,y, xerr=None, yerr=None):
        d = {"x": x,
             "y": y}
        if xerr is not None:
            d.update({"xerr": xerr})
        elif yerr is not None:
            d.update({"yerr": yerr})
        
        self.data = pd.DataFrame(d)
        self.xmin = self.data["x"].min()
        self.xmax = self.data["x"].max()

    def get_x(self):
        return self.data["x"]
    
    def get_y(self, x=None):
        if x is None:
            return self.data["y"]
        else:
            if x.min()<self.xmin or x.max()>self.xmax:
                raise IndexError("Requested value was outside of interpolation range")
            else:
                return CubicSpline(self.data["x"], self.data["y"])(x)
    
    def get_yerr(self):
        if "yerr" in self.data.columns:
            return self.data["yerr"]
        else:
            return np.zeros(len(self.data["y"]))