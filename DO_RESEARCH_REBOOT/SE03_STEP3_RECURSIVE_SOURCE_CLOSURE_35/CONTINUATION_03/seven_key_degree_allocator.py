"""Instantiate the new source law on saved original rows; never execute an access."""
import hashlib,json,sys,time
from pathlib import Path
F=Path(__file__).resolve().parent;P=F.parents[1]
B=P/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
START=time.process_time();CAP=float(sys.argv[1])
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def put(n,z):
    with (F/n).open('x',encoding='utf-8') as f:json.dump(z,f,indent=2)
def degree(tree,marks):
    deg={m:0 for m in marks}
    def visit(t,prev):
        if t is None:return
        k,l,r=t
        if k in marks:
            if prev is not None:deg[prev]+=1
            prev=k
        visit(l,prev);visit(r,prev)
    visit(tree,None)
    return deg
def D(tree,marks):return sum(max(v-2,0) for v in degree(tree,marks).values())
def main():
    path=B/'SOURCE_JOINT_REPAIR_03/actual_monotone_return_source.json'
    ownpath=B/'SOURCE_JOINT_REPAIR_03/actual_auxiliary_owner_extension.json'
    src=read(path);rr={r['t']:r for r in src['period_rows']};mm=src['funding']['macros']
    M={m['target'] for m in mm};assert len(M)==7
    h0={tuple(z['demand']):tuple(z['unit']) for z in src['funding']['h0']}
    h=dict(h0);data=[];bad=[]
    for m in mm:
        rs=[rr[t] for t in m['rows_t']];before=rs[0]['BF_before'];after=rs[-1]['BF_after']
        ds,dt=D(before,M),D(after,M);degs=degree(before,M);target=m['target']
        t=before;anc=[]
        while t[0]!=target:
            if t[0] in M:anc.append(t[0])
            t=t[1 if target<t[0] else 2]
        assert len(anc)==m['Q'];b=sum(degs[v]>=3 for v in anc);d=degs[target]
        kappa=min(d+m['Q'],2)-min(d,2);c=min(m['H'],3)
        margin=2*c-m['Q']+dt-ds
        assert margin==2*c-b-kappa
        row={'end_t':m['end_t'],'rows_t':m['rows_t'],'H':m['H'],'Q':m['Q'],
          'd':d,'b':b,'kappa':kappa,'D_source':ds,'D_target':dt,'c':c,'margin':margin}
        data.append(row)
        if margin<0:bad.append(row)
    if bad:
        put('degree_allocator_receipt.json',{'status':'UNSUPPORTED_LIVE_EXCEPTION_NOT_FULL_FUNDING',
          'exceptions':bad,'all_margins':data,'source_queries':0,'source_engine_calls':0,
          'input_sha256':{str(path.relative_to(P)):sha(path)}})
        print('LIVE_EXCEPTION_REPORTED_NO_FALSE_FUNDING_PASS',flush=True);return
    assert all(data[i]['D_target']==data[(i+1)%len(data)]['D_source'] for i in range(len(data)))
    K=max(v['D_source'] for v in data);cut=next(i for i,v in enumerate(data) if v['D_source']==K)
    bank=[];log=[];peak=0
    for j in range(len(mm)):
        i=(cut+j)%len(mm);m=mm[i];law=data[i];units=list(map(tuple,m['units']));dd=list(map(tuple,m['demands']))
        selected=units[:2*law['c']];fixed={d:h0[d] for d in dd if d in h0}
        assert set(fixed.values())<=set(selected)
        assert len(bank)==K-law['D_source'];peak=max(peak,len(bank)+len(selected))
        pool=[u for u in selected if u not in fixed.values()]+bank;new=[]
        for d in dd:
            if d not in fixed:
                u=pool.pop(0);h[d]=u;new.append({'demand':d,'unit':u})
        keep=K-law['D_target'];assert len(pool)>=keep
        released=pool[keep:];bank=pool[:keep]
        log.append({**law,'selected_units':selected,'fixed':list(fixed.items()),
          'new':new,'carry':bank,'released':released})
    assert not bank and peak<=10
    U={tuple(u) for m in mm for u in m['units']};DD={tuple(d) for m in mm for d in m['demands']}
    assert set(h)==DD and set(h.values())<=U and len(set(h.values()))==len(DD)==36
    assert all(h[d]==u for d,u in h0.items())
    current=read(ownpath)['full_allocation'];assert len(current)==36
    put('degree_allocator_receipt.json',{'status':'COMPLETE_NEW_SEVEN_KEY_DEGREE_SOURCE_CERTIFICATE',
      'source_queries':0,'source_engine_calls':0,'source_period':src['period'],
      'source_rows_replayed':False,'genuine_macros':len(mm),'A':src['A'],'QF':src['QF'],
      'D':'sum(max(marked_child_degree-2,0))','K_actual':K,'K_bound':4,
      'c':'min(H,3)','cut_before_macro':cut,'working_peak_selected_plus_carry':peak,'working_bound':10,
      'h':[{'demand':d,'unit':u} for d,u in sorted(h.items())],'receipt':log,
      'current_frozen_full36_unchanged':True,'current_owner_sha256':sha(ownpath),
      'new_actual_physical_owner_assignments':False,
      'input_sha256':{str(p.relative_to(P)):sha(p) for p in [path,ownpath]}})
    print('FULL36_NEW_SOURCE_COMPARISON; ORIGINAL_CURRENT_OWNERS_UNCHANGED',flush=True)
    assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:
        with (B/'audit_proof179_exit.json').open('x',encoding='utf-8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0},f)
