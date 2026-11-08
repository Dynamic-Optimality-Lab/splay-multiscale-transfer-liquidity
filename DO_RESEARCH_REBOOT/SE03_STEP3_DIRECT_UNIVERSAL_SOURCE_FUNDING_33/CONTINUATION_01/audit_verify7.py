"""Independent physical event transposition and natural-owner check."""
import json,time,sys,importlib.util,hashlib
from pathlib import Path
B=Path(__file__).resolve().parent;P=B.parent.parent;CAP=float(sys.argv[1]);QCAP=int(sys.argv[2]);START=time.process_time();queries=0
def rd(p):return json.loads(p.read_text())
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def fr(v):return tuple(map(fr,v)) if isinstance(v,list) else v
def main():
    global queries
    source=rd(B/'unary_projection_source_countercertificate.json');checked=rd(B/'unary_projection_independent_audit.json');z=rd(B/'unary_projection_physical_repair_map.json');assert checked['status']=='PASS_CLOSED_SOURCE_AND_UNARY_PROJECTION_COST_GAP'
    assert hashlib.sha256((B/'unary_projection_source_countercertificate.json').read_bytes()).hexdigest()==checked['input_sha256']['unary_projection_source_countercertificate.json']
    sp=importlib.util.spec_from_file_location('independent_unary_repair33',P/'SE03_STEP3_GUARDED_E4_REALIZABILITY_27/CONTINUATION_01/audit_independent2.py');I=importlib.util.module_from_spec(sp);sp.loader.exec_module(I)
    def tick():
        global queries
        if queries>=QCAP or time.process_time()-START>CAP-3:raise TimeoutError('INDEPENDENT_REPAIR_CAP')
        queries+=1
    I.tick=tick
    def shape(tree):
        def walk(v,lo,hi):return 'F'+str(hi) if v is None else (v.key,walk(v.left,lo,v.key-1),walk(v.right,v.key+1,hi))
        return walk(tree.root,1,9)
    A=I.Tree(fr(z['native_initial']));F=I.Tree(fr(z['native_initial']));rows=[];physical={r['occurrence']:r for r in source['rows']}
    for nt,(mode,x) in enumerate(z['native_word'],1):
        assert z['native_rows'][nt-1]['mode']==mode and z['native_rows'][nt-1]['target']==x;pt=z['native_rows'][nt-1]['physical_boundary_reference'];before=(shape(A),shape(F));pa,ea=A.access(x);pb='';eb=[]
        if mode=='K':pb,eb=F.access(x)
        q=sum(e['kind']=='DOUBLE' for e in eb);assert (len(ea),q)==(z['native_rows'][nt-1]['a'],z['native_rows'][nt-1]['q'])
        rows.append({'occurrence':nt,'mode':mode,'a':len(ea),'qF':q,'genuine_F':mode=='K' and before[1][0]!=x,'physical':pt})
        if mode=='K':assert physical[pt]['mode']=='K' and q==physical[pt]['qF']
    assert shape(A)==shape(F)==fr(z['native_initial']) and sum(r['a'] for r in rows)==29
    maps={tuple(v['native']):tuple(v['physical']) for v in z['bit_map']};dm={tuple(v['native']):tuple(v['physical']) for v in z['demand_map']}
    V={(r['occurrence'],j,b) for r in rows for j in range(1,r['a']+1) for b in (0,1)};U={(r['occurrence'],j,b) for r in source['rows'] for j in range(1,r['a']+1) for b in (0,1)}
    assert set(maps)==V and len(set(maps.values()))==len(maps) and set(maps.values())<=U and U-set(maps.values())=={(9,2,0),(9,2,1)}
    def own(rows):
        ends=[i for i,r in enumerate(rows) if r['genuine_F']];ans={}
        for j,end in enumerate(ends):
            p=ends[j-1];seg=rows[p+1:end+1] if p<end else rows[p+1:]+rows[:end+1];dd=[(r['occurrence'],k) for r in seg for k in range(1,r['qF']+1)];uu=[(r['occurrence'],i,b) for r in seg for i in range(1,r['a']+1) for b in (0,1)];ans.update(zip(dd,uu))
        return ans
    native=own(rows);old=own(source['rows']);assert len(native)==len(old)==2 and all(maps[u]==old[dm[d]] for d,u in native.items())
    vevents=[(r['occurrence'],j) for r in rows for j in range(1,r['a']+1)];event_map={e:maps[e+(0,)][:2] for e in vevents}
    assert all(maps[e+(1,)]==event_map[e]+(1,) for e in vevents)
    pending=set();i=0;peak=0;reserve_peak=0;emitted=[]
    for r in source['rows']:
        for j in range(1,r['a']+1):
            ev=(r['occurrence'],j)
            if ev not in event_map.values():continue
            pending.add(ev);peak=max(peak,2*len(pending))
            while i<len(vevents) and event_map[vevents[i]] in pending:
                pending.remove(event_map[vevents[i]]);emitted.append(vevents[i]);i+=1
            reserve_peak=max(reserve_peak,2*len(pending))
    assert emitted==vevents and not pending and peak==4 and reserve_peak==2
    assert rd(B/'native9_sparse_independent_audit.json')['status']=='PASS_COMPLETE_NINE_ANCHOR_SOURCE_CERTIFICATE'
    result={'status':'PASS_SOURCE_EXACT_UNARY_FAMILY_REPAIR_AND_H0_TRANSPORT','original_A':30,'native_A':29,'native_bits':len(V),'actual_physical_bits':len(U),'unused_original_bits':sorted(U-set(maps.values())),'native_original_Q':2,'all_original_h0_owners_preserved':True,'extra_repair_reserve':reserve_peak,'raw_transposition_with_current_input':peak,'native_working_bound':8,'transported_sufficient_working_bound':10,'arbitrary_repetition_noncollision':'disjoint original occurrence copies; empty repair reserve at every returning block boundary','scope':'the specified source-uniform family; no arbitrary anonymous-helper decomposition asserted','principal_U33':'OPEN','new_source_queries':queries,'external_or_formal_verification':False,'input_sha256':{n:hashlib.sha256((B/n).read_bytes()).hexdigest() for n in ('UNARY_SOURCE_REPAIR_THEOREM.md','unary_projection_physical_repair_map.json')}}
    out('unary_source_repair_independent_audit.json',result);print(json.dumps(result))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_verify7_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':queries,'source_engine_calls':queries})
