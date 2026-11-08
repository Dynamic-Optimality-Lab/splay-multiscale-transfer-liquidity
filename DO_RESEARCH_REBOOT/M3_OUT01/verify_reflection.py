"""Complete GAP01 profile/word and B-kernel reflection identity check."""
import sys,json,time
from pathlib import Path
sys.path[:0]=['DO_RESEARCH_REBOOT/M3_GAP01','DO_RESEARCH_REBOOT/M3_GAPINT01']
from build import decorate,options
from core_refinement_v2 import S,V,rho
from framework_v2 import reflect_alpha
BASE=Path('DO_RESEARCH_REBOOT/M3_OUT01')

def rev(t):
    return S.LEAF if t[0]=='leaf' else S.node(8-t[1],rev(t[3]),rev(t[2]))

def shadow9(t):
    def at(path):
        n=t
        for side in path:
            if n[0]=='leaf':return (1,0,0)
            n=n[2+side]
        if n[0]=='leaf':return (1,0,0)
        core=n[1] in range(9)
        return (0,int(core),n[1] if core else 0)
    return tuple(at(p) for p in ((),(0,),(1,),(0,0),(0,1),(1,0),(1,1)))

def main():
    out=BASE/'reflection_audit.json';assert not out.exists();start=time.process_time()
    c=json.loads(Path('DO_RESEARCH_REBOOT/M3_GAP01/catalog.json').read_text())
    bc=json.loads(Path('DO_RESEARCH_REBOOT/M3_LDR01/negative_run_census.json').read_text())
    bt=[V.from_serial(r['tree']) for r in bc['nodes']];bid={t:i for i,t in enumerate(bt)}
    models=queries=0
    for m in c['models']:
        t=decorate(bt[m['core']],m['counts']);r=rev(t);models+=1
        assert rho(reflect_alpha(shadow9(r)))==rho(shadow9(t))
        for H,x,dest,word,depths in options(t):
            cur=r
            for mode,k in word:
                assert mode=='K';cur=S.trace(cur,8-k)[0]
            assert rho(reflect_alpha(shadow9(cur)))==rho(shadow9(dest))
            queries+=1
        assert time.process_time()-start<120,'UNKNOWN reflection CPU cap'
    kernels=0
    for i,b in enumerate(bt):
        rb=rev(b);assert c['psi'][i]==c['psi'][bid[rb]]
        pre=S.trace(V.insert(b,-1),-1)[0];rpre=S.trace(V.insert(rb,9),9)[0]
        assert rev(pre)==rpre
        for x in range(9):
            a=S.trace(pre,x);b2=S.trace(rpre,8-x)
            assert rev(a[0])==b2[0] and S.lookup(pre,x)[1]==S.lookup(rpre,8-x)[1]
            kernels+=1
    assert models==48450 and kernels==43758 and queries<1000000
    result={'status':'PASS_COMPLETE_LOW_REFLECTION_IDENTITIES','models':models,
            'A_word_queries':queries,'B_kernel_queries':kernels,'core_debt_reflection_mismatches':0,
            'raw_high_states_reflected':False,'cpu_seconds':round(time.process_time()-start,3)}
    with out.open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
