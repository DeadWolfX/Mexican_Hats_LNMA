import numpy as np
from scipy.signal import convolve2d

def dog_core(I, psf, amp):

    """
    This function takes the image and parameters to apply difference of gaussians hat.

    Args:
    
         I (matrix): It is a matrix representing pixel values of the image.

         psf (float): PSF (Point Spread Function) related to the image.

         amp (int): Amplification factor for the image.
       
    Returns:
        img_DoG matrix: It is a matrix representing pixel values of the image processed with difference of gaussians hat.
    """
    sz = I.shape
    sigma = int(np.round(0.5 * psf * amp))
    lnG = 9
    x, y = np.meshgrid(np.arange(-lnG//2 + 1, lnG//2 + 1), np.arange(-lnG//2 + 1, lnG//2 + 1))
    G1 = np.exp(-(x**2 + y**2) / (2.0 * sigma**2))
    G1 = G1 / np.sum(G1)
    G2 = np.exp(-(x**2 + y**2) / (2.0 * (sigma * 0.625 / 10)**2))
    G2 = G2 / np.sum(G2)
    dog = G1 - G2

    img_DoG = np.pad(I, (lnG, lnG), mode='edge')
    img_DoG = -convolve2d(img_DoG, dog, mode='same')
    img_DoG = img_DoG[lnG:-lnG, lnG:-lnG]
    img_DoG[img_DoG < 0] = 0

    return img_DoG
