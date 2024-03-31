import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import numpy as np

def planck_axis_scale(ax, xlim, divide):
    ax.set_xscale('linear')
    ax.set_xlim([divide, xlim[-1]])
    ax.spines['left'].set_visible(False)
    ax.yaxis.set_ticks_position('right')
    #ax.yaxis.set_visible(False)

    divider = make_axes_locatable(ax)
    axLin = divider.append_axes("left", size=1.4, pad=0)
    axLin.set_xscale('log')
    axLin.set_xlim([xlim[0], divide])
    axLin.spines['right'].set_visible(False)
    axLin.yaxis.set_ticks_position('left')
    #plt.setp(axLin.get_xticklabels(), visible=True)

    return ax, axLin