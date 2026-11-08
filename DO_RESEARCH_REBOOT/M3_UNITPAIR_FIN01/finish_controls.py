"""Only the three missing support cases. No completed predicate is replayed."""
import sys,json,time,hashlib,importlib.util
from pathlib import Path
sys.path[:0]=['DO_RESEARCH_REBOOT/M3_UNITPAIR01','DO_RESEARCH_REBOOT/M3_OUT01','DO_RESEARCH_REBOOT/M3_GAPINT01']
from decoder import UnitPairCertificate
from proposal_factory_v2 import proposals
import interior_original as IN
import outside_original as OUT
spec=importlib.util.spec_from_file_location('independent_raw_interface',Path('DO_RESEARCH_REBOOT/M3_TWOGAP_AUD01/source_audit.py'));A=importlib.util.module_from_spec(spec);spec.loader.exec_module(A)
BASE=Path('DO_RESEARCH_REBOOT/M3_UNITPAIR_FIN01');OLD=Path('DO_RESEARCH_REBOOT/M3_UNITPAIR01')
def main():
    out=BASE/'source_completion.json';assert not out.exists();start=time.process_time()
    previous=json.loads((OLD/'source_audit_cap.json').read_text());todo=[tuple(p) for p in previous['incomplete_support_controls']]
    assert todo==[(7,8),(7,9),(8,9)];done={tuple(p) for p in previous['completed_supports']};assert not done.intersection(todo)
    P=UnitPairCertificate();dl=IN.DAG();L=IN.build_slow(dl,'MXL');dh=IN.DAG();H=IN.build_shigh(dh,'MXH');FIN,FOUT=proposals(IN),proposals(OUT)
    rows=[];cycles=[];S=IN.S;z=S.LEAF
    def check(r,kind,g,h):
        d,obj=(dl,L) if kind=='LOW' else (dh,H);env=r['environment'];assert set(d.vars)<=set(env)
        for name,n in d.vars.items():
            nd=d.nodes[n];v=env[name]
            if nd[1]=='bool':assert v in (False,True)
            else:
                width,signed=nd[3][2:4];assert (-(1<<(width-1))<=v<(1<<(width-1))) if signed else 0<=v<(1<<width)
        assert d.ev_ground(obj['root'],env),r['label']
        s=A.ordinary(d,env,obj['s']);t=A.ordinary(d,env,obj['t']);assert s==r['source'] and t==r['destination']
        assert len(A.flat(s))==len(A.flat(t))==147 and s['sigma']==t['sigma']==[int(i in (g,h)) for i in range(10)]
        js,jt=P.J(s),P.J(t)
        if kind=='LOW':
            nv=A.val(d,env,L['wit'].nev);charge=sum((A.val(d,env,L['wit'].evd[i])+1)//2 for i in range(nv));q=A.val(d,env,L['bt'].q)
            assert charge==r['H'] and q==r['q'] and 2*charge-q==r['w'];res=r['w']-P.O(t)+P.O(s);assert res>=0;m=None
        else:
            m=A.mid(d,env,H['g']);assert m==r['shared_midpoint'] and len(A.flat(m))==127
            w=A.val(d,env,H['w1']);assert w==r['w'];res=[w-P.M(m)+P.O(s),P.M(m)-P.O(t)];assert min(res)>=0
        assert time.process_time()-start<300,'UNKNOWN completion audit CPU cap'
        row={'label':r['label'],'g':g,'h':h,'kind':kind,'source':s,'destination':t,'midpoint':m,'J_source':js,'J_destination':jt,
          'weight':r['w'],'residual':res,'original_root':True,'environment_sha256':hashlib.sha256(json.dumps(env,sort_keys=True).encode()).hexdigest(),'environment':env}
        rows.append(row);return row
    for g,h in todo:
        checkpoint=BASE/f'p{g}_{h}.json';assert not checkpoint.exists();first=len(rows);helper=FOUT if h==9 or (g+h)%2 else FIN
        B=S.node(32,S.node(0,z,S.node(16,z,z)),S.node(96,S.balanced([48,64,80]),S.balanced([112,128])))
        AA=S.node(32,S.node(0,z,S.node(16,z,z)),S.node(96,S.balanced([48,64,80]),S.balanced([112,128])))
        for gap in (g,h):B=IN.V.insert(B,16*gap-8);AA=IN.V.insert(AA,16*gap-8)
        _,Bd,low=helper.low(dl,L,AA,B,[(0,1),(96,0)],[['K',96]],f'pair_{g}_{h}_fresh_cycle_low',341)
        high=helper.high(dh,H,Bd,32,low['destination'],low['source'],f'pair_{g}_{h}_fresh_cycle_high')
        lo=check(low,'LOW',g,h);hi=check(high,'HIGH',g,h)
        assert A.flat(lo['source'])==A.flat(hi['destination']) and A.flat(lo['destination'])==A.flat(hi['source']);assert low['w']+high['w']==8
        cycle={'g':g,'h':h,'weight':8,'full147_O_closure':True,'same127_M':True,'chi8':P.chi(lo['source']['b'])};cycles.append(cycle)
        AA=S.node(0,z,S.node(128,S.balanced([16*k for k in range(1,8)]),z));B=z
        for k in reversed(range(9)):B=S.node(16*k,z,B)
        for gap in (g,h):AA=IN.V.insert(AA,16*gap-8);B=IN.V.insert(B,16*gap-8)
        _,_,nr=helper.low(dl,L,AA,B,[(128,0)],[['K',128]],f'pair_{g}_{h}_weight_minus2',341);check(nr,'LOW',g,h);assert nr['w']==-2
        with checkpoint.open('x',encoding='utf-8') as f:json.dump({'status':'PASS','pair':[g,h],'rows':rows[first:],'cycle':cycle},f,separators=(',',':'))
        print(json.dumps({'pair':[g,h],'new_roots':len(rows),'CPU':round(time.process_time()-start,3)}),flush=True)
    assert len(rows)==9 and len(cycles)==3
    report={'status':'THREE_REMAINING_SOURCE_CONTROLS_PASS','only_supports_executed':todo,'previously_completed_supports_replayed':0,
      'new_original_roots':9,'new_full_mixed_cycles':3,'DAG_nodes':[len(dl.nodes),len(dh.nodes)],'CPU_seconds':round(time.process_time()-start,3),
      'original_previous_cap_retained':previous['status'],'prior42_controls_reused_by_pinned_provenance':True,
      'source_coverage_now_complete':True,'full_M3_proved':False,'checkpoint_files':[f'p{g}_{h}.json' for g,h in todo]}
    with out.open('x',encoding='utf-8') as f:json.dump(report,f,indent=2)
    print(json.dumps(report,indent=2),flush=True)
if __name__=='__main__':main()
