import json,sys,time
from pathlib import Path
from full_geometry_sparse_solver import run
B=Path(__file__).resolve().parent
if __name__=='__main__':
    error=None
    try:run(4,float(sys.argv[1]))
    except BaseException as e:error=repr(e);raise
    finally:
        with (B/'audit_proof147_exit.json').open('x') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0},f)