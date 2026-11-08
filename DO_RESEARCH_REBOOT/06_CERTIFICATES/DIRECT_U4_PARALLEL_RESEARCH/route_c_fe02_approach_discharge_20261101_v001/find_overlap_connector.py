"""Only the AD00B-authorized u=2 fixed-target provenance audit."""
import importlib.util
import json
import sys
from pathlib import Path

sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('original_fixed_connector',HERE/'find_fixed_connector.py')
c=importlib.util.module_from_spec(s);s.loader.exec_module(c)


def main():
    d=json.loads((HERE/'overlap_discharge_certificate.json').read_text())['cases']['2']
    assert not d['same_connector_success']
    start,target=c.encode(c.tt(d['synchronized_state'])),c.encode(c.tt(d['B0']))
    f={start:None};b={target:None};ff=[start];bf=[target];meet=None;levels=0;checks=0
    while ff and bf and meet is None:
        levels+=1
        if len(ff)<=len(bf):
            new=[]
            for code in ff:
                tree=c.decode(code)
                for x in range(1,c.N+1):
                    out,_=c.tu.trace(tree,x);dest=c.encode(out)
                    if dest not in f:f[dest]=(code,x);new.append(dest)
                    if dest in b:meet=dest;break
                if meet is not None:break
            ff=new
        else:
            new=[]
            for code in bf:
                tree=c.decode(code);x=tree[1]
                for pred in c.preimages(tree):
                    checks+=1
                    if pred not in b:b[pred]=(code,x);new.append(pred)
                    if pred in f:meet=pred;break
                if meet is not None:break
            bf=new
        assert len(f)<=c.BOUND and len(b)<=c.BOUND
        print(json.dumps(dict(level=levels,forward=len(f),backward=len(b),found=meet is not None)),flush=True)
    word=None
    if meet is not None:
        left=[];at=meet
        while f[at] is not None:at,x=f[at];left.append(x)
        word=left[::-1];at=meet
        while b[at] is not None:at,x=b[at];word.append(x)
        tree=c.decode(start)
        for x in word:tree,_=c.tu.trace(tree,x)
        assert c.encode(tree)==target
    result=dict(status='FIXED_CONNECTOR_FOUND' if word is not None else 'FIXED_TARGET_NOT_REACHED',
        overlap=2,scope_sha256=c.sha(HERE/'AD00B_OVERLAP_SCOPE_GATE.md'),
        overlap_certificate_sha256=c.sha(HERE/'overlap_discharge_certificate.json'),
        source_keys=c.N,state_bound=c.BOUND,forward_states=len(f),backward_states=len(b),
        levels=levels,inverse_edges_source_checked=checks,connector=word,
        no_general_FE02_claim=True,no_larger_key_count_fit=True)
    with (HERE/'overlap_connector_certificate.json').open('x',encoding='utf-8') as out:
        json.dump(result,out,indent=2);out.write('\n')
    print(json.dumps(result,indent=2),flush=True)


if __name__=='__main__':main()
