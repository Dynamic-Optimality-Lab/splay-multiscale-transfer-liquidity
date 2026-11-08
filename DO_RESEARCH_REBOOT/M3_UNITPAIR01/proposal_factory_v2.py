"""Preparation-only fixtures; the production predicate is checked independently."""
import ast,inspect,sys
from types import SimpleNamespace
sys.path.insert(0,'DO_RESEARCH_REBOOT/M3_TWOGAP_AUD01')
import reference as R
def _fixture_alpha(am,word):
    def build(slot):
        rec=am.slots[slot];children=[]
        for kind,ref in am.kids[slot]:
            children.append(build(ref) if kind==0 else ('port' if kind==1 else None))
        return (rec['key'],*children)
    def alpha(t):
        out=[]
        for path in R.SHADOW:
            n=t
            for side in path:
                if n is None or n=='port':break
                n=n[1+side]
            if n is None:out.append([2,0,0])
            elif n=='port':out.append([1,0,0])
            else:
                core=n[0]>=0 and n[0]<=128 and n[0]%16==0
                out.append([0,int(core),n[0]//16 if core else 0])
        return out
    t=build(0);source=alpha(t)
    for mode,x in word:t=R.splay(t,x)
    return source,alpha(t)
def proposals(module):
    out=SimpleNamespace(**vars(module));edits=[]
    for name in ('low','high'):
        parsed=ast.parse(inspect.getsource(getattr(module,name)));fn=parsed.body[0];removed=0
        kept=[]
        for node in fn.body:
            if isinstance(node,ast.Assert) and isinstance(node.test,ast.Call) and isinstance(node.test.func,ast.Attribute) and node.test.func.attr=='ev_ground' and isinstance(node.test.func.value,ast.Name) and node.test.func.value.id=='d':removed+=1
            else:kept.append(node)
        assert removed==1;fn.body=kept;alpha_nodes=0
        if name=='low':
            first=next(i for i,n in enumerate(fn.body) if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name) and n.targets[0].id=='w' and isinstance(n.value,ast.Call) and isinstance(n.value.func,ast.Name) and n.value.func.id=='exact_witness')
            last=next(i for i,n in enumerate(fn.body) if i>=first and isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name) and n.targets[0].id=='ta')
            alpha_nodes=last-first+1;assert alpha_nodes==5
            fn.body[first:last+1]=ast.parse('sa, ta = _fixture_alpha(am, word)').body
        ast.fix_missing_locations(parsed);ns=dict(vars(module));ns['_fixture_alpha']=_fixture_alpha;exec(compile(parsed,__file__+':'+module.__name__+'.'+name,'exec'),ns)
        setattr(out,name,ns[name]);edits.append({'module':module.__name__,'function':name,'duplicate_assert_removed':1,'eager_fixture_alpha_nodes_replaced':alpha_nodes})
    out.proposal_edits=edits;return out
