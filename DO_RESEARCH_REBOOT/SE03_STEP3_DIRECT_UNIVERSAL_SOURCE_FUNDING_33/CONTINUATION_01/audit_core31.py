"""Materialize the interior max-contraction failure in a closed source word."""
import json,time,sys,hashlib,importlib.util
from pathlib import Path
from interior_projection_source_tools import *
from four_hull_source_compiler import HullCompiler
from four_hull_source_reuse import from_kernel
from finite_source_word_compiler import Compiler
B=Path(__file__).resolve().parent;P=B.parent.parent;START=time.process_time();CAP=float(sys.argv[1]);QCAP=int(sys.argv[2]);queries=0
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def main():
    global queries
    source=P/'SE03_STEP2_COLD_NEG2_01/source_model.py';sp=importlib.util.spec_from_file_location('constructive_four_hull_source33',source);S=importlib.util.module_from_spec(sp);sp.loader.exec_module(S);p0=S.path
    def tickpath(t,x):
        global queries
        if queries>=QCAP or time.process_time()-START>CAP-2:raise TimeoutError('SOURCE_RESOURCE_CAP')
        queries+=1;return p0(t,x)
    S.path=tickpath;G=from_kernel(json.loads((B/'interior_max_contraction_closed_source.json').read_text())['four_hull_source_kernel']);native=json.loads((B/'native10_source_actions.json').read_text());T=list(map(fr,native['trees']));C=Compiler(native);family=json.loads((B/'B_full_spectrum_result_02.json').read_text());e=family['causal_edges'][1];private=e['private_key'];gap=(private-1)//2
    def embed(core):
        def bind(v):
            if not isnode(v):return (private,'L','R') if v=='F'+str(gap) else v
            return 2*v[0],bind(v[1]),bind(v[2])
        return normalize(bind(core),{v:v for v in []}) if False else normphysical(bind(core))
    physical=sorted([2*v for v in range(1,11)]+[private]);ranks={k:j+1 for j,k in enumerate(physical)}
    def normphysical(t):
        def walk(v,hi):return 'F'+str(hi) if not isnode(v) else (v[0],walk(v[1],ranks[v[0]]-1),walk(v[2],hi))
        return walk(t,11)
    b=e['source_B_core_index'];bt=e['B_target_core_index'];bpre,g=C.incoming[b];initial=embed(T[bpre]);As=normphysical(fr(e['source_A']));assert As[0]==2*g
    prep=G.compile(initial,As);word=[('D',r['key']) for r in prep];arows=[{'mode':'D',**r} for r in prep];word.append(('K',2*g));arows.append({'mode':'K','key':2*g,'before':As,'after':As,'H':0,'method':'literal root identity'})
    packet_index=len(word);x=e['target_actual_key'];after,pa,ea=S.trace(As,x);assert len(ea)==1 and after==normphysical(fr(e['actual_A_target']));word.append(('K',x));arows.append({'mode':'K','key':x,'before':As,'after':after,'H':len(ea),'method':'fresh ordinary eleven-key source'})
    close=C.inward(bt)+list(range(2,11))+list(range(9,0,-1))+C.outward(bpre);a=after
    for k in close:
        at,p,ev=S.trace(a,2*k);word.append(('K',2*k));arows.append({'mode':'K','key':2*k,'before':a,'after':at,'H':len(ev),'method':'fresh ordinary eleven-key source'});a=at
    reset=G.compile(a,initial)
    for r in reset:word.append(('D',r['key']));arows.append({'mode':'D',**r})
    assert arows[0]['before']==arows[-1]['after']==initial
    for left,right in zip(arows,arows[1:]):assert left['after']==right['before']
    D=native['destination'];Q=native['Q'];E=bpre;fullchart=();erasechart=();seen={};copies=[];copy=0
    def chart(c,k):return (k,)+tuple(v for v in c if v!=k)
    while (E,fullchart,erasechart) not in seen:
        seen[E,fullchart,erasechart]=copy;F=bpre;old=(E,fullchart,erasechart);rows=[]
        for j,(mode,key) in enumerate(word):
            f0,e0=F,E;cf,ce=fullchart,erasechart;q=qe=0
            if mode=='K':
                assert key%2==0;k=key//2;F=D[F][k-1];q=Q[f0][k-1]
                if k!=T[f0][0]:fullchart=chart(fullchart,k)
                if k!=10:
                    E=D[E][k-1];qe=Q[e0][k-1]
                    if k!=T[e0][0]:erasechart=chart(erasechart,k)
            rows.append({'absolute_t':copy*len(word)+j+1,'word_index':j,'kind':mode,'key':key,'BF_before':f0,'BF_after':F,'BE_before':e0,'BE_after':E,'H':arows[j]['H'],'QF':q,'QE':qe,'chartF_before':cf,'chartF_after':fullchart,'chartE_before':ce,'chartE_after':erasechart})
        assert F==bpre;copies.append({'start':old,'end':(E,fullchart,erasechart),'rows':rows});copy+=1
        if time.process_time()-START>CAP-2:raise TimeoutError('CLOSURE_CPU')
    u=seen[E,fullchart,erasechart];L=copy-u;assert u>=1;period=sum((c['rows'] for c in copies[u:u+L]),[]);assert copies[u]['start']==copies[u+L-1]['end'];local=next(r for r in period if r['word_index']==packet_index);assert (local['BF_before'],local['BF_after'],local['H'],local['QF'])==(b,bt,e['H'],e['Q']);assert len(period)==L*len(word)
    A=sum(r['H'] for r in period);QF=sum(r['QF'] for r in period);QE=sum(r['QE'] for r in period);# aggregate cost recorded independently; no Coarse-Double assumption
    result={'status':'EXPLICIT_PAIRED_CLOSED_FULL_B_FULL_MULTISET_EDGE','candidate':e,'initial_common_A_B_BE':initial,'word':word,'A_word_source_rows':arows,'four_hull_source_kernel':{'trees':G.T,'destinations':G.dest,'H':G.H},'G4_rigid_term_instantiations':G.instantiations,'raw_rotations_are_not_original_events':True,'source_prefix_copies':u,'period_copies':L,'period':[period[0]['absolute_t'],period[-1]['absolute_t']],'period_rows':period,'packet_absolute_t':local['absolute_t'],'A_period':A,'QF_period':QF,'QE_period':QE,'CD_margin':2*A-QF,'all_A_B_BE_and_full_genuine_recency_orders_close':True,'source_queries':queries,'source_engine_calls':queries,'original_hanging_payloads':'all displayed gap terms chosen empty; no finite population is used as a universal proof','legal_owner_exchange':'none constructed or altered; this refutes a candidate state formula, not a frozen allocation','not_a_Coarse_Double_counterexample':2*A>=QF,'principal_U33':'OPEN','input_sha256':{n:hashlib.sha256((B/n).read_bytes()).hexdigest() for n in ('native10_source_actions.json','native10_credit_certificate.json','B_full_spectrum_result_02.json')}}
    out('B_full_spectrum_edge_1_closed_source.json',result);print(json.dumps({k:result[k] for k in ('status','source_prefix_copies','period_copies','period','packet_absolute_t','A_period','QF_period','QE_period','CD_margin','source_queries','G4_rigid_term_instantiations')}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_core31_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':queries,'source_engine_calls':queries})
