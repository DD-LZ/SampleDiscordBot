#Made to re run discord bot if its throwing an exception and crashing

import time
import datetime
from datetime import datetime
from subprocess import Popen
import sys

filename = sys.argv[1]
while True:
    print("\n...CRASH DETECTED [" + str(datetime.now()) + "], RE-BOOTING " + filename)
    p = Popen("python3 " + filename, shell=True)
    p.wait()