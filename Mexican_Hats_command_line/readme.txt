In the main directory of the code, Mexican_Hats, there exists a requirements.txt file that contains 
the necessary packages and their versions for this code. You can install them manually or let the code 
itself verify and install the required packages.

The next files are examples to try the code:
  -SynEx2.tif  
  -ejemplo.tif 
  -raw7_100_DAMIAN_PSFCHECK_561_DONUTS_33MS_5POWERL.tif

The main code is analysis_image.py, which applies Temporal MSSR, specifically in the full stack using the Mexican hat of your choice. It needs to be executed with the following arguments:

  - imgName (string): This is a string representing the path of the image.

  - amp (int): The amplification factor for the image.

  - psf (float): The PSF (Point Spread Function) related to the image.

  - order (int): The order for MSSR.

  - mesh (float): A value that defines the creation of a mesh.

  - interp (string): The method used for interpolation in the image. It could be:

    - bicubic
    - fourier
    Note: If the interp isn't defined, it will default to using bicubic.
  - type (string): A text string that designates the name of the hat. It could be:

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

For example, to run the code with the parameters:

imgName = "path/image_name.tif"
amp = 5
psf = 3
order = 1
mesh = 1
interp = "bicubic"
type = "laplacian"
nIter = 1
dimz = 100
method = 'Frangi'

If you are excecuting the code outside the Mexican_Hats_command_line  directory you need to execute:

python3 /path/analysis_image.py path/image_name.tif 5 3 1 1 bicubic laplacian 1 100 Frangi

If you are excecuting the code inside the Mexican_Hats_command_line  directory you need to execute:

python3 analysis_image.py image_name.tif 5 3 1 1 bicubic laplacian 1 100 Frangi
