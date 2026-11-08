import sys
from cold_frames import run
run('producer',50,650,'cold002',float(sys.argv[1]),int(sys.argv[2]))
