"""Pin the inspected primary theorem and its new source-specific corollary."""
import json,time,urllib.request,hashlib
from pathlib import Path
B=Path(__file__).resolve().parent
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def main():
    url='https://arxiv.org/pdf/1907.06310v3';raw=urllib.request.urlopen(url,timeout=20).read();assert raw.startswith(b'%PDF')
    with (B/'primary_1907_06310v3.pdf').open('xb') as f:f.write(raw)
    out('uniform_A_realization_proof_object.json',{'status':'UNIFORM_SOURCE_REALIZATION_COROLLARY_DERIVED_AUDIT_PENDING','primary_dependency':{'title':'A Foundation for Proving Splay is Dynamically Optimal','authors':['Caleb C. Levy','Robert E. Tarjan'],'version':'arXiv:1907.06310v3','theorem':'3.4','url':url,'pdf_sha256':hashlib.sha256(raw).hexdigest(),'definition_and_proof_inspected':True,'imported':'finite ordinary-bottom-up endpoint transformation for same-key BSTs of size>=4','external_numeric_cost_not_imported':True},'conditions':['N>=4','same finite physical ordered key set','specified genuine K_g with S_g(Bprev)=Bs and root(Bprev)!=g','root(As)=g','specified original packet P with B path Bs->Bt','specified closing KEEP segment V with Bt->Bprev','given closed B cycle genuine support exactly M'],'symbolic_steps':[{'rule':'A_ONLY_TRANSFORM','before':['Bprev','Bprev'],'target':'As','after':['As','Bprev']},{'rule':'KEEP_G','before':['As','Bprev'],'target':'g','after':['As','Bs'],'A_cost':0,'B_genuine':True},{'rule':'ORIGINAL_PACKET_UNCHANGED','before':['As','Bs'],'word':'P','after':['Ap','Bt'],'H_Q_unchanged':True},{'rule':'GIVEN_B_CLOSURE','before':['Ap','Bt'],'word':'KEEP(V)','after':['Av','Bprev']},{'rule':'A_ONLY_TRANSFORM','before':['Av','Bprev'],'target':'Bprev','after':['Bprev','Bprev']}],'erased_and_chart_closure':'actual finite-state eventual recurrence of W; choose actual u,L and warm charts','extra_A_costs':'all actual; no credit amount asserted, none omitted from W','funding_claim':False,'source_queries':0,'principal_U33':'OPEN','proof_sha256':hashlib.sha256((B/'UNIFORM_A_REALIZATION_OVER_CLOSED_B.md').read_bytes()).hexdigest()});print(json.dumps({'status':'UNIFORM_A_REALIZATION_DEPENDENCY_PINNED','bytes':len(raw),'primary_sha256':hashlib.sha256(raw).hexdigest(),'new_source_queries':0}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_proof72_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0})
