import numpy as np
from scipy.signal import convolve2d
import math

def laplacian_core(x0, psf, amp, twR):
    """
    This function takes the image and parameters to apply Laplacian hat.

    Args:
    
         x0 (matrix): It is a matrix representing pixel values of the image.

         psf (float): PSF (Point Spread Function) related to the image.

         amp (int): Amplification factor for the image.

       
    Returns:
        img_laplacian matrix: It is a matrix representing pixel values of the image processed with Laplacian hat.
    """
    sigma = int(np.round(0.5 * psf * amp))
    
    if twR:
        img_laplacian = cMSLapI(x0, sigma, twR)
        img_laplacian[img_laplacian < 0] = 0
        img_laplacian = img_laplacian * (x0 ** 4)
    else:
        img_laplacian = cMSLapI(x0, sigma, twR)
        img_laplacian[img_laplacian < 0] = 0

    img_laplacian[np.isnan(img_laplacian)] = 0
    return img_laplacian

def cMSLapI(img, r, twR):
    """
    This function takes the image and parameters to calculate Laplacian multiscale.

    Args:
    
         img (matrix): It is a matrix representing pixel values of the image.

         r (float): Ratio parameter to calculate the Fourier radius.

       
    Returns:
        multiscaleLaplacian: It is a matrix representing the  Laplacian multiscale.
    """    
    img = np.fft.fft2(img)
    
    nx, ny = img.shape
    
    n = 60

    if twR:
        radius_fourier = 1.6227 / (0.0531 + r)
        radius_fourier2 = 0.4 * radius_fourier
        filt1 = Makefilter(nx, ny, n, radius_fourier, twR)
        filt2 = Makefilter(nx, ny, n, radius_fourier2, twR)
        filt = (filt1 * (1 - filt2))
    else:
        radius_fourier = 1.6227 / (0.0531 + r)
        filt = Makefilter(nx, ny, n, radius_fourier, twR) / (radius_fourier ** 2)
        
    ImageN = img * filt
    multiscaleLaplacian = np.fft.ifft2(ImageN).real

    return multiscaleLaplacian

def Makefilter(nx, ny, n, radius, twR):
    """
    This function takes the image parameters to create the filter used in the Laplacian multiscale.

    Args:
    
         nx (float): Height of the image,ie,number of rows in it matrix representation.

         ny (float): Width of the image,ie,number of colums in it matrix representation.

         n (int): order.

         r (float): Fourier radius

       
    Returns:
        filt matrix: It is a matrix representing the filter.
    """ 
    
    kxmax = 3.1416
    kymax = 3.1416
    
    
    step_x = 2 * kxmax / nx
    step_y = 2 * kymax / ny

    n=round((kxmax + step_x)/step_x)
    m=round((kymax + step_y)/step_y)    
    
    kx=np.zeros((n,))
    ky=np.zeros((m,))

    for i in range(n):
        kx[i]=i*step_x 

    for i in range(m):
        ky[i]=i*step_y 

   
    Kx, Ky = np.meshgrid(kx, ky)
    
    Kx=Kx.T
    Ky=Ky.T
    
    Kxyz = (Kx * Kx) + (Ky * Ky)
    c_nk = np.sqrt(2.0 * n + 1) / (np.sqrt(2) * radius * kxmax)
    nhx=math.floor(nx/2)+1
    nhy=math.floor(ny/2)+1
    flipx=nx%2
    flipy=ny%2
    filt = np.zeros((nx, ny))

    if twR:
        filt[0:nhx,0:nhy] = hdaf(n, c_nk, Kxyz)
    else:
        filt[0:nhx,0:nhy]=Kxyz * hdaf(n,c_nk,Kxyz) 
        
    submatrix = filt[nhx+1:nx, :]
    submatrix_reversed = submatrix[::-1, :]
    filt[nhx+1:nx, :] = submatrix_reversed
    
    filt[:, nhy:ny] = filt[:, nhy + flipy - 1:nhy + flipy - (ny - nhy) - 1:-1] 
        
   

    return filt 

def hdaf(n, c_nk, x):

    """
    This function takes the image parameters to create the filter based on Hermited Distributed Approximating Functional used in the Laplacian multiscale.

    Args:
    
         n (int): order.

         c_nk (float): Coefficient factor.

         x (matrix): Matrix representation of Laplacian.

       
    Returns:
        val matrix.
    """     
    x = x * (c_nk ** 2)
    fac=np.arange(n, -1, -1)
    fac=[ math.factorial(x) for x in fac]
    coefficients = 1.0 / np.array(fac)
    en = np.polyval(coefficients, x)
    val = en * np.exp(-x)
    return val
    

