import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits

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
        
        self.xdim, self.ydim = self.imgs[0].shape
        xc, yc = np.ceil((self.xdim - 1)/2), np.ceil((self.ydim - 1)/2)
        self.xc, self.yc = np.int(xc), np.int(yc)


        
    def get_pol_imgs(self):
        """
        Separate & Compute Polarised images
        """        
        self.I    = self.imgs[0]
        self.Q    = self.imgs[1]
        self.U    = self.imgs[2]
        self.P    = np.sqrt(self.Q**2 + self.U**2)
              
        # Obtain disc image in scattered light by removing central pixel (i.e. the star)
        Idisc        = self.imgs[0]
        Idisc[self.xc,self.yc] = 0
        self.Idisc   = Idisc

        
        
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
