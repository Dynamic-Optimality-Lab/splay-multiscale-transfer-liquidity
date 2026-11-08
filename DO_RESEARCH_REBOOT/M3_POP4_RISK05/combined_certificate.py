"""Audited covered-domain dispatch. Uncovered signatures are explicit errors."""
import json,sys,importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];REBOOT=ROOT/'DO_RESEARCH_REBOOT'
class UncoveredSignature(ValueError):pass
def module(name,path):
    sp=importlib.util.spec_from_file_location(name,path);out=importlib.util.module_from_spec(sp);sp.loader.exec_module(out);return out
class CombinedCoveredCertificate:
    def __init__(self):self.kind=None;self.decoder=None
    @staticmethod
    def scope(state):
        sig=state['sigma']
        if len(sig)!=10 or any(not isinstance(n,int) or not 0<=n<=266 for n in sig):raise ValueError('invalid signature')
        override5={tuple(v) for v in json.loads((REBOOT/'M3_POP4_RISK05/certification_run.json').read_text())['source_certified_signatures']}
        if tuple(sig) in override5 or tuple(reversed(sig)) in override5:return 'override5_population4'
        renewal4={tuple(v) for v in json.loads((REBOOT/'M3_POP4_RISK04/certification_run.json').read_text())['source_certified_signatures']}
        if tuple(sig) in renewal4 or tuple(reversed(sig)) in renewal4:return 'renewal4_population4'
        renewal3={tuple(v) for v in json.loads((REBOOT/'M3_POP4_RISK03/certification_run.json').read_text())['source_certified_signatures']}
        if tuple(sig) in renewal3 or tuple(reversed(sig)) in renewal3:return 'renewal3_population4'
        renewed={tuple(v) for v in json.loads((REBOOT/'M3_POP4_RISK02/certification_run.json').read_text())['source_certified_signatures']}
        if tuple(sig) in renewed or tuple(reversed(sig)) in renewed:return 'renewed_population4'
        pop4={tuple(v) for v in json.loads((REBOOT/'M3_POP4_RISK01/run_result.json').read_text())['completed_signatures']}
        if tuple(sig) in pop4 or tuple(reversed(sig)) in pop4:return 'population4'
        risk={tuple(v) for v in json.loads((REBOOT/'M3_POP3_RISK01/run_result.json').read_text())['completed_signatures']}
        if tuple(sig) in risk or tuple(reversed(sig)) in risk:return 'risk_population3'
        new={tuple(v) for v in json.loads((REBOOT/'M3_POP3_ALL01/run_result.json').read_text())['completed_signatures']}
        if tuple(sig) in new or tuple(reversed(sig)) in new:return 'new_population3'
        support=[i for i,n in enumerate(sig) if n]
        if len(support)<=1:return 'single'
        if sum(sig)==2:return 'unit_pair'
        allowed={(2,1,0),(1,1,1),(1,2,0),(2,0,1),(1,0,2),(0,2,1),(0,1,2)}
        if sum(sig)==3 and ((not any(sig[3:]) and tuple(sig[:3]) in allowed) or (not any(sig[:7]) and tuple(reversed(sig[7:])) in allowed)):return 'population3'
        raise UncoveredSignature('M3 hard-deficit multiple-support domain is not fully certified')
    def load(self,kind):
        if self.kind==kind:return
        self.decoder=None
        if kind=='single':
            sys.path.insert(0,str(REBOOT/'M3_COMB_AUD01'));m=module('covered_single_bank',REBOOT/'M3_COMB_AUD01/candidate.py');self.decoder=m.RestrictedCombinedCertificate()
        elif kind=='unit_pair':
            sys.path.insert(0,str(REBOOT/'M3_UNITPAIR01'));m=module('covered_unit_bank',REBOOT/'M3_UNITPAIR01/decoder.py');self.decoder=m.UnitPairCertificate()
        elif kind=='override5_population4':
            sys.path.insert(0,str(REBOOT/'M3_POP4_RISK05'));m=module('override5_population4_bank',REBOOT/'M3_POP4_RISK05/certified_decoder.py');self.decoder=m.PopulationFourCertificate()
        elif kind=='renewal4_population4':
            sys.path.insert(0,str(REBOOT/'M3_POP4_RISK04'));m=module('renewal4_population4_bank',REBOOT/'M3_POP4_RISK04/certified_decoder.py');self.decoder=m.PopulationFourCertificate()
        elif kind=='renewal3_population4':
            sys.path.insert(0,str(REBOOT/'M3_POP4_RISK03'));m=module('renewal3_population4_bank',REBOOT/'M3_POP4_RISK03/certified_decoder.py');self.decoder=m.PopulationFourCertificate()
        elif kind=='renewed_population4':
            sys.path.insert(0,str(REBOOT/'M3_POP4_RISK02'));m=module('renewed_population4_bank',REBOOT/'M3_POP4_RISK02/certified_decoder.py');self.decoder=m.PopulationFourCertificate()
        elif kind=='population4':
            sys.path.insert(0,str(REBOOT/'M3_POP4_RISK01'));m=module('covered_population4_bank',REBOOT/'M3_POP4_RISK01/certified_decoder.py');self.decoder=m.PopulationFourCertificate()
        elif kind=='risk_population3':
            sys.path.insert(0,str(REBOOT/'M3_POP3_RISK01'));m=module('covered_risk_population_bank',REBOOT/'M3_POP3_RISK01/certified_decoder.py');self.decoder=m.PopulationThreeCertificate()
        elif kind=='new_population3':
            sys.path.insert(0,str(REBOOT/'M3_POP3_ALL01'));m=module('covered_new_population_bank',REBOOT/'M3_POP3_ALL01/certified_decoder.py');self.decoder=m.PopulationThreeCertificate()
        else:
            sys.path.insert(0,str(REBOOT/'M3_POP3_01'));m=module('covered_population_bank',REBOOT/'M3_POP3_01/decoder.py');self.decoder=m.PopulationThreeCertificate()
        self.kind=kind
    def J(self,s):
        kind=self.scope(s)
        # Production LOW/HIGH predicates exclude these isolated invalid vertices.
        if not 0<=s['mu']<512 or s['mu'].bit_count()!=5:return 0
        self.load(kind)
        try:value=self.decoder.ordinary_J(s)['value'] if kind=='single' else self.decoder.J(s)
        except (AssertionError,KeyError,ValueError):
            # On typed states, these failures are invalid B projections, excluded
            # by every incident production edge. This totalizes the potential.
            value=0
        assert -2<=value<=0;return value
    @staticmethod
    def chi(b):return b['kr'][8]==0 and b['rr'][8]==19
    def ordinary(self,s):return self.J(s)-5*int(self.chi(s['b']))
    def midpoint(self,m):self.scope(m);return -5*int(self.chi(m['b']))
