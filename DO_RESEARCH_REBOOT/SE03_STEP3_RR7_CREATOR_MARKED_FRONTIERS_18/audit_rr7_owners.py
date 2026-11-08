"""Qualify the NEW original-source collision under actual sealed-CD6 owners.
Producer only; no independent allowance is used or reset.
"""
import importlib.util,json,sys,time
from pathlib import Path
B=Path(__file__).resolve().parent;P=B.parent
def mod(n,p):
    s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
p=mod('source18owners',P/'SE03_STEP2_COLD_NEG2_01/source_model.py')
L=mod('channels18owners',P/'SE03_STEP3_UNIFORM_DONOR_GROUPING_15/leaf_channels.py')
C=mod('creator18owners',P/'SE03_STEP3_SOURCE_FORCED_MULTICOMPONENT_ESCAPE_17/audit_lineage.py')
X=mod('exchange18owners',P/'SE03_STEP2_FULL_FUNDING_CLOSURE_10/physical_exchange.py')
sys.path.insert(0,str(P/'SE03_STEP2_CD6_FINAL_ASSEMBLY_14'))
from cd6_allocator import allocate
calls=0;backend_rows=0
def tr(t,x):
    global calls
    calls+=1;assert calls<100000;return p.trace(t,x)
def out(n,x):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(x,f,indent=2)
def fr(x):return tuple(fr(y) for y in x) if isinstance(x,list) else x
def pack(m):return [{'demand':d,'unit':u} for d,u in sorted(m.items())]
def one(c,erased,mirrored=False):
    global backend_rows
    R=fr(c['initial_common_tree']);word=[tuple(z) for z in c['word']];prefix=[tuple(z) for z in c['reaching_prefix']]
    initA=fr(c['initial_A']);initB=fr(c['initial_BF'])
    if mirrored:
        def mirror(t):return t if isinstance(t,str) else (14-t[0],mirror(t[2]),mirror(t[1]))
        R=mirror(R);initA=mirror(initA);initB=mirror(initB)
        word=[(m,14-x) for m,x in word];prefix=[(m,14-x) for m,x in prefix]
    E=R
    for m,x in prefix:
        if m=='K' and x!=erased:E=tr(E,x)[0]
    seen={};k=0
    while E not in seen:
        assert k<40;seen[E]=k;k+=1
        for m,x in word:
            if m=='K' and x!=erased:E=tr(E,x)[0]
    u=seen[E];mult=k-u;E0=E;base=len(prefix)+u*len(word)
    rows=[];a,b=initA,initB
    for occurrence,(m,x) in enumerate(word*mult,base+1):
        before=(a,b,E);a,pa,ea=tr(a,x);genuine=m=='K' and b[0]!=x;pb=pe='';eb=[];ee=[]
        if m=='K':b,pb,eb=tr(b,x)
        if m=='K' and x!=erased:E,pe,ee=tr(E,x)
        rows.append({'occurrence':occurrence,'mode':m,'target':x,'genuine_F':genuine,
            'A_path':pa,'BF_path':pb,'BE_path':pe,'A_events':ea,'BF_events':eb,'BE_events':ee,
            'a':len(ea),'qF':len(eb),'qE':sum(z['kind']=='DOUBLE' for z in ee),'before':before,'after':(a,b,E)})
    assert (a,b,E)==(initA,initB,E0)
    M={z['target'] for z in rows if z['genuine_F']};assert len(M)==7
    v=L.build(rows,M);aux=[]
    for t in rows:
        mode='D' if t['mode']=='K' and t['target']==erased else t['mode'];bb,aa=t['before'],t['after']
        aux.append(dict(t,mode=mode,genuine_F=mode=='K' and bb[2][0]!=t['target'],qF=t['qE'],qE=0,
            before=(bb[0],bb[2],bb[2]),after=(aa[0],aa[2],aa[2])))
    backend_rows+=len(aux);small=allocate(aux);f6=small['f'];lock={d:f6[d] for d in v['D']&set(f6)}
    old=X.exchange(v['D'],v['U'],lock,v['h0']);prior=old['allocation']
    walked=L.augment_partial(v['D'],v['U'],prior,v['h'])
    Rnat=v['D']-set(v['h0']);alpha={d:d if d in Rnat else old['blocked'][d]['owner'] for d in v['D']-set(prior)}
    deep={tuple(d) for z in v['deep'] for d in z['natural_excess']};qual=[]
    creators=C.creator_records(rows,M);hi={unit:d for d,unit in v['h'].items()}
    for path in walked['paths']:
        root=tuple(path['root']);f=path['frontier']
        if f is None or alpha[root] not in deep:continue
        f=tuple(f);m=next(m for m in v['macros'] if f[0] in m['occurrences'])
        positive=[(i,t) for i,t in enumerate(rows) if t['occurrence'] in m['occurrences'] and t['a']]
        if (m['H'],m['Q'],len(m['branch']),m['z'])!=(1,2,2,1) or len(positive)!=1:continue
        i,t=positive[0]
        if t['A_path'] not in ('RR','LL'):continue
        par=C.parents(t['before'][0])[m['target']]
        if par in M:continue
        edge=(par,m['target']);cs=[z for z in creators if tuple(z['edge'])==edge and z['row_index']<i]
        creator=max(cs,key=lambda z:z['row_index']) if cs else max((z for z in creators if tuple(z['edge'])==edge),key=lambda z:z['row_index'])
        unit=tuple(creator['unit'])
        if unit in hi:
            qual.append({'root':root,'deep_anchor':alpha[root],'first_undefined_frontier':f,'owner_path':path,
                'positive_A_row':t['occurrence'],'A_orientation':t['A_path'],'creator':creator,
                'creator_unit':unit,'existing_comparison_preimage':hi[unit]})
    return {'erased':erased,'mirrored':mirrored,'word':word,'reaching_prefix':prefix,'common_initial':R,
        'initial_A':initA,'initial_BF':initB,'initial_BE_at_recurrence':E0,
        'u':u,'L':mult,'base':base,'actual_interval':[base+1,base+len(rows)],'rows':rows,
        'auxiliary_rows':aux,'six_key_core':small['core'],'f6':pack(f6),'locked_common':pack(lock),
        'prior':pack(prior),'leaf_comparison':pack(v['h']),'natural_h0':pack(v['h0']),
        'deep_packets':v['deep'],'branch_frontiers':sorted(v['R']),
        'actual_A_BF_BE_closed':True,'all_original_owner_values_unchanged':True,
        'qualifying_RR7_collisions':qual,'partial_owner_paths':walked['paths']}
