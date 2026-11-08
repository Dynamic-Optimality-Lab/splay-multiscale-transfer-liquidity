"""Only new population4 source controls, with immediate checkpoints."""
import sys,json,time,hashlib,copy,importlib.util
from pathlib import Path
from itertools import product
sys.path[:0]=['DO_RESEARCH_REBOOT/M3_POP4_RISK01','DO_RESEARCH_REBOOT/M3_UNITPAIR01','DO_RESEARCH_REBOOT/M3_OUT01','DO_RESEARCH_REBOOT/M3_GAPINT01']
# Load explicitly: UNITPAIR01 also has a module named decoder.
spec=importlib.util.spec_from_file_location('population_four_decoder',Path('DO_RESEARCH_REBOOT/M3_POP4_RISK01/certified_decoder.py'));D=importlib.util.module_from_spec(spec);spec.loader.exec_module(D)
from proposal_factory_v2 import proposals
import interior_original as IN
import outside_original as OUT
sp=importlib.util.spec_from_file_location('independent_population_raw',Path('DO_RESEARCH_REBOOT/M3_TWOGAP_AUD01/source_audit.py'));A=importlib.util.module_from_spec(sp);sp.loader.exec_module(A)
BASE=Path('DO_RESEARCH_REBOOT/M3_POP4_RISK01');S=IN.S
def fullsig(v):return list(v)
def mirror(t):return S.LEAF if t[0]=='leaf' else S.node(128-t[1],mirror(t[3]),mirror(t[2]))
def main():
    out=BASE/'source_audit.json';assert not out.exists();start=time.process_time()
    run=json.loads((BASE/'run_result.json').read_text());assert run['status'] in ('ALL360_TOTAL4_MULTI_FINITE_CERTIFICATES_PASS','STOPPED_ON_FIRST_FAILURE')
    P=D.PopulationFourCertificate();dl=IN.DAG();L=IN.build_slow(dl,'MXL');dh=IN.DAG();H=IN.build_shigh(dh,'MXH');FIN,FOUT=proposals(IN),proposals(OUT)
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
    selected=[[3,1,0,0,0,0,0,0,0,0],[2,2,0,0,0,0,0,0,0,0],[1,3,0,0,0,0,0,0,0,0],
      [0,0,0,0,0,0,0,0,1,3],[0,3,1,0,0,0,0,0,0,0],[0,0,0,0,2,2,0,0,0,0]]
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
    # New source controls: a helper strictly BETWEEN two other gap0 keys.
    middle_sig=(3,1,0,0,0,0,0,0,0,0);middle_rows=[]
    if middle_sig in covered:
        for w in (0,1):
            choice=next((bi for bi,t in enumerate(P.B['trees']) if t[0]==0 and P.B['kernels']['0'][bi][8] is not None and P.B['kernels']['0'][bi][8][1]==w),None)
            assert choice is not None,('missing pinned B kernel',w)
            def scale(t):return z if t is None else S.node(16*t[0],scale(t[1]),scale(t[2]))
            BB=scale(P.B['trees'][choice]);BB=IN.V.insert(IN.V.insert(BB,-8),8)
            AA=S.node(0,S.node(-7,S.node(-8,z,z),S.node(-6,z,z)),S.node(128,S.balanced([16*k for k in range(1,8)]),z));AA=IN.V.insert(AA,8)
            cuts=[(128,0)];word=[['K',-7],['K',128]]
            _,_,r=FIN.low(dl,L,AA,BB,cuts,word,f'pop4_middle_of_three_gap0_w{w}',341)
            row=check(r,'LOW');assert r['H']==2 and r['w']==w and r['word_codes'][0][1]==-7
            middle_rows.append({'row':row,'A':AA,'B':BB,'cuts':cuts})
        item=middle_rows[1]
        _,_,r=FIN.low(dl,L,item['A'],item['B'],item['cuts'],[['D',-7],['K',-7],['K',128]],'pop4_middle_of_three_DELETE_zeroKEEP',341)
        macro=check(r,'LOW');normal=item['row']
        assert A.flat(macro['source'])==A.flat(normal['source']) and A.flat(macro['destination'])==A.flat(normal['destination'])
        assert macro['q']==normal['q'] and macro['weight']==normal['weight']==1 and r['H']==2
        AA=mirror(item['A']);BB=mirror(item['B']);cuts=[(128-k,1-side) for k,side in item['cuts']]
        _,_,r=FOUT.low(dl,L,AA,BB,cuts,[['K',135],['K',0]],'pop4_reflected_middle_of_three_gap9_w1',341)
        row=check(r,'LOW');assert r['word_codes'][0][1]==135 and r['w']==1
    report={'status':'POPULATION4_ORIGINAL_SOURCE_AND_FULL_CLOSURE_PASS','completed_canonical_signatures':completed,'new_original_signatures':len(covered),
      'unique_original_roots':len(rows),'full_closed_mixed_cycles':len(cycles),'all147_O_coordinates':True,'same_actual127_M':True,
      'new_helper_controls':len(rows)-len(completed)-2*len(cycles),'middle_of_three_gap0_and_gap9':bool(middle_rows),
      'middle_DELETE_zeroKEEP_same_actual_node':bool(middle_rows),'previous_source_checks_repeated':0,'h0_correction_reused_not_replayed':True,
      'self_reflecting_canonical_controls':sum(s==list(reversed(s)) for s in completed),'DAG_nodes':[len(dl.nodes),len(dh.nodes)],
      'CPU_seconds':round(time.process_time()-start,3),'root_files':source_files,'cycles':cycles,'full_M3_proved':False}
    assert report['new_helper_controls']<=8 and len(cycles)<=6 and report['CPU_seconds']<300
    with out.open('x') as f:json.dump(report,f,indent=2)
    print(json.dumps({k:v for k,v in report.items() if k not in ('completed_canonical_signatures','root_files','cycles')},indent=2),flush=True)
if __name__=='__main__':main()
