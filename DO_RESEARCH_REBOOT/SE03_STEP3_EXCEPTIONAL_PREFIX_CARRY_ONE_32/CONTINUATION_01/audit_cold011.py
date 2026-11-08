import sys
from cold_frames import run
run('producer',5327,5577,'cold011',float(sys.argv[1]),int(sys.argv[2]))
