"""Bounded deterministic SHARP-01 corpus, physical incidence and exact dual tests."""
from collections import defaultdict, deque, Counter
from fractions import Fraction
from itertools import combinations
from pathlib import Path
import hashlib,json,os,random,subprocess,time,ctypes
from sharp01_oracle import replay,Tree,plain_splay,vine,digest,VERSION
import sharp01_sources as src

BASE=Path(__file__).resolve().parent
REPO=BASE.parents[1]
SEED=20261110

def write(path,obj):
    path.write_text(json.dumps(obj,separators=(',',':')),encoding='utf-8')

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def corpus():
    ans=[src.H(p) for p in range(1,7)]+[src.H(3,2),src.H(5,2)]
    ans += [src.W(p,hit=hit) for p in (2,3,4,5) for hit in (None,3)]
    w5=src.W(3,hit=5); w5.update(name='W_5',family='W_5'); ans.append(w5)
    ans += [src.W_star(),src.H_dec()]
    ans += [src.G(4,L=31,r=r) for r in (1,3,8)]
    ans += [src.G(5,L=L,r=3) for L in (11,17,31)]
    ans += [src.G(6,L=31,r=2)]
    ans += [src.lifted_H(p,r=2) for p in (2,3,4)]
    ans += [src.I_m_Z(r) for r in (1,3,5)]
    ans += [src.warm_local(),src.warm_marked(3),src.warm_marked(5)]
    ans += src.campaign15()
    # Independent complete perturbations: common diagonal + arbitrary preparation
    # and KEEP pattern + FULL increasing/reverse synchronization, all paid.
    rng=random.Random(SEED)
    for n in (7,9,13,21,33):
        for j in range(3):
            prefix=[[('K' if rng.randrange(4) else 'D'),rng.randrange(1,n+1)] for _ in range(4*n)]
            word=prefix+src.ops('K',range(1,n+1))+src.ops('K',range(n-1,0,-1))
            ans.append(src.source(f'perturb_{n}_{j}',n,word,family='controlled_random',seed=SEED))
    # Recurrent words expose legitimate periods without charging their warm-up.
    for n in (9,13,21,33):
        word=[['K' if rng.randrange(3) else 'D',rng.randrange(1,n+1)] for _ in range(3*n)]
        a,b=Tree(vine(range(1,n+1))),Tree(vine(range(1,n+1)))
        seen={}; history=[]
        for i in range(64):
            key=digest([a.state(),b.state()])
            if key in seen:
                u=seen[key]; L=i-u
                ans.append({'name':f'warmed_random_{n}','family':'warmed_random','initial_A':a.state(),'initial_B':b.state(),
                            'operations':word*L,'diagonal_initial':vine(range(1,n+1)),
                            'reaching_prefix':word*u,'orbit_preperiod':u,'orbit_period':L,'seed':SEED})
                break
            seen[key]=i;history.append(key)
            for tag,x in word:
                plain_splay(a,x)
                if tag=='K':plain_splay(b,x)
        else:raise AssertionError('bounded recurrent construction did not close')
    # Reflect a representative of EVERY mandatory physical family.
    names=['H_6_1','W_5','W_star','H_dec','G_4_1_L31_r1_z1','lifted_H_4_1_r2','I^3Z','warm_marked_5_1_r3']
    chosen=[s for s in ans if s['name'] in names]
    chosen += [s for s in ans if s['name'].startswith('C15_') and 'mirrorFalse' in s['name']][:2]
    ans += [src.reflect(s) for s in chosen]
    for name in ('H_6_1','G_4_1_L31_r1_z1','C15_zero_r7_mirrorFalse'):
        s=next(s for s in ans if s['name']==name)
        ans.append({**s,'name':name+'_copies3','family':s['family']+'_copies','operations':s['operations']*3})
    ans += [src.source('empty',0,[]),src.source('root_identity',1,[['K',1],['D',1],['K',1]]),
            src.source('no_KEEP',3,[['D',3],['D',2],['D',1]]),
            src.source('one_KEEP',3,[['K',1],['D',3],['D',2],['D',1]])]
    assert len(ans)<=220 and len({s['name'] for s in ans})==len(ans)
    assert all(len(s['initial_A']['children'])<=600 and len(s['operations'])<=20000 for s in ans)
    return ans

