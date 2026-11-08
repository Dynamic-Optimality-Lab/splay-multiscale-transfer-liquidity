"""Signature dispatch for all45 two-unit supports; original high semantics unchanged."""
import json,sys
from pathlib import Path
sys.path.insert(0,'DO_RESEARCH_REBOOT/M3_TWOGAP_AUD01')
import reference as R
BASE=Path(__file__).resolve().parent;OLD=BASE.parent/'M3_TWOGAP01'
def reflected_alpha(a):return tuple((kind,iss,8-k if iss and kind==0 else k) for p in (0,2,1,6,5,4,3) for kind,iss,k in [a[p]])
class UnitPairCertificate:
    def __init__(self):
        self.bank=json.loads((BASE/'B_bank.json').read_text());self.bid={R.frozen(t):i for i,t in enumerate(self.bank['trees'])};self.active=None;self.table=None
    def load(self,g,h):
        if self.active==(g,h):return
        self.table=None
        if (g,h)==(0,1):
            m=json.loads((OLD/'decoder_metadata.json').read_text());p=json.loads((OLD/'potential_sparse.json').read_text());values=p['labels']
        else:
            folder=BASE/f'p{g}_{h}';m=json.loads((folder/'metadata.json').read_text());p=json.loads((folder/'potential.json').read_text());values=p['values']
        self.table=(m['classes'],{R.frozen(a):i for i,a in enumerate(m['shadows'])},{int(k):v for k,v in values.items()});self.active=(g,h)
    @staticmethod
    def scope(s):
        sig=s['sigma'];support=[i for i,n in enumerate(sig) if n]
        if len(sig)!=10 or len(support)!=2 or any(sig[i]!=1 for i in support):raise ValueError('outside distinct two-unit signature family')
        if not 0<=s['mu']<512 or s['mu'].bit_count()!=5:raise ValueError('invalid mask')
        return tuple(support)
    def J(self,s):
        g,h=self.scope(s);reflected=g+h>9
        if reflected:g,h=9-h,9-g
        b=self.bid[R.core_view(s['b'])];a=R.raw_normalize(s['alpha'])
        if reflected:b=self.bank['mirror'][b];a=reflected_alpha(a)
        self.load(g,h);N,aid,values=self.table;ai=aid.get(a);psi=self.bank['psi'][b]
        if ai is None or not a[0][1] or a[0][2]!=self.bank['trees'][b][0]:return -psi
        v=values.get(b*N+ai,-psi);assert -2<=v<=-psi;return v
    @staticmethod
    def chi(b):return b['kr'][8]==0 and b['rr'][8]==19
    def O(self,s):return self.J(s)-5*int(self.chi(s['b']))
    def M(self,m):self.scope(m);return -5*int(self.chi(m['b']))
