from pathlib import Path
import sys,json,time,atexit,hashlib
ROOT=Path(__file__).resolve().parent
C1=ROOT.parent/'CONTINUATION_01_COVERAGE_PROOF'
PARENT=ROOT.parent
REPO=ROOT.parents[2]
sys.path.insert(0,str(C1))
import core as inherited
from core import *
ROOT=Path(__file__).resolve().parent
C1=ROOT.parent/'CONTINUATION_01_COVERAGE_PROOF'
PARENT=ROOT.parent;REPO=ROOT.parents[2]
inherited.ROOT=ROOT;inherited.frozen.ROOT=ROOT;inherited.frozen.prior.ROOT=ROOT
inherited.inherited_distortion.ROOT=ROOT;inherited.inherited_frame.ROOT=ROOT
from return_normalization import guarded_skeleton
from gap_payment import keep_gaps,hard_guarded
from periodic_payment import periodic_cost


def write(name,obj):
    (ROOT/name).write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n',encoding='utf-8')


class Meter:
    def __init__(self,stage):
        self.stage=stage;self.cpu=time.process_time();self.wall=time.perf_counter();self.success=False;self.details={}
        base='RESOURCE_'+stage;name=base+'.json';k=2
        while (ROOT/name).exists():name=base+f'_v{k:03d}.json';k+=1
        self.name=name;atexit.register(self.finish)
    def finish(self):
        write(self.name,{'stage':self.stage,'status':'completed' if self.success else 'failed_or_interrupted',
            'process_CPU_seconds':time.process_time()-self.cpu,'wall_seconds':time.perf_counter()-self.wall,
            'memory':memory(),**self.details})


if __name__=='__main__':
    meter=Meter('inheritance_preflight')
    manifest=json.loads((C1/'CONT01_DELIVERY_MANIFEST.json').read_text())
    for p,h in manifest['files'].items():assert file_hash(C1/p)==h,p
    import finalize as old_finalize
    old_finalize.ROOT=C1
    transitive=old_finalize.verify_pins()
    critical=json.loads((C1/'CRITICAL_WITNESS_CERTIFICATE.json').read_text())
    assert critical['frozen_combined_escape_verified'] and critical['all_raw4_intervals_ineligible_verified']
    write('INPUT_MANIFEST.json',{'Continuation01_manifest_sha256':file_hash(C1/'CONT01_DELIVERY_MANIFEST.json'),
        'Continuation01_files':manifest['files'],'HEAD':manifest['HEAD'],'branch':manifest['branch'],
        'historical_hash_pin_counts':transitive,
        'original_critical_gap':critical['original_R_star'],
        'frozen_interface':'Q_B <=(41+48 C_seq+102 C_DF) A + R_next^P',
        'B3_B4_necessary_conditions':['no frozen same-operation/same-old-g match','q(h)>2A(G_h)',
            'no raw/G/H local5A arc through h','all full-period cuts/variants cyclic L>9A'],
        'original_R_next_P_definition_unchanged':True})
    meter.success=True;meter.details.update(C1_files=len(manifest['files']),transitive_pin_counts=transitive)
    print('PASS Continuation01 and transitive historical pins',transitive,flush=True)
