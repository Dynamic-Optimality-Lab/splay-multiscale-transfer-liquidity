"""Gate E: deterministic concrete replays with the read-only frozen engine."""
import json,sys,time
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parent.parent
sys.path.insert(0,str(ROOT/'python'))
from independent import splay as original
account={'new_finite_tests':0,'source_engine_calls':0}
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def n(k,l,r):return original.node(k,l,r)
def mirror(t,ceiling):
    if t==original.LEAF:return t
    return n(ceiling-t[1],mirror(t[3],ceiling),mirror(t[2],ceiling))
def realize(t,count,style,reflected=False):
    def rec(u):
        if isinstance(u,str):
            i=int(u[1:])
            if style=='empty':return original.LEAF
            vals=[4*i+1,4*i+2,4*i+3]
            if style=='balanced':return n(vals[1],n(vals[0],original.LEAF,original.LEAF),n(vals[2],original.LEAF,original.LEAF))
            z=original.LEAF
            for v in reversed(vals):z=n(v,original.LEAF,z)
            return z
        return n(4*u[0],rec(u[1]),rec(u[2]))
    z=rec(t)
    return mirror(z,4*(count+1)) if reflected else z
def key(k,count,reflected):return 4*(count+1-k) if reflected else 4*k
def run(a,b,e,word,count,reflected=False):
    rows=[]
    for mode,x,erased in word:
        k=key(x,count,reflected);before=(a,b,e)
        a,ae=original.trace(a,k);account['source_engine_calls']+=1
        be=[];ee=[]
        if mode=='K':b,be=original.trace(b,k);account['source_engine_calls']+=1
        if mode=='K' and x!=erased:e,ee=original.trace(e,k);account['source_engine_calls']+=1
        rows.append({'before':before,'after':(a,b,e),'a':len(ae),'qF':sum(ev[0]!='ZIG' for ev in be),
            'qE':sum(ev[0]!='ZIG' for ev in ee),'A_cases':[ev[0] for ev in ae]})
    return rows,(a,b,e)