def flow(demands,capacities,adj):
    # Integral augmenting paths. Nodes have original gap identities.
    S=('s',0);T=('t',0); graph=defaultdict(dict)
    def edge(u,v,c):graph[u][v]=c;graph[v].setdefault(u,0)
    for i,u in demands.items():
        edge(S,('u',i),u)
        for j in adj.get(i,[]):edge(('u',i),('c',j),sum(demands.values())+1)
    for j,c in capacities.items():edge(('c',j),T,c)
    total=0
    while True:
        parent={S:None};todo=deque([S])
        while todo and T not in parent:
            u=todo.popleft()
            for v,c in graph[u].items():
                if c>0 and v not in parent:parent[v]=u;todo.append(v)
        if T not in parent:break
        z=T;amt=10**18
        while parent[z] is not None:amt=min(amt,graph[parent[z]][z]);z=parent[z]
        z=T
        while parent[z] is not None:
            u=parent[z];graph[u][z]-=amt;graph[z][u]+=amt;z=u
        total+=amt
    reached=set(parent);deficient=[i for i in demands if ('u',i) in reached]
    assignment=[[i,j,graph[('c',j)].get(('u',i),0)] for i in demands for j in adj.get(i,[]) if graph[('c',j)].get(('u',i),0)]
    return total,deficient,assignment

def deficiency(ds,demands,capacities,adj):
    near={j for i in ds for j in adj.get(i,[])}
    return sum(demands[i] for i in ds)-sum(capacities[j] for j in near)

