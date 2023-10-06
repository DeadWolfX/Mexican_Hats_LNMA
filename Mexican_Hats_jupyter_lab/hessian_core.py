import numpy as np
from scipy.ndimage import gaussian_filter
from scipy.signal import convolve2d

def hessian_core(x0, psf, amp, method):
    
    """
    This function takes the image and parameters to apply Hessian hat.

    Args:
    
         x0 (matrix): It is a matrix representing pixel values of the image.

         psf (float): PSF (Point Spread Function) related to the image.

         amp (int): Amplification factor for the image.

         method (string): Methods for vessel segmentation:
          - Frangi
          - Sato
       
    Returns:
       img_hessian matrix: It is a matrix representing pixel values of the image processed with Hessian hat.
    """
    
    sigma = 0.25 * psf * amp
    Dxx, Dxy, Dyy = Hessian2D(x0, sigma)
    Dxx *= sigma ** 2
    Dxy *= sigma ** 2
    Dyy *= sigma ** 2

    Lambda1, Lambda2, Ix, Iy = eig2image(Dxx, Dxy, Dyy, method)
    img_hessian_norm = np.sqrt(Lambda1 ** 2 + Lambda2 ** 2)
    eigs = Lambda1 * Lambda2
    img_hessian = img_hessian_norm * eigs
    I = np.logical_and(Lambda1 < 0, Lambda2 < 0)
    img_hessian[~I] = 0
    img_hessian[np.isnan(img_hessian)] = 0

    return img_hessian

def Hessian2D(I, Sigma):

    """
    This function takes the image and parameters to calculate the Gaussian filters and calculate the Hessian for a 2D imagen.

    Args:
    
         I (matrix): It is a matrix representing pixel values of the image.

         sigma (float): Standard deviation for the Gaussian kernel generation.
       
    Returns:
        Dxx, Dxy, Dyy matrices: Matrices that represent the Hessian .
    """
    
    pad_size = int(round(3 * Sigma))

    I = np.pad(I,(pad_size, pad_size), mode='edge')
    X, Y = np.meshgrid(np.arange(-pad_size, pad_size + 1), np.arange(-pad_size, pad_size + 1))

    DGaussxx = (1 / (2 * np.pi * Sigma ** 4)) * (X ** 2 / Sigma ** 2 - 1) * np.exp(-(X ** 2 + Y ** 2) / (2 * Sigma ** 2))
    DGaussxy = (1 / (2 * np.pi * Sigma ** 6)) * (X * Y) * np.exp(-(X ** 2 + Y ** 2) / (2 * Sigma ** 2))
    DGaussyy = DGaussxx.T

    Dxx = convolve2d(I, DGaussxx, mode='valid')
    Dxy = convolve2d(I, DGaussxy, mode='valid')
    Dyy = convolve2d(I, DGaussyy, mode='valid')

    return Dxx, Dxy, Dyy

def eig2image(Dxx, Dxy, Dyy, method):

    """
    This function takes the Hessian matrices to calculate the eigenvalues and diagonal matrices for the image.

    Args:
    
         Dxx,Dxy,Dyy (matrices): Matrices for the Hessian.

         method (string): Methods for vessel segmentation:
          - Frangi
          - Sato
       
    Returns:
        Lambda1, Lambda2 floats: Eigenvalues.
        Ix, Iy : Diagonal matroces.
    """
    tmp = np.sqrt((Dxx - Dyy) ** 2 + 4 * Dxy ** 2)
    v2x = 2 * Dxy
    v2y = Dyy - Dxx + tmp

    mag = np.sqrt(v2x ** 2 + v2y ** 2)
    i = (mag != 0)
    v2x[i] /= mag[i]
    v2y[i] /= mag[i]

    v1x = -v2y
    v1y = v2x

    mu1 = 0.5 * (Dxx + Dyy + tmp)
    mu2 = 0.5 * (Dxx + Dyy - tmp)
    
    if method != 'Frangi' and method != 'Sato':
        print('The method parameter should be Frangi or Sato, but as there is no match, Frangi is used.')
        method='Frangi'
        
    if method == 'Frangi':
        check = np.abs(mu1) > np.abs(mu2)
    elif method == 'Sato':
        check = mu1 > mu2

    Lambda1 = mu1.copy()
    Lambda2 = mu2.copy()
    Lambda1[check] = mu2[check]
    Lambda2[check] = mu1[check]
    Ix = v1x.copy()
    Ix[check] = v2x[check]
    Iy = v1y.copy()
    Iy[check] = v2y[check]

    return Lambda1, Lambda2, Ix, Iy
