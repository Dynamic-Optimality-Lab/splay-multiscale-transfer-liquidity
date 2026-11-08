"""One-table-at-a-time signed certificate for the explicitly named population5 family."""
import json,sys
from pathlib import Path
sys.path.insert(0,'DO_RESEARCH_REBOOT/M3_TWOGAP_AUD01')
import reference as R
BASE=Path(__file__).resolve().parent
CASES={tuple(v) for v in json.loads((BASE/'certification_run.json').read_text())['source_certified_signatures']}

def ra(a):return tuple((kind,iss,8-k if iss and kind==0 else k) for p in (0,2,1,6,5,4,3) for kind,iss,k in [a[p]])
class PopulationFiveCertificate:
    def __init__(self):
        self.B=json.loads((BASE.parent/'M3_UNITPAIR01/B_bank.json').read_text());self.bid={R.frozen(t):i for i,t in enumerate(self.B['trees'])};self.active=None;self.table=None
    @staticmethod
    def scope(s):
        sig=s['sigma']
        if len(sig)!=10 or sum(sig)!=5 or len([n for n in sig if n])<2:raise ValueError('outside population5 family')
        if not 0<=s['mu']<512 or s['mu'].bit_count()!=5:raise ValueError('invalid mask')
        canonical=max(tuple(sig),tuple(reversed(sig)))
        if canonical in CASES:return canonical,tuple(sig)!=canonical
        raise ValueError('outside new total5 signatures')
    def load(self,sig):
        if self.active==sig:return
        self.table=None;folder=BASE/('s'+''.join(map(str,sig)));m=json.loads((folder/'metadata.json').read_text());p=json.loads((folder/'potential.json').read_text())
        self.table=(m['classes'],{R.frozen(a):i for i,a in enumerate(m['shadows'])},{int(k):v for k,v in p['values'].items()});self.active=sig
    def inspect(self,s):
        sig,reflected=self.scope(s);b=self.bid[R.core_view(s['b'])];a=R.raw_normalize(s['alpha'])
        if reflected:b=self.B['mirror'][b];a=ra(a)
        self.load(sig);N,aid,values=self.table;ai=aid.get(a);psi=self.B['psi'][b]
        valid=ai is not None and a[0][1] and a[0][2]==self.B['trees'][b][0]
        v=values.get(b*N+ai,-psi) if valid else -psi;assert -2<=v<=-psi
        return {'value':v,'canonical_sigma':sig,'reflected':reflected,'B':b,'A':ai,'profile_found':bool(valid)}
    def J(self,s):return self.inspect(s)['value']
    @staticmethod
    def chi(b):return b['kr'][8]==0 and b['rr'][8]==19
    def O(self,s):return self.J(s)-5*int(self.chi(s['b']))
    def M(self,m):self.scope(m);return -5*int(self.chi(m['b']))
