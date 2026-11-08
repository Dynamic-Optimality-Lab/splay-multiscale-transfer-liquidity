import runpy,sys
from pathlib import Path
sys.argv.extend(['proof269','1'])
runpy.run_path(str(Path(__file__).resolve().parents[2]/'SE03_STEP3_RECURSIVE_SOURCE_CLOSURE_35/CONTINUATION_04/search_FP_access_countercut.py'),run_name='__main__')
