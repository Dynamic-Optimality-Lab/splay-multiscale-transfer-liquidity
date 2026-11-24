from fast_physics import *
from types import SimpleNamespace
from collections import OrderedDict
sys.path.insert(0,str(REPO/'python'))
from independent import splay as ind


class TupleCode:
    """Exact pointer encoding of independent immutable tuple trees.

    Cached whole-subtree integers share untouched fringe work. Identity
    checks prevent Python object-ID reuse from being treated as equality.
    This is not a probabilistic state hash.
    """
    def __init__(self,n,limit=4096):self.n=n;self.b=(n+1).bit_length();self.limit=limit;self.cache=OrderedDict()
    def code(self,t):
        if t[0]=='leaf':return 0
        stack=[(t,False)];values={}
        while stack:
            node,done=stack.pop();key=id(node)
            if not done:
                entry=self.cache.get(key)
                if entry is not None and entry[0] is node:
                    self.cache.move_to_end(key);values[key]=entry[1];continue
                stack.append((node,True))
                if node[2][0]=='node':stack.append((node[2],False))
                if node[3][0]=='node':stack.append((node[3],False))
            else:
                _,k,l,rr=node
                lc=values.pop(id(l)) if l[0]=='node' else 0
                rc=values.pop(id(rr)) if rr[0]=='node' else 0
                lk=l[1] if l[0]=='node' else 0;rk=rr[1] if rr[0]=='node' else 0
                c=lc|rc|(lk<<((2*k-2)*self.b))|(rk<<((2*k-1)*self.b))
                values[key]=c;self.cache[key]=(node,c);self.cache.move_to_end(key)
                while len(self.cache)>self.limit:self.cache.popitem(last=False)
        return values[id(t)]|(t[1]<<(2*self.n*self.b))


def as_tuple(st):
    view=SimpleNamespace(ind=ind)
    return Replay.as_tuple(view,Tree(st))


def verify_source(s):
    n=len(s['initial_A']['children']);a=FullTree(s['initial_A']);b=FullTree(s['initial_B'])
    aa=as_tuple(s['initial_A']);bb=aa if s['initial_A']==s['initial_B'] else as_tuple(s['initial_B'])
    codec=TupleCode(n);ha=hashlib.sha256();hb=hashlib.sha256();A=Q=0;steps=0
    for t,(tag,x) in enumerate(s['operations'],1):
        aa,ev=ind.trace(aa,x);cost,_,_,detail=a.splay(x,b,'A')
        assert len(ev)==cost and [z[0] for z in ev]==[z[0] for z in detail]
        assert codec.code(aa)==a.code,(s['name'],t,'A full state')
        A+=cost;steps+=len(ev);ha.update(a.code.to_bytes((2*n+1)*codec.b//8+2,'little'))
        if tag=='K':
            bb,ev=ind.trace(bb,x);_,q,_,detail=b.splay(x,a,'B')
            assert sum(z[0]!='ZIG' for z in ev)==q
            assert [z[0] for z in ev]==[z[0] for z in detail]
            assert codec.code(bb)==b.code,(s['name'],t,'B full state')
            Q+=q;steps+=len(ev)
        hb.update(b.code.to_bytes((2*n+1)*codec.b//8+2,'little'))
    assert A==s['A'] and Q==s['Q_B']
    assert a.state()==s['initial_A'] and b.state()==s['initial_B']
    return {'source':s['name'],'population':n,'original_operations':len(s['operations']),
        'all_complete_A_B_operation_states_match_exact_independent_tuple_encoding':True,
        'all_actual_StepEv_case_sequences_and_costs_match':True,'A':A,'Q_B':Q,
        'independent_StepEv_checks':steps,'A_boundary_stream_sha256':ha.hexdigest(),'B_boundary_stream_sha256':hb.hexdigest(),
        'complete_original_paired_closure_verified':True,
        'qualification':'Full physical verification; original Pi/U/R6 is separate and not inferred from H guards.'}


if __name__=='__main__':
    meter=Meter('independent_large_physical_sources');out=[]
    sets=[json.loads((ROOT/'DILATED_SOURCES.json').read_text())]
    if (ROOT/'ADAPTIVE_LIFT_SOURCE.json').exists():sets.append([json.loads((ROOT/'ADAPTIVE_LIFT_SOURCE.json').read_text())])
    for ss in sets:
        for s in ss:
            z=verify_source(s);out.append(z);write('INDEPENDENT_LARGE_PHYSICS.json',out)
            print('PASS',s['name'],z['population'],z['original_operations'],'full-state pairs',flush=True)
    meter.success=True;meter.details['sources']=len(out)