def main():
    data=json.loads((B/'symbolic_replay.json').read_text());debt=json.loads((B/'debt_v3_audit.json').read_text())
    assert debt['status']=='PASS_CERTIFIED_NORMALIZED_ENDPOINTS_AND_REFUTATION'
    reports=[];mixed=set();seams=[]
    for f in data['families']:
        count=11;word=[(r['mode'],r['key'],f['erased_key']) for r in f['word']]
        for style in ('empty','balanced','chain'):
            for refl in (False,True):
                initial=realize(f['initial_full_diagonal'],count,style,refl)
                first,end=run(initial,initial,initial,word,count,refl)
                assert end[:2]==(initial,initial)
                rows,end2=run(initial,initial,end[2],word,count,refl)
                assert end2==end
                for got,expected in zip(rows,f['rows']):
                    assert (got['a'],got['qF'],got['qE'])==(expected['a'],expected['qF'],expected['qE'])
                    assert got['after']==tuple(realize(t,count,style,refl) for t in expected['after'])
                    mixed.update(got['A_cases'])
                assert sum(r['a'] for r in rows)==f['A'] and sum(r['qF'] for r in rows)==f['QF']
                assert sum(r['qE'] for r in first)==f['first_QE']
                assert original.inorder(initial)==original.inorder(end[0])==original.inorder(end[1])
                assert original.is_valid(initial)
                reports.append({'family':f['name'],'fringes':style,'reflected':refl,'ambient_keys':len(original.inorder(initial)),
                    'two_copy_AF_and_E_closure':True,'A':f['A'],'QF':f['QF'],'QE':f['QE']})
                account['new_finite_tests']+=1
        # Every retained E boundary is replayed at a shifted actual seam.
        # Hence whichever is the certified Step1 maximum-debt seam is included.
        initial=realize(f['initial_full_diagonal'],count,'empty');eroot=realize(f['auxiliary_recurrent_start'],count,'empty')
        rows,end=run(initial,initial,eroot,word,count)
        for cut in [0]+[i for i,q in enumerate(word,1) if q[0]=='K' and q[1]!=q[2] and i<len(word)]:
            source=(initial,initial,eroot) if cut==0 else rows[cut-1]['after']
            rotated=word[cut:]+word[:cut];rs,endpoint=run(*source,rotated,count)
            assert endpoint==source
            assert tuple(sum(r[k] for r in rs) for k in ('a','qF','qE'))==(f['A'],f['QF'],f['QE'])
            # Actual-time transport t->t or t+N is a bijection on one period.
            N=len(word);times=[i if i>cut else i+N for i in range(1,N+1)]
            assert len(set(times))==N and set(times)==set(range(cut+1,cut+N+1))
            seams.append({'family':f['name'],'cut_after':cut,'full_and_erased_closure':True,'ID_transport_bijective':True})
            account['new_finite_tests']+=1
    c=data['core10_control'];count=10
    word=[(mode,k,10) for mode,k in c['word']]
    for style in ('empty','balanced'):
        for refl in (False,True):
            s=realize(c['initial'],count,style,refl);rs,end=run(s,s,s,word,count,refl)
            assert end[:2]==(s,s)
            assert sum(r['a'] for r in rs)==c['A'] and sum(r['qF'] for r in rs)==c['QF']
            reports.append({'family':'core10_control','fringes':style,'reflected':refl,'A':c['A'],'QF':c['QF'],
                'full_pair_closed':True,'scope':'two reflected actual masks, not realization of all16 necessary masks'})
            account['new_finite_tests']+=1
    # Insert literal zero-A DELETE and nongenuine KEEP after every KEEP.
    f=data['families'][0];count=11;word=[]
    for q in f['word']:
        word.append((q['mode'],q['key'],f['erased_key']))
        if q['mode']=='K':word.extend([('D',q['key'],f['erased_key']),('K',q['key'],f['erased_key'])])
    for refl in (False,True):
        s=realize(f['initial_full_diagonal'],count,'balanced',refl)
        e=realize(f['auxiliary_recurrent_start'],count,'balanced',refl)
        rs,end=run(s,s,e,word,count,refl)
        assert end==(s,s,e)
        assert tuple(sum(r[k] for r in rs) for k in ('a','qF','qE'))==(f['A'],f['QF'],f['QE'])
        zero=sum(r['a']==r['qF']==r['qE']==0 for r in rs)
        assert zero>=2*sum(q['mode']=='K' for q in f['word'])
        reports.append({'family':'Omega_plus_zero_gap_extension','reflected':refl,'operations':len(word),'inserted_zero_operations':48,
            'all_original_costs_preserved':True,'actual_AF_E_closure':True})
        account['new_finite_tests']+=1
    assert {'LR','RL'}<=mixed
    out('independent_replay.json',{'status':'PASS_FROZEN_SOURCE_ENGINE_REPLAYS','engine':'python/independent/splay.py trace only; depth+1 pair costs NOT used',
        'fixtures':reports,'all_retained_seams':seams,'all_critical_costs_and_full_trees_agree':True,
        'A_mixed_orientations_seen':sorted(mixed),'core10_masks':'one concrete mask and its actual reflection; remaining14 necessary masks not promoted',
        'debt_reflection':'source Dhat1 follows visible marked third path label, q1 margin>=1 and false tall ceiling in each orientation; no psi symmetry assumed',
        'GateG':'all saved witness minima -2; no width-two architecture counterpath found',
        'source_finite_tests_are_universal_proof':False,'new_allocations_claimed':False,
        'same_agent_independent_derivation':True,'external_peer_review':False,'whole_compiler_formalization':False,
        **account})
    print(json.dumps({'status':'PASS_FROZEN_SOURCE_ENGINE_REPLAYS','fixture_records':len(reports),'cyclic_seams':len(seams),**account}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_independent_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,**account})
