import runpy,sys
from pathlib import Path
sys.argv.append('proof249')
runpy.run_path(str(Path(__file__).resolve().parents[2]/'SE03_STEP3_RECURSIVE_SOURCE_CLOSURE_35/CONTINUATION_04/derive_zero_neutral_funding.py'),run_name='__main__')
