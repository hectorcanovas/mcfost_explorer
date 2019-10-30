import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits

# Class that will be saved locally ==============
class Dust():
    def __init__(self, path = ''):
        self.path   = path + 'data_dust/'
        self.angles = [inp for inp in np.arange(0,181)]


    def read_lambda(self):
        """
        Read wavelengths used for dust/SED/Images computations.
        """        
        hdu = fits.open(self.path + 'lambda.fits.gz')
        self.lambdas = hdu[0].data
  

    def read_pol(self):
        """
        Read polarisability curve.
        """        
        hdu = fits.open(self.path + 'polarizability.fits.gz')
        self.polar = hdu[0].data


    def read_phase_f(self):
        """
        Read phase function.
        """        
        hdu        = fits.open(self.path + 'phase_function.fits.gz')
        self.phase = hdu[0].data

        
    def read_all(self):
        self.read_lambda()
        self.read_phase_f()
        self.read_pol()


# Associated plotters ============================================================
    def make_canvas(self, xlabel = '', ylabel = '', fontsize = 16):
        plt.xlabel(xlabel, fontsize = fontsize)
        plt.ylabel(ylabel, fontsize = fontsize)
        plt.xticks(fontsize = fontsize)
        plt.yticks(fontsize = fontsize)


    def plot_phase(self, fontsize = 16, figsize=[10,7], plt_show = True):
        if plt_show:
            fig = plt.figure(figsize=figsize)
        
        self.make_canvas(xlabel = 'Scattering Angle', ylabel = r'$Log_{10}$(Phase Function)', fontsize = fontsize)
        plt.plot(self.angles, np.log10(self.phase))
        if plt_show:
            plt.show()    

            
    def plot_polaris(self, fontsize = 16, figsize=[10,7], plt_show = True):
        if plt_show:
            fig = plt.figure(figsize=figsize)
        plt.plot(self.angles, self.polar)
        self.make_canvas(xlabel = 'Scattering Angle', ylabel = 'Polarizability', fontsize = fontsize)
        plt.hlines(xmin=0,    xmax=180, y=0, linestyles=':')
        plt.vlines(ymin=-0.1, ymax=1.0, x=90, linestyles=':')
        if plt_show:
            plt.show()

    
    def plot_scat(self, fontsize = 20, figsize=[30,10], fig_name = None):
        fig = plt.figure(figsize=figsize)
        plt.subplot(121)        
        self.plot_phase(plt_show = False, fontsize = fontsize)
        plt.subplot(122)        
        self.plot_polaris(plt_show = False, fontsize = fontsize)
        plt.show()
        if fig_name:
            text = f'Figure saved as {fig_name}'
            print('='*len(text))
            print(text)
            print('='*len(text))
            fig.savefig(fig_name)
