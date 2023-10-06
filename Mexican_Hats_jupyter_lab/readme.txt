To try this code only need to download the directory Mexican_Hats_jupyter_lab and open it in jupyter lab then visualise the file Example.ipynb and execute each cell in order.

The next files are examples to try the code:
  -SynEx2.tif  
  -ejemplo.tif 
  -raw7_100_DAMIAN_PSFCHECK_561_DONUTS_33MS_5POWERL.tif

The main code is analysis_image.py, which applies Temporal MSSR, specifically in the full stack using the Mexican hat of your choice. It needs to be executed with the following arguments:

Note: Some parameters are predefined to try the code in the jupyter lab such that you only change imgName,interp,tipe,method and dimz the code show you great results with the images examples. 

  - imgName (string): This is a string representing the path of the image.

  - amp (int): The amplification factor for the image.

  - psf (float): The PSF (Point Spread Function) related to the image.

  - order (int): The order for MSSR.

  - mesh (float): A value that defines the creation of a mesh.

  - interp (string): The method used for interpolation in the image. It could be:

    - bicubic
    - fourier
    Note: If the interp isn't defined, it will default to using bicubic.
  - tipe (string): A text string that designates the name of the hat. It could be:

    - laplacian: applies Laplacian processing.
    - meanshift: applies Mean Shift processing.
    - hessian: applies Hessian processing.
    - dog: applies Difference of Gaussians processing.
    Note: If this parameter is not defined, only a copy of the original image is used.
  
  - nIter (int): The number of iterations when applying the chosen hat.

  - dimz (int): The number of frames contemplated for the z-stack.

  - method (string): Enhancement method available for the Hessian process. It could be:

    - Frangi
    - Sato
The code returns a matrix representing pixel values of the image processed with Temporal MSSR and the chosen hat, along with its visualizations. 
