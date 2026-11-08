"""Run the preserved integrity checks with native long-path filesystem access."""
import importlib.util
import os
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode=True
RAW_HERE=Path(__file__).resolve().parent
RAW_ROOT=RAW_HERE.parents[3]
spec=importlib.util.spec_from_file_location('cyclic_review_preserved_sealer',RAW_HERE/'seal_delivery.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)


def native(p):
    raw=str(p)
    return Path('\\\\?\\'+raw) if os.name=='nt' and not raw.startswith('\\\\?\\') else p


def git(*args):
    return subprocess.check_output(['git','--no-optional-locks',*args],cwd=RAW_ROOT,text=True).strip()


if __name__=='__main__':
    m.HERE=native(RAW_HERE)
    m.ROOT=native(RAW_ROOT)
    m.BASE=m.HERE.parent
    m.STAGE=m.ROOT/'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE'
    m.git=git
    m.main()
