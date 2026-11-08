import sys
from cold_frames import run
run('producer',0,5577,'cold012',float(sys.argv[1]),int(sys.argv[2]),True)
