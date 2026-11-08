"""Only new population4 source controls, with immediate checkpoints."""
import sys,json,time,hashlib,copy,importlib.util
from pathlib import Path
from itertools import product
sys.path[:0]=['DO_RESEARCH_REBOOT/M3_POP4_RISK03','DO_RESEARCH_REBOOT/M3_UNITPAIR01','DO_RESEARCH_REBOOT/M3_OUT01','DO_RESEARCH_REBOOT/M3_GAPINT01']
# Load explicitly: UNITPAIR01 also has a module named decoder.
spec=importlib.util.spec_from_file_location('population_four_decoder',Path('DO_RESEARCH_REBOOT/M3_POP4_RISK03/candidate_decoder.py'));D=importlib.util.module_from_spec(spec);spec.loader.exec_module(D)
from proposal_factory_v2 import proposals
import interior_original as IN
import outside_original as OUT
sp=importlib.util.spec_from_file_location('independent_population_raw',Path('DO_RESEARCH_REBOOT/M3_TWOGAP_AUD01/source_audit.py'));A=importlib.util.module_from_spec(sp);sp.loader.exec_module(A)
ROOT=Path('DO_RESEARCH_REBOOT/M3_POP4_RISK03');BASE=ROOT;S=IN.S
def fullsig(v):return list(v)
def mirror(t):return S.LEAF if t[0]=='leaf' else S.node(128-t[1],mirror(t[3]),mirror(t[2]))
def decode_term(code):
    chars=iter(code)
    def read():
        c=next(chars)
        if c=='a':return None
        if c=='b':return 'G'
        return (int(c,16),read(),read())
    t=read();assert next(chars,None) is None;return t
def positions(t,p=()):
    if not isinstance(t,tuple):return []
    return positions(t[1],p+(0,))+([(p,t[0])] if t[0]==9 else [])+positions(t[2],p+(1,))
def color_and_expand(code,sig,firstpath,nonminimum,helpergap=0):
    if 'b' in code:return None
    t=decode_term(code);anons=[p for p,k in positions(t)];support=[g for g,n in enumerate(sig) if n]
    def valid(n,p,lo,hi,allowed,colors):
        if n is None:return True
        if n=='G':return lo>hi
        k,l,r=n
        if k<9:
            return lo<=k<=hi and valid(l,p+(0,),lo,k-1,{g for g in allowed if g<=k},colors) and valid(r,p+(1,),k+1,hi,{g for g in allowed if g>k},colors)
        gap=colors[p]
        return gap in allowed and lo<=gap<=hi+1 and valid(l,p+(0,),lo,gap-1,{g for g in allowed if g<=gap},colors) and valid(r,p+(1,),gap,hi,{g for g in allowed if g>=gap},colors)
    for choices in product(support,repeat=len(anons)):
        colors=dict(zip(anons,choices))
        if firstpath is not None and colors.get(tuple(firstpath))!=helpergap:continue
        if any(choices.count(g)>sig[g] for g in range(10)) or not valid(t,(),0,8,set(support),colors):continue
        assigned={};counts=[0]*10
        for p in anons:
            gap=colors[p];assigned[p]=16*gap-8+counts[gap];counts[gap]+=1
        if nonminimum and (firstpath is None or (helpergap==0 and assigned[tuple(firstpath)]<=-8) or (helpergap==9 and assigned[tuple(firstpath)]>=136+sig[9]-1)):continue
        keys=tuple(sorted([16*k for k in range(9)]+[16*g-8+j for g,n in enumerate(sig) for j in range(n)]));cuts=[]
        def fill(n,p,lo,hi,parent=None,side=None):
            available=[x for x in keys if lo<x<hi]
            if n is None:
                if parent is not None:cuts.append((parent,side))
                return S.balanced(available)
            label,left,right=n;k=16*label if label<9 else assigned[p];assert lo<k<hi
            return S.node(k,fill(left,p+(0,),lo,k,k,0),fill(right,p+(1,),k,hi,k,1))
        tree=fill(t,(),-10000,10000);assert S.inorder(tree)==list(keys)
        return tree,cuts,assigned
    return None
