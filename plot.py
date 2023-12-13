import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import StrMethodFormatter


class plotting: #Class to assist plotting of the results
    def __init__(self, xmin, xmax, ymin, ymax, steps, riv_coords = None):
        self.xmin=xmin
        self.ymin=ymin
        self.xmax=xmax
        self.ymax=ymax
        self.riv_coords=riv_coords
        self.steps=steps

    def mesh(self): #Method to create plot grid
        xvec = np.linspace(self.xmin, self.xmax, self.steps)
        yvec = np.linspace(self.ymin, self.ymax, self.steps)
        xvec, yvec = np.meshgrid(xvec, yvec)
        return xvec, yvec

    def fix_to_mesh(self, model): #Method to export results to the plot grid
        h1=[]
        psi1=[]
        for x,y in zip(self.mesh()[0].flatten(),self.mesh()[1].flatten()):
            head = model.calc_head(x, y)
            psi_0 = model.calc_psi(x, y)
            h1.append(head)
            psi1.append(psi_0)
        h = np.array(h1).reshape((self.steps, self.steps))
        psi = np.array(psi1).reshape((self.steps, self.steps))
        return h, psi

    #Method to create 2-D plot.....
    
    #Method to create 3-D plot
    def plot3d(self, model): #3D Plotting of the results
        fig, ax = plt.subplots(figsize=(15, 20), subplot_kw={'projection': "3d"})
        surf = ax.plot_surface(self.mesh()[0], self.mesh()[1], self.fix_to_mesh(model)[0], cmap=cm.coolwarm, linewidth=0, antialiased=True)
        ax.zaxis.set_major_formatter(StrMethodFormatter('{x:,.4f}'))  # Corrected format specifier
        ax.set_xlabel('Length of Domain (m)', fontsize=25, labelpad=25)  # Increase font size and labelpad
        ax.set_ylabel('Width of Domain (m)', fontsize=25, labelpad=28)  # Increase font size and labelpad
        ax.set_zlabel('Drawdown (m)', fontsize=25, labelpad=5)  # Increase font size and labelpad
        colorbar = fig.colorbar(surf, shrink=0.5, ax=ax, location="right")
        colorbar.ax.tick_params(labelsize=25)  # Set the font size for colorbar labels

        ax.set_zticks([])  # Hide the z-axis ticks

        ax.set_ylim(0, None)  # Modify here to show entire vicinity

        ax.tick_params(axis='x', labelsize=30)
        ax.tick_params(axis='y', labelsize=30)

        return ax, fig

