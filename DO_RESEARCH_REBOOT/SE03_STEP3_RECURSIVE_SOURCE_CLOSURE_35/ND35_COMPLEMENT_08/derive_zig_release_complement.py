"""Direct extension of the original ND35 map; no ordinary source evaluations."""
import bisect,collections,hashlib,json,sys,time
from pathlib import Path
F=Path(__file__).resolve().parent;O=F.parent/'CONTINUATION_04';B=F.parent.parent/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
CAP=float(sys.argv[1]);START=time.process_time()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def labels(t):
    s=set()
    def go(v):
        if v is None:return frozenset()
        a=go(v[1])|go(v[2])|{v[0]};s.add(a);return a
    go(t);return s
def main():
    lp=F/'lifetime_controls.json';op=O/'independent_core_sector_neutral.json';cp=F/'exact_challenge_sources.json'
    life=json.loads(lp.read_text());old=json.loads(op.read_text());challenge=json.loads(cp.read_text());inputs=[]
    for r in life['controls']:
        prior=next(x for x in old['controls'] if x['source']==r['source']);qby={d[0]:max(x[1] for x in r['D'] if x[0]==d[0]) for d in r['D']}
        inputs.append((r['source'],r['fine_steps'],{tuple(d) for d in r['D0']},{tuple(a['demand']):tuple(a['actual_bit']) for a in prior['g_plus']},
          {p['decrease_source_step']:tuple(p['actual_bit']) for p in prior['cyclic_level_pairings']},qby))
    rows=challenge['vine_family_control']['rows'];fine=[];neutral=set();nonneutral=set()
    def add(a,b,kind,unit=None,demand=None,slot=None,pattern=None,t=None):
        fine.append({'index':len(fine),'before':a,'after':b,'kind':kind,'unit':unit,'demand':demand,'slot':slot,'pattern':pattern,'t':t})
    for r in rows:
        jb=labels(r['BF_before'])
        for ev in r['A_events']:
            for z in ev['rotations']:
                a=len(jb-labels(z['before']));b=len(jb-labels(z['after']));add(a,b,'A',(r['t'],ev['j'],z['bit']),pattern=ev['pattern'],t=r['t'])
        ja=labels(r['A_after']);di=0
        for ev in r['BF_events']:
            double=len(ev['pattern'])==2;d=(r['t'],di+1) if double else None;changes=[(len(labels(z['before'])-ja),len(labels(z['after'])-ja)) for z in ev['rotations']];drops=sum(a-b for a,b in changes)
            if double:(nonneutral if drops else neutral).add(d);di+=1
            first=True
            for a,b in changes:
                slot=None
                if b<a:slot='PAYMENT' if double and first else ('B2_RELEASE' if double else 'BZIG_RELEASE');first=False
                add(a,b,'B',demand=d,slot=slot,pattern=ev['pattern'],t=r['t'])
    assert all(fine[i]['after']==fine[i+1]['before'] for i in range(len(fine)-1)) and fine[0]['before']==fine[-1]['after']
    ups=collections.defaultdict(list);cross={}
    for f in fine:
        if f['after']-f['before']==1:ups[f['after']].append(f['index'])
    for f in fine:
        if f['after']-f['before']==-1:
            uu=ups[f['before']];u=uu[bisect.bisect_left(uu,f['index'])-1];cross[f['index']]=tuple(fine[u]['unit'])
    gp={tuple(f['demand']):cross[f['index']] for f in fine if f['slot']=='PAYMENT'}
    assert set(gp)==nonneutral and len(set(cross.values()))==len(cross)
    inputs.append(('VINE8',fine,neutral,gp,cross,{r['t']:r['Q'] for r in rows}))
    reports=[]
    for name,fine,D0,gp,cross,qby in inputs:
        extra={};details=[]
        for d in sorted(D0):
            t,k=d
            if k!=qby[t]:continue
            bf=[f for f in fine if f['kind']=='B' and f['t']==t];last=bf[-1]
            assert len(last['pattern'])==1 and last['slot']=='BZIG_RELEASE'
            u=cross[last['index']];assert u not in gp.values() and u not in extra.values();extra[d]=u
            details.append({'neutral_terminal_demand':d,'actual_zig_release_step':last['index'],'actual_A_donor':u})
        gz=dict(gp);gz.update(extra);assert len(gz)==len(gp)+len(extra) and len(set(gz.values()))==len(gz)
        internal=D0-set(extra)
        reports.append({'source':name,'original_gplus_values_preserved':len(gp),'terminal_neutral_paid':len(extra),'remaining_internal_neutral':len(internal),
          'direct_new_pairs':details,'g_Z':[{'demand':d,'unit':u} for d,u in sorted(gz.items())],'D_internal_neutral':sorted(internal),'old_owner_maps_modified':False})
    v=next(x for x in reports if x['source']=='VINE8');assert v['terminal_neutral_paid']>0 and v['remaining_internal_neutral']==2
    out={'status':'DIRECT_ZIG_RELEASE_EXTENSION_SOURCE_CONTROLS_PASS','controls':reports,'source_queries':0,'source_engine_calls':0,
      'universal_statement_is_symbolic_not_inferred_from_controls':True,'Objective_I':'OPEN','Objective_II':'DEFERRED',
      'input_sha256':{str(p):sha(p) for p in (lp,op,cp,F/'ZIG_RELEASE_COMPLEMENT_THEOREM.md',F/'derive_zig_release_complement.py')}}
    with (F/'zig_release_complement_controls.json').open('x',encoding='utf8') as f:json.dump(out,f,indent=2)
    print(json.dumps({'status':out['status'],'controls':[{k:r[k] for k in ('source','original_gplus_values_preserved','terminal_neutral_paid','remaining_internal_neutral')} for r in reports]}),flush=True)
    assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error=repr(ex);raise
    finally:
        with (B/'audit_proof302_exit.json').open('x',encoding='utf8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0},f)