def main():
    global BASE
    batch=int(sys.argv[1]);manifest=json.loads((ROOT/('source_batch_'+str(batch).zfill(3)+'_cases.json')).read_text())
    BASE=ROOT/'source_audits'/('batch_'+str(batch).zfill(3));BASE.mkdir(parents=True,exist_ok=False)
    out=BASE/'source_audit.json';start=time.process_time()
    run={'completed_signatures':manifest['signatures']}
    P=D.PopulationFourCandidate();dl=IN.DAG();L=IN.build_slow(dl,'MXL');dh=IN.DAG();H=IN.build_shigh(dh,'MXH');FIN,FOUT=proposals(IN),proposals(OUT)
    rows=[];cycles=[];completed=[];seen={};source_files=[];z=S.LEAF
    def check(r,kind,require_profile=True,expected_classes=None):
        d,obj=(dl,L) if kind=='LOW' else (dh,H);e=r['environment'];digest=hashlib.sha256(json.dumps(e,sort_keys=True).encode()).hexdigest();identity=(kind,digest)
        if identity in seen:return seen[identity]
        assert set(d.vars)<=set(e)
        for name,n in d.vars.items():
            nd=d.nodes[n];v=e[name]
            if nd[1]=='bool':assert v in (False,True)
            else:
                w,sg=nd[3][2:4];assert (-(1<<(w-1))<=v<(1<<(w-1))) if sg else 0<=v<(1<<w)
        assert d.ev_ground(obj['root'],e),r['label']
        s=A.ordinary(d,e,obj['s']);t=A.ordinary(d,e,obj['t']);assert s==r['source'] and t==r['destination'];assert len(A.flat(s))==len(A.flat(t))==147
        si=P.inspect(s);ti=P.inspect(t);js,jt=si['value'],ti['value']
        if require_profile:assert si['profile_found'] and ti['profile_found'],r['label']
        if expected_classes is not None:assert (si['A'],ti['A'])==tuple(expected_classes)
        if kind=='LOW':
            nev=A.val(d,e,L['wit'].nev);hh=sum((A.val(d,e,L['wit'].evd[i])+1)//2 for i in range(nev));q=A.val(d,e,L['bt'].q)
            assert hh==r['H'] and q==r['q'] and 2*hh-q==r['w'];weight=r['w'];res=weight-P.O(t)+P.O(s);assert res>=0;m=None
        else:
            m=A.mid(d,e,H['g']);assert m==r['shared_midpoint'] and len(A.flat(m))==127
            weight=A.val(d,e,H['w1']);q=A.val(d,e,H['q']);assert weight==6-q;res=[weight-P.M(m)+P.O(s),P.M(m)-P.O(t)];assert min(res)>=0
        if s['sigma'][9]:assert not P.chi(s['b']) and not P.chi(t['b'])
        row={'label':r['label'],'kind':kind,'source':s,'destination':t,'midpoint':m,'source_potential':si,'destination_potential':ti,'weight':weight,
          'q':q,'residual':res,'original_root':True,'environment_sha256':digest,'environment':e};rows.append(row);seen[identity]=row
        # Save immediately: an interruption cannot erase an accepted root.
        name=f'root_{len(rows):03d}.json'
        with (BASE/name).open('x',encoding='utf-8') as f:json.dump(row,f,separators=(',',':'))
        source_files.append(name);assert time.process_time()-start<300,'UNKNOWN population source-family CPU cap';return row
    completed_canon=run['completed_signatures'];covered={tuple(v) for s in completed_canon for v in (s,list(reversed(s)))}
    assert completed_canon,'No finite certificates to promote'
    for index,sig in enumerate(completed_canon):
        label=''.join(map(str,sig));first=len(rows);fixture=FOUT if sig[9] or index%2 else FIN
        AA=S.node(0,z,S.node(128,S.balanced([16*k for k in range(1,8)]),z));BB=z
        for k in reversed(range(9)):BB=S.node(16*k,z,BB)
        for gap,n in enumerate(sig):
            for j in range(n):AA=IN.V.insert(AA,16*gap-8+j)
            if n:BB=IN.V.insert(BB,16*gap-8)
        _,_,r=fixture.low(dl,L,AA,BB,[(128,0)],[['K',128]],f'pop4_{label}_negative_H1',341)
        check(r,'LOW');assert r['w']==-2
        with (BASE/('source_'+label+'.json')).open('x') as f:json.dump({'status':'ORIGINAL_ROOT_PASS','sigma':sig,'root_files':source_files[first:]},f,indent=2)
        completed.append(sig)
        print(json.dumps({'new_source_canonical_controls':len(completed),'roots':len(rows),'CPU':round(time.process_time()-start,3)}),flush=True)
    selected=[]
    nonfixed=next((x for x in completed_canon if x!=list(reversed(x))),None)
    selfcase=next((x for x in completed_canon if x==list(reversed(x))),None)
    fourcase=next((x for x in completed_canon if sum(n>0 for n in x)==4),None)
    for value in (nonfixed,list(reversed(nonfixed)) if nonfixed else None,selfcase,fourcase):
        if value is not None and value not in selected:selected.append(value)
    for index,sig in enumerate(selected):
        if tuple(sig) not in covered:continue
        fixture=FOUT if sig[9] or index%2 else FIN
        core=S.node(32,S.node(0,z,S.node(16,z,z)),S.node(96,S.balanced([48,64,80]),S.balanced([112,128])));AA=core;BB=core
        for gap,n in enumerate(sig):
            for j in range(n):AA=IN.V.insert(AA,16*gap-8+j)
            if n:BB=IN.V.insert(BB,16*gap-8)
        _,Bd,low=fixture.low(dl,L,AA,BB,[(0,1),(96,0)],[['K',96]],f'pop4_{sig}_cycle_low',341)
        high=fixture.high(dh,H,Bd,32,low['destination'],low['source'],f'pop4_{sig}_cycle_high');lo=check(low,'LOW',False);hi=check(high,'HIGH',False)
        assert A.flat(lo['source'])==A.flat(hi['destination']) and A.flat(lo['destination'])==A.flat(hi['source']);assert low['w']+high['w']==8
        cycles.append({'sigma':sig,'weight':8,'full147_O_closure':True,'same127_M':True,'chi8':P.chi(lo['source']['b'])})
    # Fresh helper controls on a NEW sector; old middle/h0 controls are reused.
    helper_cases=[v for v in completed_canon if v[0] or v[9]]
    if helper_cases:
        sig=next((v for v in helper_cases if sum(n>0 for n in v)==4),helper_cases[0])
        folder=ROOT/('s'+''.join(map(str,sig)));c=json.loads((folder/'relation.json').read_text());B=P.B
        def helper_control(gap,w):
            choices={}
            for bi,row in enumerate(B['kernels'][str(gap)]):
                for x,pair in enumerate(row):
                    if pair is not None and pair[1]==w:choices.setdefault((B['trees'][bi][0],x),bi)
            for ai,opts in enumerate(c['options']):
                root=c['shadows'][ai][0][2]
                for H,x,aa,gg,fi,code in opts:
                    if H!=2 or gg!=gap:continue
                    bi=choices.get((root,x))
                    if bi is None:continue
                    word=c['families'][fi]['word'];expanded=color_and_expand(code,sig,word[0],False,gap)
                    if expanded is None:continue
                    AA,cuts,assigned=expanded
                    def scale(t):return z if t is None else S.node(16*t[0],scale(t[1]),scale(t[2]))
                    BB=scale(B['trees'][bi])
                    for g,n in enumerate(sig):
                        if n:BB=IN.V.insert(BB,16*g-8)
                    now=AA;targets=[]
                    for path in word:
                        node=now
                        for side in path:node=node[2+side]
                        targets.append(node[1]);now=S.trace(now,node[1])[0]
                    marks={x};marks.update(k for k in range(9) if len(marks)<5);mu=sum(1<<k for k in marks)
                    fixture=FOUT if sig[9] else FIN
                    _,_,r=fixture.low(dl,L,AA,BB,cuts,[['K',k] for k in targets],f'renewed_batch{batch}_{sig}_gap{gap}_w{w}',mu)
                    check(r,'LOW',expected_classes=(ai,aa));assert r['H']==2 and r['w']==w
                    return {'A':AA,'B':BB,'cuts':cuts,'targets':targets,'mu':mu}
            raise AssertionError(('new helper fixture unavailable',sig,gap,w))
        made=[]
        for gap in (0,9):
            if sig[gap]:
                for weight in (0,1):made.append(helper_control(gap,weight))
        if len(made)==2 and sig!=list(reversed(sig)):
            item=made[-1];AA=mirror(item['A']);BB=mirror(item['B']);cuts=[(128-k,1-side) for k,side in item['cuts']]
            mu=sum(1<<(8-k) for k in range(9) if item['mu']>>k&1)
            _,_,r=FOUT.low(dl,L,AA,BB,cuts,[['K',128-k] for k in item['targets']],f'renewed_batch{batch}_reflected_helper_w1',mu)
            check(r,'LOW');assert r['w']==1
    report={'status':'RENEWED_TOTAL4_SOURCE_BATCH_PASS','batch_index':batch,'completed_canonical_signatures':completed,'new_original_signatures':len(covered),
      'unique_original_roots':len(rows),'full_closed_mixed_cycles':len(cycles),'all147_O_coordinates':True,'same_actual127_M':True,
      'new_helper_controls':len(rows)-len(completed)-2*len(cycles),'inherited_middle_h0_normal_forms_reused':True,'previous_source_checks_repeated':0,'h0_correction_reused_not_replayed':True,
      'self_reflecting_canonical_controls':sum(s==list(reversed(s)) for s in completed),'DAG_nodes':[len(dl.nodes),len(dh.nodes)],
      'CPU_seconds':round(time.process_time()-start,3),'root_files':source_files,'cycles':cycles,'full_M3_proved':False}
    assert report['new_helper_controls']<=4 and len(cycles)<=4 and report['CPU_seconds']<300
    with out.open('x') as f:json.dump(report,f,indent=2)
    print(json.dumps({k:v for k,v in report.items() if k not in ('completed_canonical_signatures','root_files','cycles')},indent=2),flush=True)
if __name__=='__main__':
    err=None
    try:main()
    except BaseException as exc:
        err={'type':type(exc).__name__,'message':str(exc)};raise
    finally:
        destination=ROOT/('source_batch_'+str(int(sys.argv[1])).zfill(3)+'_exit.json')
        with destination.open('x') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':err,'source_CPU_cap':300},f,indent=2)

