import numpy as np
from astropy.wcs import WCS
import scarlet
import sep 

import pylab as plt
import astropy.io.fits as fits
import os, re

from astropy.nddata import Cutout2D


def mk_hst_cutout(filename, pos, size, ind=0, path = ''):
    '''Make a (`size`)-large cutout from a file (`filename`) at position (`pos`).
    '''
    
    hdus = fits.open(path+filename)
    wcs = WCS(hdus[ind].header)
    img = hdus[ind].data
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
    '''Make a (`size`)-large cutout from a file (`filename`) at position (`pos`).
    '''
    cube = []

    for f in filenames:
        hdus = fits.open(path+f)
        img = hdus[0].data
        ny, nx = img.shape
        n = np.min([nx,ny])
        pos = (int(nx/2), int(ny/2))
        cut = Cutout2D(img, pos, (n,n))
        cube.append(cut.data)

    hdu = fits.PrimaryHDU(np.array(cube))
    hdul = fits.HDUList([hdu])
    hdul.writeto(path+'cube_HSC_'+f, clobber=True)
    
    return cube


def get_hst_psf(filename, pos, size = 51, path = ''):
    
    hdus = fits.open(path+filename)
    img = hdus[0].data.byteswap().newbyteorder()
    
    star = Cutout2D(img, pos, (size, size)).data
    
    star = np.asarray(star, order='C')
    bkg = sep.Background(star)
    catalog = sep.extract(star, 3, err=bkg.globalrms)
    
    x, y = catalog['x'], catalog['y']
    while int(x)%2 == 0:
        x+=1
    while int(y)%2 == 0:
        y+=1
        
    plt.imshow(np.sqrt(star))
    plt.plot(x, y, 'x')
    plt.show()
    
    shift = (-x+int(size/2), -y+int(size/2))
    print(x, y, shift)
    
    psf = scarlet.fft.shift(star, shift, return_Fourier=False)
    
    plt.imshow(np.sqrt(psf))
    plt.show()
    hdu = fits.PrimaryHDU(star)
    hdul = fits.HDUList([hdu])
    hdul.writeto(path+'PSF_hst_'+filename, clobber=True)
    
    return psf




