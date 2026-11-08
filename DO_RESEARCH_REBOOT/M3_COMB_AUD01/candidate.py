"""Independent decoder for the combined RESTRICTED candidate, not a full-M3 API."""
import json,sys
from pathlib import Path
from array import array
from reference_v2 import tree,mirror,shadow
ROOT=Path(__file__).resolve().parents[2]
R=ROOT/'DO_RESEARCH_REBOOT'

class RestrictedCombinedCertificate:
    def __init__(self):self.active=None;self.data=None
    def load(self,g):
        if g==self.active:return
        self.data=None
        folder=R/('M3_GAP01' if g==0 else f'M3_GAPINT0{g}')
        c=json.loads((folder/'catalog.json').read_text());p=array('i');p.frombytes((folder/'potential.bin').read_bytes())
        if c['byteorder']!=sys.byteorder:p.byteswap()
        bt=[tree(r['tree']) for r in json.loads((R/'M3_LDR01/negative_run_census.json').read_text())['nodes']]
        sid={tuple(tuple(r) for r in s):i for i,s in enumerate(c['shadows'])}
        local={ai:j for r in range(9) for j,ai in enumerate(c['shadows_by_root'][str(r)])}
        self.data=c,p,{b:i for i,b in enumerate(bt)},sid,local;self.active=g

    @staticmethod
    def core(b):
        seen=set()
        def at(k):
            if k not in range(9) or k in seen:raise ValueError('invalid core tree')
            seen.add(k)
            ch=[]
            for kind,ref in [('kl','rl'),('kr','rr')]:
                v=b[ref][k];ch.append(at(v) if b[kind][k]==0 and v<9 else None)
            return (k,*ch)
        t=at(b['root'])
        if seen!=set(range(9)):raise ValueError('missing core')
        return t

    @staticmethod
    def profile(a,g):
        def balanced(keys):
            if not keys:return None
            m=len(keys)//2;return (16*keys[m],balanced(keys[:m]),balanced(keys[m+1:]))
        def at(pos,keys,level):
            if not keys:return None
            k,iss,label=a[pos]
            if level==0:k=0
            if k==1:return balanced(keys)
            if k!=0:raise ValueError('nonempty S interval has no node or port')
            if iss:
                if label not in keys:raise ValueError('S label outside source interval')
                left=tuple(x for x in keys if x<label);right=tuple(x for x in keys if x>label);code=16*label
            else:
                if not min(keys)<=g<=max(keys)+1:raise ValueError('anonymous gap outside interval')
                left=tuple(x for x in keys if x<g);right=tuple(x for x in keys if x>=g);code=16*g-8+level
            if level==2:return (code,balanced(left),balanced(right))
            lp,rp=(1,2) if pos==0 else ((3,4) if pos==1 else (5,6))
            return (code,at(lp,left,level+1),at(rp,right,level+1))
        return shadow(at(0,tuple(range(9)),0))

    def ordinary_J(self,s):
        sig=s['sigma'];support=[i for i,n in enumerate(sig) if n]
        if len(sig)!=10 or len(support)>1 or any(not 0<=n<=266 for n in sig):raise ValueError('uncovered multi-positive-gap domain')
        if not 0<=s['mu']<512 or s['mu'].bit_count()!=5:raise ValueError('invalid mask')
        g=support[0] if support else 0;reflected=g>=5;g=9-g if reflected else g
        b=s['b'];a=s['alpha']
        if b['root'] not in range(9) or not a[0][1] or a[0][2]!=b['root']:
            return {'value':0,'profile_found':False,'fallback':'not a synchronized low boundary'}
        self.load(g);c,p,bid,sid,local=self.data
        try:
            core=self.core(b)
            if reflected:
                core=mirror(core)
                a=[[k,iss,8-label if iss and (oldpos==0 or k==0) else label]
                   for oldpos in (0,2,1,6,5,4,3) for k,iss,label in [a[oldpos]]]
            profile=self.profile(a,g);ai=sid[profile];bi=bid[core];u=c['B_bases'][bi]+local[ai]
        except (KeyError,ValueError,AssertionError):return {'value':0,'profile_found':False,'fallback':'invalid low image'}
        value=p[u];assert -2<=value<=-c['psi'][bi]<=0
        return {'value':value,'profile_found':True,'canonical_gap':g,'table_node':u}

    @staticmethod
    def chi(b):return b['kr'][8]==0 and b['rr'][8]==19
    def ordinary(self,s):return self.ordinary_J(s)['value']-5*int(self.chi(s['b']))
    def midpoint(self,m):return -5*int(self.chi(m['b']))
