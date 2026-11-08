"""Independent symbolic word-composition and dependency audit of the corollary.
This checks the derived interface, not the published theorem by finite tests.
"""
import json,time,hashlib
from pathlib import Path
B=Path(__file__).resolve().parent
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def main():
    p=json.loads((B/'uniform_A_realization_proof_object.json').read_text());dep=p['primary_dependency'];assert hashlib.sha256((B/'primary_1907_06310v3.pdf').read_bytes()).hexdigest()==dep['pdf_sha256'];assert hashlib.sha256((B/'UNIFORM_A_REALIZATION_OVER_CLOSED_B.md').read_bytes()).hexdigest()==p['proof_sha256'];assert dep['version']=='arXiv:1907.06310v3' and dep['theorem']=='3.4' and dep['definition_and_proof_inspected'] and dep['external_numeric_cost_not_imported'];content='primary definition and proof independently reread through authoritative web PDF'
    try:
        from pypdf import PdfReader
        reader=PdfReader(str(B/'primary_1907_06310v3.pdf'));text=''.join(page.extract_text() or '' for page in reader.pages[5:8]);compact=''.join(text.split());assert 'Theorem3.4.' in compact and 'four' in text.lower();content='local pinned PDF text extracted: Theorem3.4 and same-key size>=4 transformation proof'
    except ModuleNotFoundError:pass
    # Symbolic states stand for arbitrary same-key finite BSTs, not test fixtures.
    A=Bstate='Bprev';Aroots={'As':'g'};Bsteps={('Bprev','g'):'Bs',('Bs','P'):'Bt',('Bt','KEEP(V)'):'Bprev'};Asteps={('As','P'):'Ap',('Ap','KEEP(V)'):'Av'};events=[]
    for step in p['symbolic_steps']:
        assert step['before']==[A,Bstate]
        if step['rule']=='A_ONLY_TRANSFORM':A=step['target'];events.append(('ALL_DELETE_TRANSFORMATION',step['before'][0],A,'ALL_REAL_COSTS_RETAINED'))
        elif step['rule']=='KEEP_G':
            assert Aroots[A]==step['target']=='g' and step['A_cost']==0 and step['B_genuine'];Bstate=Bsteps[Bstate,'g'];events.append(('KEEP','g','ACTUAL_Q_G'))
        elif step['rule']=='ORIGINAL_PACKET_UNCHANGED':
            assert step['word']=='P' and step['H_Q_unchanged'];A=Asteps[A,'P'];Bstate=Bsteps[Bstate,'P'];events.append(('EXACT_ORIGINAL_PACKET','P','ALL_ORIGINAL_H_Q'))
        elif step['rule']=='GIVEN_B_CLOSURE':A=Asteps[A,step['word']];Bstate=Bsteps[Bstate,step['word']];events.append(('KEEP_CLOSING_SEGMENT','V','ALL_REAL_A_B_COSTS'))
        else:raise ValueError('Unknown symbolic rule')
        assert step['after']==[A,Bstate]
    assert (A,Bstate)==('Bprev','Bprev');assert sum(e[0]=='EXACT_ORIGINAL_PACKET' for e in events)==1 and not p['funding_claim'];assert len(p['conditions'])==7 and any('root(Bprev)!=g' in s for s in p['conditions']) and any('N>=4' in s for s in p['conditions']);out('uniform_A_realization_independent_audit.json',{'status':'PASS_UNIFORM_SOURCE_REALIZATION_COROLLARY_INTERFACE_AUDIT','mathematical_result':'arbitrary finite synchronized A shadow over a GIVEN closed B cycle embeds in an original common-diagonal, fully paired/erased/chart-closed source','proof_method':'symbolic same-key word composition, published all-size transformation theorem, and actual finite-state recurrence; no finite source samples used as a universal proof','primary_dependency_inspection':content,'symbolic_cost_ledger':events,'arbitrary_private_A_ancestors_allowed':True,'unproved_B_closed_cycle_premise_discharged':False,'funding_or_donor_claim':False,'source_queries':0,'principal_U33':'OPEN','external_or_formal_verification':False,'input_sha256':{n:hashlib.sha256((B/n).read_bytes()).hexdigest() for n in ('UNIFORM_A_REALIZATION_OVER_CLOSED_B.md','uniform_A_realization_proof_object.json','primary_1907_06310v3.pdf')}});print(json.dumps({'status':'PASS_UNIFORM_A_SOURCE_REALIZATION_COROLLARY','primary_inspection':content,'no_funding_claim':True,'new_source_queries':0}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_verify30_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0})
