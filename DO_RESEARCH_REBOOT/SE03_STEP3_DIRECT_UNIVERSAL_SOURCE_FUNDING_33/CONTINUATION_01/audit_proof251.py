import runpy,sys
from pathlib import Path
sys.argv.append('proof251')
runpy.run_path(str(Path(__file__).resolve().parents[2]/'SE03_STEP3_RECURSIVE_SOURCE_CLOSURE_35/CONTINUATION_04/probe_joint_source_relation.py'),run_name='__main__')
