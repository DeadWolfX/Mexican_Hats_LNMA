import numpy as np
from PIL import Image
import CoreAnalysisType as CAT


def sfMSSR(x0, amp, psf, order, mesh, interp, tipe, nIter=1,method=None):

    """
    This function takes the image and parameters to apply Singel Frame MSSR, ie, in one frane of the stack.

    Args:
    
         x0 (matrix): It is a matrix representing pixel values of the image.

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
        IMSSR matrix: It is a matrix representing pixel values of the image processed with Single Frame MSSR.
    """
    
    x1 = x0.astype(float)
    sz = x1.shape
    Exedge = 1
     
    if amp > 1:
        if interp.lower() != "bicubic" and interp.lower() != "fourier":
            print('The interpolation parameter should be bicubic or Fourier, but as there is no match, bicubic will be used.')
            interp='bicubic'
        if interp.lower() == "bicubic":
            new_height = int(sz[0] * amp)
            new_width = int(sz[1] * amp)
            AMP = np.array(Image.fromarray(x1).resize((new_width, new_height), Image.BICUBIC))
            
        else:
            if interp.lower() == "fourier":
                AMP = FourierMag(x1, amp)
            
        if mesh == 1:
            
            AMP = compGrid(AMP, np.ceil(amp/2), 1)
    else:
        AMP = x1
    
    MS = CAT.CoreAnalysisType(tipe=tipe, I=AMP, psf=psf, amp=amp, nIter=nIter,method=method)
    
    
    
    I3 = MS / np.max(MS)
    
    x3 = AMP / np.max(AMP)

    for i in range(order):
        I4 = x3 - I3  # Diff
        I5 = np.max(I4) - I4  # Diff complement
        I5 = I5 / np.max(I5)  # Normalization
        I6 = I5 * I3  # Intensity weighting
        I7 = I6 / np.max(I6)  # Final normalization
        x3 = I3
        I3 = I7

    I3[np.isnan(I3)] = 0
    I3[I3 < 0] = 0
    IMSSR = I3 * np.max(x1)  # Importante

    outliers = False

    if outliers:
        th = 0.97
        f, x = ecdf(AMP.flatten())
        mnX = np.min(x[f > th])
        AMP[AMP >= mnX] = mnX

        f, x = ecdf(IMSSR.flatten())
        mnX = np.min(x[f > th])
        IMSSR[IMSSR >= mnX] = mnX

    IMSSR = IMSSR * AMP

    return IMSSR

def compGrid(img, desp, prp):
    """
    This function takes the image and parameters to compute a Grid.

    Args:
    
         img (matrix): It is a matrix representing pixel values of the image.

         desp (int): Value to generate padding into the image.

         prp (int): Factor of proporion.

    Returns:
        imgHVC matrix: It is a matrix representing pixel values of the processed image.
    """
    height, width = img.shape
    desp=int(desp)
    imgPad = np.pad(img, [(desp, desp), (desp, desp)], mode='symmetric')
    imgVI = imgPad[(1 + desp):(height + desp)+1, 1:width+1]
    imgVD = imgPad[(1 + desp):(height + desp)+1, (2 * desp ):(2 * desp + width)]
    imgHI = imgPad[0:(height), (desp):(width + desp)]
    imgHD = imgPad[(2 * desp ):(2 * desp + height), (desp):(width + desp)]
    imgHVC = (img + prp * (imgHD + imgHI + imgVD + imgVI)) / (1 + (4 * prp))
    
    return imgHVC

def FourierMag(Img, mg):

    """
    This function takes the image and magnification to compute a Fourier Magnification.

    Args:
    
         Img (matrix): It is a matrix representing pixel values of the image.

         mg (int): Factor of magnification.


    Returns:
        iFM matrix: It is a matrix representing pixel values of the processed image.
    """
   
    img = np.fft.fft2(Img)
    szx , szy = img.shape
    mdX = int(np.ceil(szx / 2))
    mdY = int(np.ceil(szy / 2))
    szFx=szx*mg
    szFy=szy*mg
    fM = np.zeros((szFx,szFy),dtype=complex)
    lnX=np.abs(mdX-szx)
    lnY =np.abs(mdY-szy)
    img=mg*mg*img
    fM[0:mdX,0:mdY] =img[0:mdX, 0:mdY]  # izq sup cuadrante
    fM[0:mdX, (szFy-lnY):szFy] =img[0:mdX, mdY:szy]  # der sup cuadrante
    fM[(szFx - lnX):szFx, 0:mdY] =img[mdX:szx, 0:mdY]  # izq inf cuadrante
    fM[(szFx - lnX):szFx, (szFy-lnY):szFy] =img[mdX:szx, mdY:szy]# der inf cuadrante
    iFM = np.fft.ifft2(fM).real
    return iFM

