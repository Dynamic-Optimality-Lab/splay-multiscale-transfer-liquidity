import runpy,sys
from pathlib import Path
sys.argv.extend(['proof225','1'])
runpy.run_path(str(Path(__file__).resolve().parents[2]/'SE03_STEP3_RECURSIVE_SOURCE_CLOSURE_35/CONTINUATION_04/search_real_leaf_profile_packets.py'),run_name='__main__')
