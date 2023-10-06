import numpy as np

def ms_core(I, psf, amp):

    """
    This function takes the image and parameters to apply Mean Shift hat.

    Args:
    
         I (matrix): It is a matrix representing pixel values of the image.

         psf (float): PSF (Point Spread Function) related to the image.

         amp (int): Amplification factor for the image.

       
    Returns:
        MS matrix: It is a matrix representing pixel values of the image processed with Mean Shift hat.
    """

    hs = int(np.round(0.5 * psf * amp))
    if hs < 1:
        hs = 1

    xPad = np.pad(I,(hs, hs), mode='symmetric')
    
    interval = np.arange(-hs, hs + 1)
    
    height, width= I.shape
    
    M = np.zeros((height,width),dtype=float)
    
    for i in interval:
        for j in interval:
            if (i != 0 or j != 0):
                xThis = xPad[hs + i:height + hs + i, hs + j:width + hs + j]
                M=np.maximum(M, np.abs(I - xThis))
                
    weightAccum = np.zeros((height,width), dtype=float)
    yAccum = np.zeros((height,width), dtype=float)
    
    
    for i in interval:
        for j in interval:
            if (i != 0 or j != 0):
                spatialKernel = np.exp(-(i ** 2 + j ** 2) / (hs ** 2))
                xThis = xPad[hs + i:height + hs + i, hs + j:width + hs + j]
                xDiffSq0 = ((I - xThis) / M) ** 2
                intensityKernel = np.exp(-1*xDiffSq0)
                weightThis = spatialKernel * intensityKernel
                weightAccum= weightAccum +weightThis
                yAccum= yAccum+(xThis * weightThis)

    MS = I - (yAccum / weightAccum)
    MS[MS < 0] = 0
    MS[np.isnan(MS)] = 0

    return MS
