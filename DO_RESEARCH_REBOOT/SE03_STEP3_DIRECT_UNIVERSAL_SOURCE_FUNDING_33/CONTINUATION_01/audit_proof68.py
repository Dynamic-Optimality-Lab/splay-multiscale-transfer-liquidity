import json,time
from pathlib import Path
from clipped_deficit_quotient import build
B=Path(__file__).resolve().parent
if __name__=='__main__':
    error=None
    try:build(1)
    except BaseException as e:error=repr(e);raise
    finally:
        with (B/'audit_proof68_exit.json').open('x') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0},f)
