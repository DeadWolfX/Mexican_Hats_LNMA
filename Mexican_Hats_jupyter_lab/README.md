<p>To try this code only need to download the directory Mexican_Hats_jupyter_lab and open it in jupyter lab then visualise the file Example.ipynb and execute each cell in order.<br><br>

The next files are examples to try the code:</p>
<ul>
  <li><p>SynEx2.tif</p></li>  
  <li><p>ejemplo.tif</p></li> 
  <li><p>raw7_100_DAMIAN_PSFCHECK_561_DONUTS_33MS_5POWERL.tif</p></li>
</ul>

<p>The main code is analysis_image.py, which applies Temporal MSSR, specifically in the full stack using the Mexican hat of your choice. It needs to be executed with the following arguments:<p>

<p><b>Note:</b> Some parameters are predefined to try the code in the jupyter lab such that you only change imgName,interp,tipe,method and dimz the code show you great results with the images examples. </p>

 <ul>
  <li><b>imgName</b>(string):</li> This is a string representing the path of the image.
  <li><b>amp</b>(int):</li> The amplification factor for the image.
  <li><b>psf</b>(float):</li> The PSF (Point Spread Function) related to the image.
  <li><b>order</b>(int):</li> The order for MSSR.
  <li><b>mesh</b>(float):</li> A value that defines the creation of a mesh.
  <li><b>interp</b>(string):</li> The method used for interpolation in the image. It could be:
    <ul>
    <li><b>bicubic</b></li>
    <li><b>fourier</b></li><br>
    <b>Note:</b> If the interp isn't defined, it will default to using bicubic.
    </ul>  
  <li><b>type</b>(string):</li> A text string that designates the name of the hat. It could be:
    <ul>
     <li><b>laplacian:</b></li> applies Laplacian processing.
    <li><b>meanshift:</b></li> applies Mean Shift processing.
    <li><b>hessian:</b></li> applies Hessian processing.
    <li><b>dog:</b></li> applies Difference of Gaussians processing.<br>
    <b>Note:</b> If this parameter is not defined, only a copy of the original image is used.
    </ul>
  <li><b>nIter</b>(int):</li> The number of iterations when applying the chosen hat.
  <li><b>dimz</b>(int):</li> The number of frames contemplated for the z-stack.
  <li><b>method</b>(string):</li> Enhancement method available for the Hessian process. It could be:
   <ul>
    <li><b>Frangi</b></li>
    <li><b>Sato</b></li>
    </ul> 
</ul>

<p>The code returns a matrix representing pixel values of the image processed with Temporal MSSR and the chosen hat, along with its visualizations. </p>