def incidence(led):
    gaps=led['gaps'];events=led['events']; ops=led['operations']
    byop=defaultdict(list);added=defaultdict(list);lost=defaultdict(list)
    for epos,e in enumerate(events):
        byop[e['id'][1]].append((epos,e))
        for field,dest in (('ancestry_added',added),('ancestry_removed',lost)):
            y,xx=e[field]
            for x in xx:dest[(e['id'][0],y,x)].append(epos)
    donors={g['gap_index']:g['c'] for g in gaps if g['c']}
    demands={g['gap_index']:g['u'] for g in gaps if g['u']}
    event_gap={op:g['gap_index'] for g in gaps for op in g['operation_ids']}
    gap_touches={g['gap_index']:{z for op in g['operation_ids'] for _,e in byop[op] if e['id'][0]=='A' for z in (e['pivot'],e['promoted'])} for g in gaps}
    graphs={k:{} for k in ('shared_endpoints','A_recreation','first_A_recreation','same_target')}
    histories=[]
    for g in gaps:
        if not g['u']:continue
        i=g['gap_index'];x=g['target'];ys=g['B_only_ancestors'];keep=g['KEEP_operation_id']
        start=ops[g['previous_KEEP_operation_id']-1]['event_range'][1]
        end=ops[keep-1]['event_range'][1]
        recreation=set();firsts=set();details=[]
        def previous(key,idx):
            vv=lost.get(key,[]);return max((v for v in vv if v<idx),default=vv[-1] if vv else None)
        def next_one(key,idx):
            vv=added.get(key,[]);return min((v for v in vv if v>=idx),default=vv[0] if vv else None)
        for y in ys:
            for ep in added.get(('A',y,x),[]):recreation.add(event_gap[events[ep]['id'][1]])
            ae=next_one(('A',y,x),end);be=next_one(('B',y,x),end);al=previous(('A',y,x),start)
            if ae is not None:firsts.add(event_gap[events[ae]['id'][1]])
            details.append({'B_only_ancestor':y,'last_A_loss_before_gap':None if al is None else events[al]['id'],
                            'first_A_recreation_after_KEEP':None if ae is None else events[ae]['id'],
                            'first_B_recreation_after_KEEP':None if be is None else events[be]['id']})
        eligible={
            'shared_endpoints':{j for j in donors if gap_touches[j]&({x}|set(ys))},
            'A_recreation':recreation&donors.keys(),
            'first_A_recreation':firsts&donors.keys(),
            'same_target':{h['gap_index'] for h in gaps if h['c'] and h['target']==x}}
        for rule,js in eligible.items():graphs[rule][i]=sorted(js)
        current_B=[e for _,e in byop[keep] if e['id'][0]=='B']
        histories.append({'gap_index':i,'KEEP_operation_id':keep,'target':x,'u':g['u'],'c':g['c'],'d':g['d'],
                          'B_only_ancestor_histories':details,
                          'B_edges_removed_in_hit':[{'id':e['id'],'edges':e['edges_removed'],'middle':e['middle']} for e in current_B],
                          'A_DELETE_rotations_in_gap':[e['id'] for op in g['DELETE_operation_ids'] for _,e in byop[op] if e['id'][0]=='A'],
                          'eligibility':{rule:sorted(js) for rule,js in eligible.items()}})
    results={}
    for rule,adj in graphs.items():
        total,ds,assignment=flow(demands,donors,adj)
        minimum=True
        if total<sum(demands.values()):
            if len(demands)<=16:
                found=False
                for size in range(1,len(demands)+1):
                    for subset in combinations(demands,size):
                        if deficiency(subset,demands,donors,adj)>0:ds=list(subset);found=True;break
                    if found:break
            else:
                minimum=False
                for i in list(ds):
                    trial=[j for j in ds if j!=i]
                    if deficiency(trial,demands,donors,adj)>0:ds=trial
            assert ds and deficiency(ds,demands,donors,adj)>0
        near=sorted({j for i in ds for j in adj.get(i,[])})
        results[rule]={'demand':sum(demands.values()),'flow':total,'success':total==sum(demands.values()),
                       'edges':adj,'assignment':assignment,'deficient_subset':ds,'neighbor_capacity_gaps':near,
                       'Hall_deficiency':deficiency(ds,demands,donors,adj) if ds else 0,
                       'minimum_cardinality_subset':minimum if ds else None,
                       'maximum_demands_eligible_at_one_gap':max([0]+[sum(j in js for js in adj.values()) for j in donors])}
    return {'rules':results,'positive_gap_histories':histories}

def potential_update(candidates,led):
    for g in led['gaps']:
        for name in g.get('Phi_start',{}):
            z=candidates.setdefault(name,{'lower':Fraction(0),'upper':None,'lower_witness':None,'upper_witness':None,'zero_obstruction':None,'unscaled_first_failure':None})
            delta=g['Phi_start'][name]-g['Phi_end'][name];d=g['d']
            w={'source':led['summary']['name'],'gap_index':g['gap_index'],'KEEP_operation_id':g['KEEP_operation_id'],
               'd':d,'Phi_start':g['Phi_start'][name],'Phi_end':g['Phi_end'][name],'delta':delta,'H':g['H'],'p':g['p'],'q':g['q']}
            if d>delta and z['unscaled_first_failure'] is None:z['unscaled_first_failure']=w
            if delta==0 and d>0 and z['zero_obstruction'] is None:z['zero_obstruction']=w
            if delta>0:
                ratio=Fraction(d,delta)
                if ratio>z['lower']:z['lower']=ratio;z['lower_witness']=w
            if delta<0:
                ratio=Fraction(d,delta)
                if z['upper'] is None or ratio<z['upper']:z['upper']=ratio;z['upper_witness']=w

