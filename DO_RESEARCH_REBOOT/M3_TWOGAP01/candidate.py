"""Constructed fixed-signature candidate; independent campaign audit pending."""
import json
from pathlib import Path
from prefix_profiles import normalize
BASE=Path(__file__).resolve().parent
SIG=[1,1]+[0]*8
def freeze(x):return tuple(freeze(v) for v in x) if isinstance(x,list) else x
class TwoGapCandidate:
    def __init__(self):
        m=json.loads((BASE/'decoder_metadata.json').read_text());p=json.loads((BASE/'potential_sparse.json').read_text())
        self.N=m['classes'];self.sid={freeze(a):i for i,a in enumerate(m['shadows'])};self.bid={freeze(t):i for i,t in enumerate(m['B_trees'])}
        self.psi=m['psi'];self.labels={int(k):v for k,v in p['labels'].items()}
    @staticmethod
    def validate(s):
        if s['sigma']!=SIG:raise ValueError('candidate covers only sigma=(1,1,0,...,0)')
        if s['mu'].bit_count()!=5 or not 0<=s['mu']<512:raise ValueError('invalid mask')
    @staticmethod
    def core(b):
        seen=set()
        def at(i):
            if i not in range(9) or i in seen:raise ValueError('invalid core projection')
            seen.add(i);ch=[]
            for k,r in (('kl','rl'),('kr','rr')):
                ref=b[r][i];ch.append(at(ref) if b[k][i]==0 and ref<9 else None)
            return (i,*ch)
        tree=at(b['root'])
        if len(seen)!=9:raise ValueError('missing core')
        return tree
    def ordinary_J(self,s):
        self.validate(s)
        try:b=self.bid[self.core(s['b'])]
        except (ValueError,KeyError):return {'value':0,'default':'non-low core projection'}
        a=self.sid.get(normalize(s['alpha']))
        if a is None or not s['alpha'][0][1] or s['alpha'][0][2]!=s['b']['root']:
            return {'value':-self.psi[b],'B_core':b,'default':'unlisted or unsynchronized alpha'}
        value=self.labels.get(b*self.N+a,-self.psi[b]);assert -2<=value<=-self.psi[b]
        return {'value':value,'B_core':b,'A_class':a}
    @staticmethod
    def chi(b):return b['kr'][8]==0 and b['rr'][8]==19
    def ordinary(self,s):return self.ordinary_J(s)['value']-5*int(self.chi(s['b']))
    def midpoint(self,m):
        self.validate(m);return -5*int(self.chi(m['b']))
