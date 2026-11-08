import sys
from cold_frames import run
run('producer',0,50,'cold001',float(sys.argv[1]),int(sys.argv[2]))
