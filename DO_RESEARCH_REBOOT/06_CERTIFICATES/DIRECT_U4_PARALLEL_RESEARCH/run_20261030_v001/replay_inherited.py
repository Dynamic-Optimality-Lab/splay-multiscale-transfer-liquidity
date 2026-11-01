"""Run existing independent verifiers with result writes redirected to this run.

Inputs, source compilers, solver contracts and old artifacts remain read-only.
No original script is modified. CHR uses its read-only main; FRC only its OUT is set.
"""
from pathlib import Path
import sys, importlib.util, contextlib, argparse
OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[3]

def main():
    parser=argparse.ArgumentParser();parser.add_argument('which',choices=('chr','frc','m2'))
    which=parser.parse_args().which
    if which=='chr':
        folder=ROOT/'DO_RESEARCH_REBOOT/M3_CHR01';name='verify_fragment.py'
    elif which=='frc':
        folder=ROOT/'DO_RESEARCH_REBOOT/M3_FRC01';name='audit_results.py'
    else:
        folder=ROOT/'DO_RESEARCH_REBOOT/M2_DSK01';name='audit_certificate.py'
    sys.path.insert(0,str(folder))
    spec=importlib.util.spec_from_file_location('u4_inherited_replay',folder/name)
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    if which=='frc':mod.OUT=OUT/'frc_independent_replay.json'
    # main() reads arguments only for the CHR verifier; it receives no --save.
    sys.argv=[str(folder/name)]
    with (OUT/(which+'_independent_replay.log')).open('x',encoding='utf-8') as stream:
        with contextlib.redirect_stdout(stream):mod.main()
    print((OUT/(which+'_independent_replay.log')).read_text())

if __name__=='__main__':main()
