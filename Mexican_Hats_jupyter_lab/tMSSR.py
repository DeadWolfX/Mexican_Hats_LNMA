import numpy as np
import imageio
import sfMSSR as sf
from tqdm import tqdm 

def tMSSR(imgName, dimz, amp, psf, order, mesh, interp, tipe, nIter=1,method=None):

    """
    This function takes the image and parameters to apply Temporal MSSR, ie, in the full stack.

    Args:
    
         imgName (matrix): It is a matrix representing pixel values of the image.

         dimz (int): Number of frames contemplated for the z-stack

         psf (float): PSF (Point Spread Function) related to the image.

         amp (int): Amplification factor for the image.

         order (int): Order for MSSR.

         mesh (float): Value that define the cration of a mesh

         interp (string): Method used for interpolation in the image.
             -  bicubic
             - fourier

          Note: if the interp isn't definide by default use bicubic 

        tipe (string): A text string that designates the name of the hat:
          - laplacian: applies Laplacian processing.
          - meanshift: applies Mean Shift processing.
          - hessian: applies Hessian processing.
          - dog: applies Difference of Gaussians processing.
           Note: If this parameter is not defined, only a copy of the original image is used.

        nIter (int): Number of iterations when applying the chosen hat.

         method (string): Methods for vessel segmentation if are plicable.
          - Frangi
          - Sato

       
    Returns:
        GSSR matrix: It is a matrix representing pixel values of the image processed with Temporal MSSR.
    """    
    print("Starting Process")

    for j in tqdm(range(dimz)):
            
        Img = imgName[j,:,:].astype(float)
       
        if j==0:
            GSSR=np.zeros((dimz,sf.sfMSSR(x0=Img, amp=amp, psf=psf, order=order, mesh=mesh, interp=interp, tipe=tipe, nIter=nIter,method=method).shape[0],sf.sfMSSR(x0=Img, amp=amp, psf=psf, order=order, mesh=mesh,      
                                                                                                                                                                    interp=interp, tipe=tipe, nIter=nIter,method=method).shape[1]))
            GSSR[j, :,:] =sf.sfMSSR(x0=Img, amp=amp, psf=psf, order=order, mesh=mesh, interp=interp, tipe=tipe, nIter=nIter,method=method)
        else:
            GSSR[j, :,:] =sf.sfMSSR(x0=Img, amp=amp, psf=psf, order=order, mesh=mesh, interp=interp, tipe=tipe, nIter=nIter,method=method)
    
    return GSSR