def main():
    c=json.loads((B/'rr7_source_candidate.json').read_text());reports=[];found=None
    for z in (13,5,1,3,7,9,11):
        r=one(c,z);reports.append(r)
        print(json.dumps({'erased':z,'u':r['u'],'L':r['L'],'core6':r['six_key_core'],
            'qualifying_collisions':len(r['qualifying_RR7_collisions'])}),flush=True)
        if r['qualifying_RR7_collisions']:found=r;break
    if found:
        mirrored=one(c,14-found['erased'],True);reports.append(mirrored)
    status='FULL_SOURCE_RR7_CANDIDATE_REFUTED_PRODUCER_AUDIT_PENDING' if found else 'PACKET_COLLISION_ONLY_FULL_RR7_QUALIFICATION_NOT_FOUND'
    out('rr7_owner_certificates.json',{'status':status,'reports':reports,'source_engine_calls':calls,
        'backend_source_rows_supplied':backend_rows,'independent_audit':'PENDING_SEPARATE_CAP',
        'does_not_refute_Universal_CD':True})
    print(json.dumps({'status':status,'queries':calls,'backend_rows':backend_rows,
        'qualifying':[{'erased':r['erased'],'mirror':r['mirrored'],'collisions':r['qualifying_RR7_collisions']} for r in reports if r['qualifying_RR7_collisions']]}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_rr7_owners_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,
        'source_engine_calls':calls,'backend_source_rows_supplied':backend_rows,'new_finite_tests':0,'old_semantic_rows_replayed':0})