def pins():
    paths=list((REPO/'DO_RESEARCH_REBOOT').glob('IAGS12_*.md'))
    paths += [REPO/'DO_RESEARCH_REBOOT'/n for n in ('RESEARCH_RULES.md','RG01_PRIMITIVE_ACCOUNTING.md','RG04_GLOBAL_REGENERATION.md',
        'ROUTE02_ROUTE04_UNIVERSAL_SOURCE_WORK_20261109/UNIVERSAL_INTERIOR_SOURCE_WORK_PROOF_OR_REFUTATION.md',
        'ROUTE02_ROUTE04_REGENERATION_CONTINUATION_20261109/UNIVERSAL_INTERIOR_SOURCE_WORK_REGENERATION_CONTINUATION.md',
        'ROUTE02_ROUTE04_TF2_AUDIT_AMPLIFICATION_20261109/TF2_INDEPENDENT_AUDIT_AND_PARAMETRIC_AMPLIFICATION.md',
        '06_CERTIFICATES/DIRECT_U4_PARALLEL_RESEARCH/run_20261030_v001/U4_02_ORIGINAL_PAIR_ACCESS_SPEC.md',
        'SE03_STEP3_RECURSIVE_SOURCE_CLOSURE_35/ND35_COMPLEMENT_08/SOURCE_SPEC.md',
        'SE03_STEP2_CD6_FINAL_ASSEMBLY_14/CD6_THEOREM.md','SE03_STEP2_CD6_FINAL_ASSEMBLY_14/CD6_FINAL_CERTIFICATE.json',
        'SE03_STEP3_UNIFORM_DONOR_GROUPING_15/ZERO_RUN_FAMILY_THEOREM.md',
        'SE03_STEP3_UNIFORM_DONOR_GROUPING_15/UNIFORM_LEAF_CHANNEL_THEOREM.md',
        'SE03_STEP3_UNIFORM_DONOR_GROUPING_15/AUDIT_CAP_CHECKPOINT.md',
        'SE03_STEP3_UNIFORM_DONOR_GROUPING_15/leaf_source_certificates2.json',
        'SE03_STEP3_UNIFORM_DONOR_GROUPING_15/zero_run_source_certificates.json',
        'EXP01_PHYSICAL_RESIDUAL_DISCOVERY/exp01_sources.py')]
    paths += [REPO/'python/independent/splay.py']
    return {str(p.relative_to(REPO)).replace('\\','/'):sha(p) for p in paths if p.exists()}

