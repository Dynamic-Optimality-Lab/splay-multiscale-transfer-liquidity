"""GSO conservative transport continuation: status or read-only verification."""
import sys
import json
import argparse
import subprocess
from pathlib import Path
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command',choices=('status','verify'),default='status',nargs='?')
    args=parser.parse_args()
    if args.command=='status':
        path=HERE/'ENGINE_RESULT.json'
        print(path.read_text(encoding='utf-8') if path.exists() else json.dumps({'engine':'WORKING_CONSERVATIVE_TRANSPORT_BACKEND','universal_CD':'OPEN'}));return
    for name in ('verify.py','verify_extended.py','packet_audit.py','tests.py','preserve.py'):
        subprocess.run([sys.executable,'-B',str(HERE/name)],cwd=str(HERE),check=True)
    subprocess.run(['lean','+leanprover/lean4:v4.21.0',str(HERE/'TransportKernel.lean')],cwd=str(HERE),check=True)
    if (HERE/'FINAL_MANIFEST.json').exists():
        subprocess.run([sys.executable,'-B',str(HERE/'seal.py'),'--verify'],cwd=str(HERE),check=True)


if __name__=='__main__':main()
