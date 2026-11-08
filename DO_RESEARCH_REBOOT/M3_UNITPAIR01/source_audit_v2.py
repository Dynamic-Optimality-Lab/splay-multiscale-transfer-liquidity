"""Bounded original-root family audit; complete coverage is from the source proof."""
import sys,json,time,hashlib,importlib.util
from pathlib import Path
sys.path[:0]=['DO_RESEARCH_REBOOT/M3_UNITPAIR01','DO_RESEARCH_REBOOT/M3_OUT01','DO_RESEARCH_REBOOT/M3_GAPINT01']
from decoder import UnitPairCertificate
import interior_original as IN
import outside_original as OUT
spec=importlib.util.spec_from_file_location('twogap_independent_source',Path('DO_RESEARCH_REBOOT/M3_TWOGAP_AUD01/source_audit.py'));A=importlib.util.module_from_spec(spec);spec.loader.exec_module(A)
BASE=Path('DO_RESEARCH_REBOOT/M3_UNITPAIR01')
from proposal_factory import proposals
FIN,FOUT=proposals(IN),proposals(OUT)
def main():
    out=BASE/'source_audit_v2.json';assert not out.exists();start=time.process_time();P=UnitPairCertificate();dl=IN.DAG();L=IN.build_slow(dl,'MXL');dh=IN.DAG();H=IN.build_shigh(dh,'MXH')
    rows=[];cycles=[];negative=[];S=IN.S;z=S.LEAF
    def check(r,kind,g,h):
        d,obj=(dl,L) if kind=='LOW' else (dh,H);e=r['environment'];assert d.ev_ground(obj['root'],e)
        s=A.ordinary(d,e,obj['s']);t=A.ordinary(d,e,obj['t']);assert s==r['source'] and t==r['destination'];assert len(A.flat(s))==len(A.flat(t))==147
        sig=[int(i in (g,h)) for i in range(10)];assert s['sigma']==t['sigma']==sig
        js,jt=P.J(s),P.J(t);assert -2<=js<=0 and -2<=jt<=0
        if kind=='LOW':
            nv=A.val(d,e,L['wit'].nev);charged=sum((A.val(d,e,L['wit'].evd[i])+1)//2 for i in range(nv));q=A.val(d,e,L['bt'].q)
            assert charged==r['H'] and q==r['q'] and 2*charged-q==r['w'];res=r['w']-P.O(t)+P.O(s);assert res>=0;m=None
        else:
            m=A.mid(d,e,H['g']);assert m==r['shared_midpoint'] and len(A.flat(m))==127
            w=A.val(d,e,H['w1']);res=[w-P.M(m)+P.O(s),P.M(m)-P.O(t)];assert min(res)>=0
        rows.append({'label':r['label'],'g':g,'h':h,'kind':kind,'w':r['w'],'source':s,'destination':t,'midpoint':m,
          'J_source':js,'J_destination':jt,'residual':res,'environment_sha256':hashlib.sha256(json.dumps(e,sort_keys=True).encode()).hexdigest()})
        assert time.process_time()-start<300,'UNKNOWN source family CPU cap'
        return rows[-1]
    for g in range(10):
        for h in range(g+1,10):
            helper=FOUT if h==9 or (g+h)%2 else FIN
            B=S.node(32,S.node(0,z,S.node(16,z,z)),S.node(96,S.balanced([48,64,80]),S.balanced([112,128])))
            AA=S.node(32,S.node(0,z,S.node(16,z,z)),S.node(96,S.balanced([48,64,80]),S.balanced([112,128])))
            for gap in (g,h):B=IN.V.insert(B,16*gap-8);AA=IN.V.insert(AA,16*gap-8)
            Ad,Bd,low=helper.low(dl,L,AA,B,[(0,1),(96,0)],[['K',96]],f'pair_{g}_{h}_fresh_cycle_low',341)
            high=helper.high(dh,H,Bd,32,low['destination'],low['source'],f'pair_{g}_{h}_fresh_cycle_high')
            lo=check(low,'LOW',g,h);hi=check(high,'HIGH',g,h)
            assert A.flat(lo['source'])==A.flat(hi['destination']) and A.flat(lo['destination'])==A.flat(hi['source'])
            assert low['w']+high['w']==8
            cycles.append({'g':g,'h':h,'weight':8,'full147_O_closure':True,'same127_M':True,'chi8':P.chi(lo['source']['b']),
              'low_environment':low['environment'],'high_environment':high['environment']})
            # A cheap key8 access against a deepest B spine, both units retained in sigma.
            AA=S.node(0,z,S.node(128,S.balanced([16*k for k in range(1,8)]),z));B=z
            for k in reversed(range(9)):B=S.node(16*k,z,B)
            for gap in (g,h):AA=IN.V.insert(AA,16*gap-8);B=IN.V.insert(B,16*gap-8)
            _,_,nr=helper.low(dl,L,AA,B,[(128,0)],[['K',128]],f'pair_{g}_{h}_weight_minus2',341);rr=check(nr,'LOW',g,h);assert nr['w']==-2
            negative.append({'g':g,'h':h,'residual':rr['residual'],'environment':nr['environment']})
            print(json.dumps({'pair':[g,h],'roots':len(rows),'cpu_seconds':round(time.process_time()-start,3)}),flush=True)
    assert len(cycles)==45 and len(negative)==45 and len(rows)==135
    report={'status':'ORIGINAL_SOURCE_FAMILY_AND_FULL_CLOSURE_PASS','signature_pairs':45,'full_original_roots':135,'low_roots':90,'high_roots':45,
      'fresh_full_mixed_cycles':45,'negative_low_controls':45,'all_full_O_coordinates':147,'all_actual_M_coordinates':127,
      'both_chi8_regions_represented':{c['chi8'] for c in cycles}=={False,True},'sigma9_positive_never_chi8':all(not c['chi8'] for c in cycles if c['h']==9),
      'DAG_nodes':[len(dl.nodes),len(dh.nodes)],'cpu_seconds':round(time.process_time()-start,3),'rows':rows,'cycles':cycles,'negative_controls':negative,'full_M3_proved':False,'proposal_fixture_AST_edits':FIN.proposal_edits+FOUT.proposal_edits}
    with out.open('x',encoding='utf-8') as f:json.dump(report,f,separators=(',',':'))
    print(json.dumps({k:v for k,v in report.items() if k not in ('rows','cycles','negative_controls')},indent=2),flush=True)
if __name__=='__main__':main()
