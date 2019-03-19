#import numpy as np
#import matplotlib.pyplot as py
import subprocess as sh


raw = sh.check_output("minimu9-ahrs --mode raw | head -n1", shell=True)

print (raw)
