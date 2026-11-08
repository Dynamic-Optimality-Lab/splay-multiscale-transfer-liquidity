"""New analytic selector and independent symbolic/fiber-minimum audit."""
import sys,json,time,hashlib
from pathlib import Path
sys.path[:0]=['DO_RESEARCH_REBOOT/M3_UNITPAIR01','DO_RESEARCH_REBOOT/M3_TWOGAP_AUD01']
import profiles as C
import reference as I
BASE=Path(__file__).resolve().parent

def main():
    out=BASE/'representation_audit.json';assert not out.exists();start=time.process_time()
    bank=BASE.parent/'M3_UNITPAIR01/B_bank.json';B=json.loads(bank.read_text());risk={k:set() for k in ('H1','0','9')};visits=0
    for bi,t in enumerate(B['trees']):
        for x in range(9):
            dep=B['depths'][bi][x];dst=B['destinations'][bi][x];w=2-dep//2;visits+=1
            if dep and w+B['psi'][dst]<2:risk['H1'].add((t[0],x))
            for g in ('0','9'):
                p=B['kernels'][g][bi][x];visits+=1
                if p is not None and p[1]+B['psi'][p[0]]<2:risk[g].add((t[0],x))
    # Independent derivation: grouped ALL fiber margins and their minima.
    margins={k:{(r,x):[] for r in range(9) for x in range(9)} for k in ('H1','0','9')}
    for r in range(9):
        for x in range(9):
            for bi,t in enumerate(B['trees']):
                if t[0]!=r:continue
                if B['depths'][bi][x]>0:margins['H1'][r,x].append(2-(B['depths'][bi][x]//2)+B['psi'][B['destinations'][bi][x]])
                for g in ('0','9'):
                    z=B['kernels'][g][bi][x]
                    if z is not None:margins[g][r,x].append(z[1]+B['psi'][z[0]])
    minima={k:{str(r)+','+str(x):min(v) if v else None for (r,x),v in rows.items()} for k,rows in margins.items()}
    for k in risk:
        independent={(r,x) for (r,x),v in margins[k].items() if v and min(v)<2};assert independent==risk[k]
        assert all(not v or min(v)>=2 for pair,v in margins[k].items() if pair not in risk[k])
    assert len(risk['H1'])==70 and len(risk['0'])==len(risk['9'])==49
    assert (1,0) not in risk['H1'] and (7,8) not in risk['H1']
    assert {(8-r,8-x) for r,x in risk['0']}==risk['9']
    assert {(8-r,8-x) for r,x in risk['H1']}==risk['H1']
    families=[(None,(p,)) for p in C.PATHS]
    for g in (0,9):families.extend((g,(p,q)) for p in C.PATHS for q in C.PATHS)
    plans=[]
    for g,word in families:
        t=C.full()
        for p in word:t=C.move(t,p)
        terminal=t[0];obs,required,forced=C.specification(g,word)
        independent=I.universe();need={()}
        for p in word:
            need.update(I.at(independent,p[:i])[0] for i in range(len(p)+1));key=I.at(independent,p)[0];independent=I.splay(independent,key)
        assert terminal==independent[0] and need==required
        assert all(terminal[:i] in required for i in range(len(terminal)))
        assert terminal in required and forced[terminal] is None
        plans.append({'helper':g,'word':word,'terminal_source_address':terminal,'required':sorted(required)})
    assert len(plans)==78 and visits==131274 and time.process_time()-start<120
    data={'bank_sha256':hashlib.sha256(bank.read_bytes()).hexdigest(),'risk':{k:sorted(v) for k,v in risk.items()},'minimum_margins':minima,'plans':plans,
      'identity':'w-J(t)+J(s)>=w+psi(Bt)-2','new_source_observables':0}
    with (BASE/'risk_selector.json').open('x') as f:json.dump(data,f,indent=2)
    report={'status':'PROVED_COMPLETE_SIGNED_REDUCTION_AND_INDEPENDENT_SELECTOR_AUDIT_PASS','pinned_bank_entries_visited':visits,
      'original_B_transitions_recomputed':0,'completed_source_roots_replayed':0,'independent_fiber_minima_equal':True,
      'word_shapes_independently_checked':78,'terminal_source_ancestry_real_required':True,'H1_risky_root_target_pairs':70,
      'H2_risky_pairs_per_outer_direction':49,'reflection_selector_equivariance':True,'strict_omitted_nonempty_H1_fibers':[[1,0],[7,8]],
      'cpu_seconds':round(time.process_time()-start,3),'bank_sha256':data['bank_sha256'],'representation_proved':True,'new_signatures_certified':0,'full_M3_proved':False}
    with out.open('x') as f:json.dump(report,f,indent=2)
    print(json.dumps(report,indent=2),flush=True)
if __name__=='__main__':main()
