import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.colorbar import colorbar
from mpl_toolkits.axes_grid1.axes_divider import make_axes_locatable
import matplotlib.ticker as ticker
from astropy.io          import fits
from astropy.convolution import convolve
from astropy.convolution import Gaussian2DKernel

# Class that will be saved locally ==============
class ImgPol():
    def __init__(self, path = '', wave = '0.5'):
        self.path   = path
        self.wave   = wave
        self.labels = ['I', 'Q', 'U', 'Idisc']        

    def read_fitscube(self):
        """
        Read MCFOTS output images
        """        
        hdu = fits.open(self.path + f'data_{self.wave}/RT.fits.gz')
        self.head = hdu[0].header
        self.imgs = hdu[0].data[:,0,0,:,:] # Not sure why the array has 5 dimensions.

        
    def get_dims(self):
        """
        Define image dimensions.
        """        
        self.xdim, self.ydim = self.imgs[0].shape  # Image pixel size [arc-secs]
        self.pixscl = self.head['CDELT2']*3600
        self.xc     = int((self.xdim - 1)/2)
        self.yc     = int((self.ydim - 1)/2)
        self.xsz_as = self.xdim * self.pixscl # Image size  [arc-secs]

        
    def get_imgs(self):
        """
        Read & label Stokes-Parameter images
        """
        for i in range(3):
            self.__setattr__(self.labels[i], self.imgs[i])
        
        # Disc in scattered light ===
        self.mask     = np.zeros([self.xdim, self.ydim]) + 1
        self.mask[self.yc, self.xc] = 0
        self.__setattr__(self.labels[3], self.imgs[0] * self.mask)


    def make_PSF(self, gauss_kernel = 5, input_psf = None):
        """
        Create PSF
        Note: a real PSF is more complex than a Gaussian.
        """        
        if input_psf:
            print('Loading user-given PSF')
        else:
            self.psf = Gaussian2DKernel(x_stddev=gauss_kernel, x_size = self.xdim, y_size = self.ydim)


    def convolve(self):
        """
        Convolve images with PSF to emulate real observations
        """        
        for label in self.labels:
            self.__setattr__(label, convolve(self.__getattribute__(label), self.psf))
        self.make_pol()


    def add_noise(self, SN = 5, noise_std = 1.0):
        """
        Add randomn noise to mimic real observations
        """        
        noise    = np.random.normal(1.0,noise_std,(self.xdim, self.ydim))               # Noise Array
        noise    = noise/np.max(noise) * np.max(np.sqrt(self.Q**2 + self.U**2)) * 1/SN  # Scale it to P 
        for inp in self.labels:
            self.__setattr__(inp, self.__getattribute__(inp) + noise)


    def make_pol(self):
        """
        Compute Polarised images
        """        
        self.P  = np.sqrt(self.Q**2 + self.U**2)
        np.seterr(divide='ignore', invalid='ignore') # To avoid Np complaining about division by zero
        self.dP = np.nan_to_num(self.P/self.Idisc, 0)
        self.labels_pol = ['P', 'dP']    # Here I store derived (not directly observed) quantities


        
    def plot_pol_imgs(self, figsize = [30,7], fontsize = 18, bbox={'facecolor':'white', 'alpha':1.0, 'pad':7}):
        """
        Separate & Compute Polarised images
        """        
        fig    = plt.figure(figsize = figsize)
        cmaps  = ['viridis', 'RdYlGn'  , 'RdYlGn'  , 'viridis']
        tlabel = [r'$I_{disc}$', 'Stokes Q', 'Stokes U', r'$P_I$']
        i      = 0
        for inp_img in [self.Idisc, self.Q, self.U, self.P]:
            ax  = plt.subplot(141 + i)
            img = plt.imshow(inp_img, cmap = cmaps[i], origin = 'lower')
            plt.subplots_adjust(wspace = 0.0, hspace = 0)
            plt.axis('off')
            ax.text(self.xdim * 0.1, self.ydim*0.9, tlabel[i], fontsize = fontsize, bbox=bbox) # label
            self.make_colorbar(ax, img, fontsize)
            i = i + 1
        plt.show()


    def make_colorbar(self, axis_obj, img, fontsize = 18):
                    #   Set Color Bar ================
            ax_divider = make_axes_locatable(axis_obj)
            cax        = ax_divider.append_axes("top", size="7%", pad="4.5%", aspect=0.075)
            cb         = plt.colorbar(img, cax=cax, orientation="horizontal")
            cb.ax.xaxis.set_label_position('top')
            cb.locator = ticker.MaxNLocator(nbins=5) #To controll the amount of ticks in Color Table
            cb.update_ticks()

            cb.ax.tick_params(labelsize = fontsize*0.8, top = True, bottom = False, labeltop = True, labelbottom = False)
            cb.ax.set_xlabel(self.head['BUNIT'], fontsize = fontsize*0.8)
