import numpy as np
from astropy.wcs import WCS

import pylab as plt
import astropy.io.fits as fits
import os, re

from astropy.nddata import Cutout2D


def mk_hst_cutout(filename, pos, size, path = ''):
    '''Make a (`size`)-large cutout from a file (`filename`) at position (`pos`).
    '''
    
    hdus = fits.open(path+filename)
    wcs = WCS(hdus[1].header)
    img = hdus[1].data
    ny, nx = img.shape
    cut = Cutout2D(img, pos, (size[0], size[1]) , wcs = wcs)

    hdu = fits.PrimaryHDU(cut.data, cut.wcs.to_header())
    hdul = fits.HDUList([hdu])
    hdul.writeto(path+'cut'+filename, clobber=True)
    
    return cut