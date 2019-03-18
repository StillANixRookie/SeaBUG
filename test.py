import numpy as np
import matplotlib.pyplot as py
import subprocess as sh


raw = sh.check_output("bash dummyimu.sh | head -1", shell=True)

print (raw)
