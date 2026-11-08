import json,time,sys
from pathlib import Path
from nonlinear15_source_batches import build
B=Path(__file__).resolve().parent
if __name__=='__main__':
    error=None
    try:build(1,float(sys.argv[1]))
    except BaseException as e:error=repr(e);raise
    finally:
        with (B/'audit_proof51_exit.json').open('x') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0},f)
