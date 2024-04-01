# cosmo_data_tools
This package makes it easier to find, download, and manipulate cosmological data products for plotting purposes.

## Installation

This package is not registered so cannot be downloaded using a package manager. However, you can install using
```
  git clone git@github.com:gplynch619/cosmo_data_tools.git
  cd cosmo_data_tools
  pip install .
```

## Why is this useful?

Data products from major cosmological experiments, such as Planck, SPT, etc., are available online but in disparate locations and formats. This makes it inconvenient to compile these data for plotting purposes and creates an overhead for making simple plots comparing data to model predictions. `cosmo_data_tools` streamlines this process by downloading these data upon request and converting to a consistent format across datasets. For example, to compare the Planck 2018 and SPT-3G TT powerspectra, you can simply run
```python
import matplotlib.pyplot as plt
from cosmo_data_tools.cmb.planck_2018_TTTEEE import planck_2018_TT
from cosmo_data_tools.cmb.spt3g_2018_TTTEEE import spt3g_2018_TT

planck = planck_2018_TT()
spt = spt3g_2018_TT()

fig,ax=plt.subplots()
ax.errorbar(planck.ell(), planck.Dl(), yerr=planck.Dl_err())
ax.errorbar(spt.ell(), spt.Dl(), yerr=spt.Dl_err())

plt.show()

```
The first time `cosmo_data_tools` is asked to plot a specific data set, it will download it from official sources and store for later use. There is more functionality as well detailed in `examples.ipynb`. 
