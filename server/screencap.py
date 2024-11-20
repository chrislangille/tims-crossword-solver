import subprocess
import os
import sys
from PIL import Image

width = 627
height = 1305 

def main():
    outfile = os.path.expanduser('assets/ss.png')
    outcmd = ['screencapture', outfile]

    try:
        # Run the command without shell=True for better security
        subprocess.check_output(outcmd)
        print("Screenshot captured successfully!")
    except subprocess.CalledProcessError as e:
        print(f'Python error: [{e.returncode}]\n{e.output.decode()}')


    image = Image.open(outfile)
    x = image.width - width
    y = 150 
    image = image.crop((x, y, x + width, y + height))
    image.save(outfile)

if __name__ == '__main__':
    sys.exit(main())


