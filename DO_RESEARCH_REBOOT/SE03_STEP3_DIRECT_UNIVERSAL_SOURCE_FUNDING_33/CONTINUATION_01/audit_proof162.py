"""Course correction: actual H2 donor/owner ledger, not another geometry test."""
import hashlib,importlib.util,json,sys,time
from pathlib import Path
from interior_projection_source_tools import fr,isnode,normalize,known
B=Path(__file__).resolve().parent;P=B.parent.parent;C=B/'DIRTY_OWNER_COURSE_CORRECTION';START=time.process_time();CAP=float(sys.argv[1])
def out(n,z):
    with (C/n).open('x') as f:json.dump(z,f,indent=2)
def pack(m):return [{'demand':d,'unit':u} for d,u in sorted(m.items())]
def main():
    z=json.loads((B/'retirement_preimage_closed_source.json').read_text());Z=json.loads((B/'native10_source_actions.json').read_text());T=list(map(fr,Z['trees']));idx={t:i for i,t in enumerate(T)};word=z['word'];arows=z['A_word_source_rows'];initial=fr(z['initial_common_A_B_BE']);physical=sorted(known(initial));rank={k:i+1 for i,k in enumerate(physical)}
    def fullnorm(t):
        def walk(v,hi):return 'F'+str(hi) if not isnode(v) else (v[0],walk(v[1],rank[v[0]]-1),walk(v[2],hi))
        return walk(t,len(physical))
    def erasep(t):
        if not isnode(t):return t
        if t[0]==5:assert not isnode(t[1]) and not isnode(t[2]);return 'E'
        return t[0],erasep(t[1]),erasep(t[2])
    core=idx[normalize(erasep(initial),{k:k//2 for k in known(initial) if k!=5})]
    def embed(b):
        def bind(t):
            if not isnode(t):return (5,'E','E') if t=='F2' else t
            return 2*t[0],bind(t[1]),bind(t[2])
        return fullnorm(bind(T[b]))
    assert embed(core)==initial
    states={k:core for k in range(6,11)};charts={k:() for k in states};seen={};copies=[];copy=0;instances=0
    def state():return tuple((states[k],charts[k]) for k in range(6,11))
    while state() not in seen:
        if copy>=64 or time.process_time()-START>CAP-3:raise TimeoutError('JOINT_SOURCE_ALIGNMENT_CAP')
        seen[state()]=copy;rows=[];old=state()
        for j,(kind,key) in enumerate(word):
            views={}
            for k in range(6,11):
                before=states[k];prior=charts[k];q=0;genuine=False
                if kind=='K' and key//2<=k:
                    assert key%2==0;x=key//2;genuine=T[before][0]!=x;q=Z['Q'][before][x-1];states[k]=Z['destination'][before][x-1];instances+=1
                    if genuine:charts[k]=(x,)+tuple(v for v in prior if v!=x)
                views[k]={'B_before':before,'B_after':states[k],'Q':q,'genuine':genuine,'chart_before':prior,'chart_after':charts[k]}
            rows.append({'occurrence':copy*len(word)+j+1,'word_index':j,'original_kind':kind,'target':key,'a':arows[j]['H'],'A_before':arows[j]['before'],'A_after':arows[j]['after'],'views':views})
        copies.append({'start':old,'end':state(),'rows':rows});copy+=1
    u=seen[state()];L=copy-u;assert u>=1;rows=sum((v['rows'] for v in copies[u:u+L]),[]);period=(rows[0]['occurrence'],rows[-1]['occurrence']);assert copies[u]['start']==copies[u+L-1]['end']
    sys.path.insert(0,str(P/'SE03_STEP2_CD6_FINAL_ASSEMBLY_14'));from cd6_allocator import allocate
    from source_funding import own_map,with_owners
    per={};solvency={}
    for k in range(6,11):
        rr=[]
        for row in rows:
            v=row['views'][k];mode=row['original_kind'] if row['original_kind']!='K' or row['target']//2<=k else 'D';bb=embed(v['B_before']);ba=embed(v['B_after'])
            rr.append({'occurrence':row['occurrence'],'original_kind':row['original_kind'],'mode':mode,'target':row['target'],'a':row['a'],'qF':v['Q'],'qE':0,'genuine_F':v['genuine'],'before':(fr(row['A_before']),bb,bb),'after':(fr(row['A_after']),ba,ba)})
        per[k]=rr;v=own_map(rr);solvency[k]={'D':len(v['D']),'U':len(v['U']),'h0_pairs':len(v['h0']),'natural_excess':sorted(v['R']),'macros':[{'H':m['H'],'Q':m['Q'],'occurrences':m['occurrences'],'unit_count':len(m['units']),'slack':2*m['H']-m['Q']} for m in v['macros']]}
    base=allocate(per[6]);assert base['core']==6;f=base['f'];domain=base['D'];stages=[];complete=True;last=None
    for k in range(7,11):
        v=own_map(per[k])
        if v['R']:
            complete=False;stages.append({'support':k,'status':'NO_DIRECT_OWN_LICENSE','natural_excess':sorted(v['R'])});break
        v['h']=dict(v['h0']);owner=with_owners(v,domain,f);g=owner['extension']['allocation'];locked={d:f[d] for d in v['D']&domain};assert all(g[d]==u for d,u in locked.items())
        stages.append({'support':k,'status':'ACTUAL_NORMALIZED_DIRECT_OWN_EXTENSION','smaller_input':pack(f),'smaller_demand_domain':sorted(domain),'common_locked':pack(locked),'independent_h0':pack(v['h0']),'old_natural_effective_prior':pack(owner['prior']['allocation']),'unpaid_after_natural':sorted(v['D']-set(owner['prior']['allocation'])),'complete_normalized_f':pack(g),'licensed_paths':owner['licensed']['paths'],'all_common_old_values_preserved':True,'independent_working_scope':'original static within-macro own funding; uniform event-wise schedule proof required, not endpoint storage'});f=g;domain=v['D'];last=(v,owner,locked)
    packet=None
    if complete:
        t=next(row['occurrence'] for row in rows if row['word_index']==(z['packet_absolute_t']-1)%len(word));pr=next(row for row in rows if row['occurrence']==t);v,owner,locked=last;invold={u:d for d,u in locked.items()};invprev={tuple(q['unit']):tuple(q['demand']) for q in stages[-1]['smaller_input']};invnat={u:d for d,u in v['h0'].items()};invfinal={u:d for d,u in f.items()};pathby={q['root']:q for q in owner['licensed']['paths']}
        dd=[(t,k) for k in range(1,pr['views'][10]['Q']+1)];bits=[(t,j,b) for j in range(1,pr['a']+1) for b in (0,1)]
        packet={'occurrence':t,'H':pr['a'],'Q_full':pr['views'][10]['Q'],'Q_aux9':pr['views'][9]['Q'],'demands':[{'demand':d,'is_common':d in locked,'old_common_unit':locked.get(d),'natural_unit':v['h0'].get(d),'final_unit':f[d],'licensed_path':pathby.get(d)} for d in dd],'actual_event_bits':[{'unit':u,'old_aux9_owner':invprev.get(u),'protected_common_owner':invold.get(u),'natural_h0_reservation':invnat.get(u),'final_full_owner':invfinal.get(u)} for u in bits],'residual_after_natural':sorted(v['D']-set(owner['prior']['allocation']))}
    assert time.process_time()-START<CAP-1
    files=('retirement_preimage_closed_source.json','retirement_boundary_independent_audit.json','native10_source_independent_audit.json')
    out('H2_actual_owner_candidate.json',{'status':'PRODUCER_ACTUAL_H2_NORMALIZED_OWNER_LINEAGE' if complete else 'H2_OWNER_LINEAGE_STOPS_AT_MISSING_SOURCE_LICENSE','joint_source_prefix_copies':u,'joint_period_copies':L,'joint_period':period,'same_as_accepted_H2_period':list(period)==z['period'],'all_source_rows':rows,'solvency_by_support':solvency,'base6':{'core':base['core'],'marks':sorted(base['marks']),'f':pack(base['f']),'D':sorted(base['D']),'working_bound':base['working_bound']},'stages':stages,'normalization_complete':complete,'H2_packet_owner_ledger':packet,'source_kernel_instances':instances,'source_queries':0,'source_engine_calls':0,'no_existing_owner_receipt_overwritten':True,'principal_U33':'OPEN','input_sha256':{n:hashlib.sha256((B/n).read_bytes()).hexdigest() for n in files}})
    print(json.dumps({'status':'H2_ACTUAL_OWNER_INSPECTION','period':period,'complete':complete,'solvency':{k:{x:val[x] for x in ('D','h0_pairs','natural_excess')} for k,val in solvency.items()},'packet':packet}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:
        with (B/'audit_proof162_exit.json').open('x') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0},f)
