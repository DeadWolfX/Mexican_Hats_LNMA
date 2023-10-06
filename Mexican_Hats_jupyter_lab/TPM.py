import numpy as np


def TPM(I):
    """
    This function takes the image to integrate the results of Temporal MSSR in one single image.

    Args:
    
         I (matrix): It is a matrix representing pixel values of the image.

    Returns:
        ITemp matrix: It is a matrix representing pixel values of the integrate image for Temporal MSSR.
    """        
    nz,nx,ny=I.shape
    ITemp = np.zeros((nx,ny))
    ITempSum = np.zeros((nx,ny))
    
    for i in range(nz):
        ITempSum =ITempSum+I[i, :,:]
    
    for i in range(nz):
        ITemp =ITemp+(I[i, :, :] * ITempSum)
    return ITemp




