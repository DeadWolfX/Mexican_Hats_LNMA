import tMSSR as tm
import TPM
import napari
import subprocess
import sys
import numpy as np
import matplotlib.pyplot as plt

def install_missing_packages(missing_requirements):
    try:
        for requirement in missing_requirements:
            subprocess.check_call(["pip", "install", requirement])
        
    except Exception as e:
        print(f"Error to install mising dependencies: {str(e)}")


def check_requirements():
    try:
        with open('requirements.txt') as f:
            requirements = f.read().splitlines()
            installed_requirements = [line.split('==')[0] for line in subprocess.check_output(["pip", "freeze"]).decode().split('\n') if line]
            missing_requirements = [requirement for requirement in requirements if requirement.split('==')[0] not in installed_requirements]
            
            if missing_requirements:
                install_missing_packages(missing_requirements)
    except Exception as e:
        print(f"Error to verify dependences: {str(e)}")


def main_analysis():
    img_path = str(sys.argv[1])
    amp = float(sys.argv[2])
    psf = float(sys.argv[3])
    order = int(sys.argv[4])
    mesh = float(sys.argv[5])
    interp =str(sys.argv[6])
    tipe = str(sys.argv[7])
    nIter = int(sys.argv[8])
    zstack=int(sys.argv[9])
    method=str(sys.argv[10])

    imgResult = tm.tMSSR(imgName=img_path, dimz=zstack, amp=amp, psf=psf, order=order, mesh=mesh, interp=interp, tipe=tipe, nIter=nIter,method=method)

    ITPMD = TPM.TPM(imgResult)
    IMEAND = np.mean(imgResult, axis=0)
    IVARD = np.var(imgResult, axis=0)

    viewer = napari.Viewer()

    viewer.add_image(imgResult, name='Process Image  Stak')
    viewer.add_image(ITPMD, name='TPMD Integrated Image')
    viewer.add_image(IMEAND, name='MEAN Integrated Image')
    viewer.add_image(IVARD, name='VARIANCE Integrated Image')
    napari.run()


if __name__ == "__main__":
    check_requirements()
    main_analysis()