import subprocess
import os
import sys


def main():
    outfile = os.path.expanduser('captured.png')
    outcmd = "{} {}".format('screencapture', outfile)

    try:
        # ordinarily we would not use shell=True due to security concerns
        subprocess.check_output([outcmd], shell=True)
    except subprocess.CalledProcessError as e:
        print('Python error: [%d]\n{}\n'.format(e.returncode, e.output))


if __name__ == '__main__':
    sys.exit(main())

