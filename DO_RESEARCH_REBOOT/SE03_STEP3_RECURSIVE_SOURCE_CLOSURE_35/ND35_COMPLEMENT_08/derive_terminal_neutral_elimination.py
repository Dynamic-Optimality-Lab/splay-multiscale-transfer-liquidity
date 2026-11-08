"""Challenge the uniform terminal-neutral proof on saved actual fine traces.

Reuse the accepted ND35 crossing bijection, explicitly transpose it, and
retain every actual source bit. No fresh ordinary source evaluations.
"""
import hashlib,json,sys,time
from pathlib import Path
F=Path(__file__).resolve().parent;C=F.parent;O=C/'CONTINUATION_04';B=C.parent/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
CAP=float(sys.argv[1]);START=time.process_time()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    p=F/'lifetime_controls.json';life=json.loads(p.read_text());oldp=O/'independent_core_sector_neutral.json';nd=json.loads(oldp.read_text());reports=[]
    for r in life['controls']:
        rows=json.loads(Path(r['source_path']).read_text())['period_rows'];fine=r['fine_steps'];T=len(rows);D={tuple(d) for d in r['D']};Dplus={tuple(d) for d in r['Dplus']};D0={tuple(d) for d in r['D0']};U={tuple(u) for u in r['U']};S=set(r['S']);ends=[i for i,z in enumerate(rows) if z['genuine_F']]
        old=next(c for c in nd['controls'] if c['source']==r['source']);cross={a['decrease_source_step']:tuple(a['actual_bit']) for a in old['cyclic_level_pairings']}
        inv={u:i for i,u in cross.items()};Pbits={tuple(x) for x in r['birth_bits']};assert set(inv)==Pbits and len(inv)==len(cross)
        for a in old['cyclic_level_pairings']:
            up=fine[a['positive_source_step']];down=fine[a['decrease_source_step']]
            assert tuple(up['unit'])==tuple(a['actual_bit']) and len(up['added'])-len(up['removed'])==1 and len(down['removed'])-len(down['added'])==1
        seeds=[];h0={};terminal=set()
        for k,end in enumerate(ends):
            ids=[];i=(ends[k-1]+1)%T
            while True:
                ids.append(i)
                if i==end:break
                i=(i+1)%T
            ts=[rows[i]['t'] for i in ids];g=rows[ids[0]]['BF_before'][0];x=rows[end]['key'];assert rows[ids[0]]['A_before'][0]==g and x!=g
            I=sorted(s for s in S if (s<g if x<g else s>g));assert I
            aindices=[f['index'] for t in ts for f in fine if f['t']==t and f['kind']=='A']
            losses=[i for i in aindices if I in fine[i]['removed']];assert losses
            seedindex=losses[-1];f=fine[seedindex];assert len(f['added'])-len(f['removed'])==1;u=tuple(f['unit'])
            bi=[f['index'] for f in fine if f['t']==rows[end]['t'] and f['kind']=='B'];z=bi[-1];assert len(fine[z]['removed'])-len(fine[z]['added'])==1
            q=rows[end]['qF'];d=(rows[end]['t'],q) if q else None
            seeds.append({'macro_end_t':rows[end]['t'],'old_root':g,'target':x,'side_cluster':I,'last_loss_step':seedindex,'positive_bit':u,'final_B_decrease_slot':z,'Q':q,'last_double':d,'last_double_neutral':d in D0 if d else False,'final_B_is_zig':len(fine[z]['pattern'])==1})
            if d:terminal.add(d)
            units=[(rows[i]['t'],j,b) for i in ids for j in range(1,rows[i]['a']+1) for b in (0,1)]
            h0.update(zip([(rows[end]['t'],j) for j in range(1,q+1)],units))
        assert len({tuple(z['positive_bit']) for z in seeds})==len(seeds)==len({z['final_B_decrease_slot'] for z in seeds})
        swaps=[]
        for e in seeds:
            d,u=e['final_B_decrease_slot'],tuple(e['positive_bit']);other=inv[u];old=cross[d]
            if other!=d:
                cross[d],cross[other]=u,old;inv[u],inv[old]=d,other
                swaps.append({'required_slot':d,'required_bit':u,'displaced_slot':other,'displaced_bit':old})
        assert all(cross[e['final_B_decrease_slot']]==tuple(e['positive_bit']) for e in seeds) and set(cross.values())==Pbits and len(set(cross.values()))==len(cross)
        gt={tuple(e['last_double']):tuple(e['positive_bit']) for e in seeds if e['last_double'] is not None}
        for d in sorted(Dplus-terminal):
            slots=[f['index'] for f in fine if f['kind']=='B' and f['demand'] is not None and tuple(f['demand'])==d and f['slot']=='PAYMENT'];assert len(slots)==1
            gt[d]=cross[slots[0]]
        assert set(gt)==Dplus|terminal and len(set(gt.values()))==len(gt) and set(gt.values())<=U
        internal=D-set(gt);assert internal==D0-terminal
        inverse={u:d for d,u in h0.items()};added={};liability={};traces=[]
        for start in sorted(D-set(h0)):
            d=start;seen=set();path=[]
            while d in gt:
                assert d not in seen;seen.add(d);u=gt[d];path.append({'demand':d,'unit':u,'h0_owner':inverse.get(u)})
                if u not in inverse:added[start]=u;break
                d=inverse[u]
            else:assert d in internal;liability[start]=d
            traces.append({'root':start,'path':path,'free_bit':added.get(start),'internal_neutral_label':liability.get(start)})
        assert len(set(added.values()))==len(added) and not set(added.values())&set(h0.values()) and len(set(liability.values()))==len(liability)
        reports.append({'source':r['source'],'Q':len(D),'nonneutral_count':len(Dplus),'neutral_count':len(D0),'neutral_terminal_eliminated':len(terminal&D0),'internal_neutral_count':len(internal),
          'genuine_macros':len(seeds),'source_seeds':seeds,'provisional_crossing_swaps':swaps,'g_T':[{'demand':d,'unit':u} for d,u in sorted(gt.items())],
          'R_T':sorted(U-set(gt.values())),'D_internal_neutral':sorted(internal),'h0_preserving_free_pairs':[{'demand':d,'unit':u} for d,u in sorted(added.items())],
          'remaining_distinct_internal_liabilities':traces,'h0_values_changed':0,'old_frozen_maps_modified':False})
    out={'status':'SOURCE_CONTROLS_PASS_UNIFORM_TERMINAL_NEUTRAL_REDUCTION','controls':reports,'source_queries':0,'source_engine_calls':0,
      'universal_proof_is_symbolic_not_inferred_from_controls':True,'Objective_I':'OPEN','Objective_II':'DEFERRED',
      'input_sha256':{str(p):sha(p) for p in (p,oldp,F/'TERMINAL_NEUTRAL_ELIMINATION.md',F/'derive_terminal_neutral_elimination.py')}}
    with (F/'terminal_neutral_controls.json').open('x',encoding='utf8') as f:json.dump(out,f,indent=2)
    print(json.dumps({'status':out['status'],'controls':[{k:r[k] for k in ('source','Q','nonneutral_count','neutral_count','neutral_terminal_eliminated','internal_neutral_count','genuine_macros')} for r in reports]}),flush=True)
    assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error=repr(ex);raise
    finally:
        with (B/'audit_proof298_exit.json').open('x',encoding='utf8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0},f)
