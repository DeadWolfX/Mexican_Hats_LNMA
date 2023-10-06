import laplacian_core as lp
import  ms_core as ms
import hessian_core as hss
import dog_core as dog

def CoreAnalysisType(tipe, I, psf, amp, nIter,method):

    """
    This function takes the image and parameters to assign the type of hat to use.

    Args:
        tipe (string): A text string that designates the name of the hat:
          - laplacian: applies Laplacian processing.
          - meanshift: applies Mean Shift processing.
          - hessian: applies Hessian processing.
          - dog: applies Difference of Gaussians processing.
           Note: If this parameter is not defined, only a copy of the original image is used.

         I (matrix): It is a matrix representing pixel values of the image.

         psf (float): PSF (Point Spread Function) related to the image.

         amp (int): Amplification factor for the image.

         nIter (int): Number of iterations when applying the chosen hat.

         method (string): Methods for vessel segmentation:
          - Frangi
          - Sato
       
    Returns:
        CoreImage matrix: It is a matrix representing pixel values of the image processed with the desired hat.
    """


    
    if tipe.lower() == "laplacian":
        CoreImage = I.copy()
        for i in range(nIter):
            CoreImage = lp.laplacian_core(x0=CoreImage, psf=psf, amp=amp, twR=False)
    elif tipe.lower() == "meanshift":
        
        CoreImage = I.copy()
        for i in range(nIter):
            CoreImage = ms.ms_core(CoreImage, psf, amp)
    elif tipe.lower() == "hessian":
        CoreImage = I.copy()
        for i in range(nIter):
            CoreImage = hss.hessian_core(CoreImage, psf, amp,method)
    elif tipe.lower() == "dog":
        CoreImage = dog.dog_core(I, psf, amp)
    else:
        CoreImage = I.copy()
    
    return CoreImage
