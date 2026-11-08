import json,time
from pathlib import Path
from root_profile_quotient import build
B=Path(__file__).resolve().parent
if __name__=='__main__':
    error=None
    try:build('positive')
    except BaseException as e:error=repr(e);raise
    finally:
        with (B/'audit_proof64_exit.json').open('x') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0},f)
