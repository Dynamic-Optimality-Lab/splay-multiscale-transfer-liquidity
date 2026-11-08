"""Launch C34 through the unchanged cumulative accepted controller."""
import runpy
from pathlib import Path
runpy.run_path(str(Path(__file__).resolve().parents[2]/'SE03_STEP3_GLOBAL_JOINT_OWNERSHIP_34/produce_pools.py'),run_name='__main__')
