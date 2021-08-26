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
    hdul.writeto(path+'cut_'+filename, clobber=True)
    
    return cut

def mk_hsc_cutout(filenames, pos=None, size=None, path = '', patch = True):
    '''Make a (`size`)-large cutout from a file (`filename`) at position (`pos`).
    '''
    cube = []
    if path == False:
        assert pos is not None and size is not None
    for f in filenames:
        hdus = fits.open(path+f)
        wcs = WCS(hdus[1].header)
        img = hdus[1].data
        ny, nx = img.shape
        if patch == True:
            if size is None:
                n = np.min([nx,ny])
            else:
                n = size
            if pos is None:
                pos = np.array([nx/2, ny/2]).astype(int)
        else:
            #TODO: implement wcs extraction
            pass
        print(n)
        cut = Cutout2D(img, pos, (n,n) , wcs = wcs)
        cube.append(cut.data)

    hdu = fits.PrimaryHDU(np.array(cube), cut.wcs.to_header())
    hdul = fits.HDUList([hdu])
    hdul.writeto(path+'cube_HSC_'+f, clobber=True)
    
    return cube


def mk_psf_cube(filenames, path = ''):
    '''Make a psf cube out of several files.
    '''
    cube = []

    for f in filenames:
        hdus = fits.open(path+f)
        wcs = WCS(hdus[0].header)
        img = hdus[0].data

        cube.append(img)

    hdu = fits.PrimaryHDU(np.array(cube), cut.wcs.to_header())
    hdul = fits.HDUList([hdu])
    hdul.writeto(path+'cube_HSC_'+f, clobber=True)
    
    return cube
