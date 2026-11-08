import json,time,sys
from pathlib import Path
from unary_to_unary_source_search_v2 import run
B=Path(__file__).resolve().parent
if __name__=='__main__':
    error=None
    try:run(2,float(sys.argv[1]))
    except BaseException as e:error=repr(e);raise
    finally:
        with (B/'audit_proof116_exit.json').open('x') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0},f)
