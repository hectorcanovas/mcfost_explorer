import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits

# Class that will be saved locally ==============
class Dust():
    def __init__(self, path = ''):
        self.path   = path
        self.angles = [inp for inp in np.arange(0,181)]


    def read_lambda(self):
        """
        Read lambdas used for dust/SED/Images computations
        """        
        hdu = fits.open(self.path + 'data_dust/lambda.fits.gz')
        self.lambdas = hdu[0].data
  

    def read_pol(self):
        """
        Read polarisability curve
        """        
        hdu = fits.open(self.path + 'data_dust/polarizability.fits.gz')
        self.polar = hdu[0].data


    def read_phase_f(self):
        """
        Read phase function
        """        
        hdu        = fits.open(self.path + 'data_dust/phase_function.fits.gz')
        self.phase = hdu[0].data

        
    def get_mcwave(self, inp_wave = 2.2):
        """
        Finds closes wavelengt to input [micrometers]
        """        
        els          = [np.abs(inp_lambda - inp_wave) for inp_lambda in self.lambdas]
        index        = np.where(els == np.min(els))[0][0]
        self.ilambda = self.lambdas[index]


    def plot_phase(self, fontsize = 16, figsize=[20,7], plt_show = True):
        if plt_show:
            fig = plt.figure(figsize=figsize)
        
        plt.plot(self.angles, np.log10(self.phase))
        plt.ylabel('Log10(Phase Function)', fontsize = fontsize)
        plt.xlabel('Scattering Angle',      fontsize = fontsize)
        plt.xticks(fontsize = fontsize)
        plt.yticks(fontsize = fontsize)
        if plt_show:
            plt.show()    

            
    def plot_polaris(self, fontsize = 16, figsize=[20,7], plt_show = True):
        if plt_show:
            fig = plt.figure(figsize=figsize)
        plt.plot(self.angles, self.polar)
        plt.ylabel('Polarizability',   fontsize = fontsize)
        plt.xlabel('Scattering Angle', fontsize = fontsize)
        plt.xticks(fontsize = fontsize)
        plt.yticks(fontsize = fontsize)
        plt.hlines(xmin=0,    xmax=180, y=0, linestyles=':')
        plt.vlines(ymin=-0.1, ymax=1.0, x=90, linestyles=':')
        if plt_show:
            plt.show()

    
    def plot_scat(self, fontsize = 16, figsize=[20,7], fig_name = None):
        fig = plt.figure(figsize=figsize)
        plt.subplot(121)        
        self.plot_phase(plt_show = False)
        plt.subplot(122)        
        self.plot_polaris(plt_show = False)
        plt.show()
        if fig_name:
            text = f'Figure saved as {fig_name}'
            print('='*len(text))
            print(text)
            print('='*len(text))
            fig.savefig(fig_name)
