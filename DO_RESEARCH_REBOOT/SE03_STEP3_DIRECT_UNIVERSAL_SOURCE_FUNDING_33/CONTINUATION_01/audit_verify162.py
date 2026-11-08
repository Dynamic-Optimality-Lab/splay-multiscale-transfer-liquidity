import json
import runpy
import time
from pathlib import Path
B = Path(__file__).resolve().parent
F = B.parent.parent / 'SE03_STEP3_RECURSIVE_SOURCE_CLOSURE_35/UNIVERSAL_GLOBAL_FUNDING_11'
error = None
try:
    runpy.run_path(str(F / 'audit_existing_compensation.py'), run_name='__main__')
except BaseException as exc:
    error = repr(exc)
    raise
finally:
    with (B / 'audit_verify162_exit.json').open('x', encoding='utf8') as f:
        json.dump(dict(whole_process_CPU_seconds=time.process_time(), error=error,
                       source_queries=0, source_engine_calls=0), f)
