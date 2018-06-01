#!/usr/bin/python3

import os
import subprocess

# Bootstrap for GUI, make sure whole script run as root
#
# GUI imports woeusb as module and I couldn't find way to elevate scripts permissions during execution,
# so we just use this as bootstrap for rest of application

# Don't work, give error:
# Unable to access the X Display, is $DISPLAY set properly?
if os.getuid() != 0:
    subprocess.run(["pkexec", "python", os.path.abspath("gui.py")])
else:
    subprocess.run(["./gui.py"])
