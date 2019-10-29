import numpy as np
import matplotlib.pyplot as plt
from astropy.io          import fits
from astropy.convolution import convolve
from astropy.convolution import Gaussian2DKernel

# Class that will be saved locally ==============
class ImgPol():
    def __init__(self, path = '', wave = '0.5'):
        self.path   = path
        self.wave   = wave

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
        self.I        = self.imgs[0]
        self.Q        = self.imgs[1]
        self.U        = self.imgs[2]
        self.mask     = np.zeros([self.xdim, self.ydim]) + 1
        self.mask[self.yc, self.xc] = 0
        self.Idisc    = self.I * self.mask # Disc in scattered light


    def make_pol(self):
        """
        Compute Polarised images
        """        
        self.P  = np.sqrt(self.Q**2 + self.U**2)
        np.seterr(divide='ignore', invalid='ignore') # To avoid Np complaining about division by zero
        self.dP = np.nan_to_num(self.P/self.Idisc, 0)


    def define_PSF(self, kernel = 5, user_defined = None):
        """
        Create PSF
        Note: a real PSF is more complex than a Gaussian.
        """        
        if user_defined:
            print('Loading user-given PSF')
        else:
            self.psf = Gaussian2DKernel(x_stddev=kernel, x_size = self.xdim, y_size = self.ydim)


    def convolve(self, kernel = 2):
        """
        Convolve images with PSF to emulate real observations
        """        
        self.I     = convolve(self.I,     self.psf)
        self.Q     = convolve(self.Q,     self.psf)
        self.U     = convolve(self.U,     self.psf)
        self.Idisc = convolve(self.Idisc, self.psf)
        self.make_pol()

        
    def plot_pol_imgs(self, figsize = [30,7], cmap = 'viridis'):
        """
        Separate & Compute Polarised images
        """        
        fig = plt.figure(figsize = figsize)
        i = 0
        for inp_img in [self.Idisc, self.Q, self.U, self.P]:
            i = i + 1
            plt.subplot(140 + i)
            plt.imshow(inp_img, cmap = cmap, origin = 'lower')
        plt.show()