def main():
    start=time.process_time();wall=time.perf_counter();pin=pins()
    assert subprocess.check_output(['git','branch','--show-current'],cwd=REPO,text=True).strip()=='coarse-double-branch'
    manifest={'implementation':VERSION,'seed':SEED,'commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=REPO,text=True).strip(),
              'input_sha256':pin,'source_completeness':'explicit finite corpus; no exhaustive all-source claim',
              'resource_ceiling_cpu_seconds':600,'historical_resource_records':'read only; no C15 seal/controller invoked'}
    write(BASE/'SHARP01_INPUT_MANIFEST.json',manifest)
    sources=corpus();write(BASE/'SHARP01_SOURCE_WITNESSES.json',{'implementation':VERSION,'seed':SEED,'sources':sources})
    (BASE/'ledgers').mkdir(exist_ok=True); summaries=[];index=[];incs=[];candidates={}
    for k,s in enumerate(sources):
        led=replay(s);sm=led['summary'];summaries.append(sm)
        name=f'ledgers/source_{k:03d}.json';write(BASE/name,led)
        index.append({'name':s['name'],'path':name,'sha256':sha(BASE/name)})
        incs.append({'source':s['name'],**incidence(led)})
        potential_update(candidates,led)
        print(json.dumps({'source':s['name'],'A':sm['A'],'Q':sm['Q'],'U':sm['U'],'C':sm['C'],'Delta':sm['Delta']}),flush=True)
        if sm['Delta']>0:
            from sharp01_validate import validate
            validate(s,led);write(BASE/'SHARP01_POSITIVE_COUNTEREXAMPLE.json',led)
            raise RuntimeError('INDEPENDENTLY CONFIRMED SHARP COUNTEREXAMPLE; STOP')
        assert time.process_time()-start<600,'new SHARP measurement CPU cap'
    for z in candidates.values():
        z['nonnegative_scalar_feasible']=z['zero_obstruction'] is None and (z['upper'] is None or z['lower']<=z['upper'])
        z['lower']=str(z['lower']);z['upper']=None if z['upper'] is None else str(z['upper'])
    changed={rel:{'before':h,'after':sha(REPO/rel)} for rel,h in pin.items() if sha(REPO/rel)!=h}
    assert not any('certificates2.json' in rel or 'zero_run_source_certificates.json' in rel or 'python/independent/' in rel for rel in changed),changed
    # EXP01 is a provenance-only original. This run imports the isolated snapshot.
    manifest['concurrent_provenance_changes']=changed
    manifest['executed_source_constructor_sha256']=sha(BASE/'sharp01_sources.py')
    write(BASE/'SHARP01_INPUT_MANIFEST.json',manifest)
    write(BASE/'SHARP01_GAP_LEDGER.json',{'state_reference_format':'Each per-source states table resolves every complete tree reference; operations/steps/events provide all original IDs.',
                                       'no_KEEP_case':'empty gap list; A is unpartitioned and Q=0; no artificial gap', 'ledgers':index})
    write(BASE/'SHARP01_RESULTS.json',{'sources':summaries,'potential_templates':candidates,'incidence':incs})
    result={'status':'PASS_FINITE_CORPUS','sources':len(sources),'operations':sum(s['operations'] for s in summaries),
            'cpu_seconds':time.process_time()-start,'wall_seconds':time.perf_counter()-wall,
            'peak_working_set_bytes':None,'max_n':max(s['n'] for s in summaries),'positive_source_deficits':0}
    if os.name=='nt':
        class PMC(ctypes.Structure):
            _fields_=[('cb',ctypes.c_ulong),('PageFaultCount',ctypes.c_ulong)]+[(n,ctypes.c_size_t) for n in ('PeakWorkingSetSize','WorkingSetSize','QuotaPeakPagedPoolUsage','QuotaPagedPoolUsage','QuotaPeakNonPagedPoolUsage','QuotaNonPagedPoolUsage','PagefileUsage','PeakPagefileUsage')]
        pm=PMC();pm.cb=ctypes.sizeof(pm)
        from ctypes import wintypes
        ctypes.windll.kernel32.GetCurrentProcess.restype=wintypes.HANDLE
        ctypes.windll.psapi.GetProcessMemoryInfo.argtypes=[wintypes.HANDLE,ctypes.POINTER(PMC),wintypes.DWORD]
        ctypes.windll.psapi.GetProcessMemoryInfo.restype=wintypes.BOOL
        assert ctypes.windll.psapi.GetProcessMemoryInfo(ctypes.windll.kernel32.GetCurrentProcess(),ctypes.byref(pm),pm.cb)
        result['peak_working_set_bytes']=pm.PeakWorkingSetSize
        assert pm.PeakWorkingSetSize<1024**3
    write(BASE/'SHARP01_RUN_RECEIPT.json',result);print(json.dumps(result))

if __name__=='__main__':
    started_cpu=time.process_time();started_wall=time.perf_counter();outcome='FAILED'
    try:
        main();outcome='COMPLETED'
    finally:
        # Persist usage even if a source/pin assertion fails on reproduction.
        write(BASE/'SHARP01_PROCESS_EXIT_RECEIPT.json',{'status':outcome,'cpu_seconds':time.process_time()-started_cpu,
                                                       'wall_seconds':time.perf_counter()-started_wall})
