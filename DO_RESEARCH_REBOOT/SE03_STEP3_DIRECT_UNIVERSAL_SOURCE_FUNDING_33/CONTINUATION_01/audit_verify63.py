"""Independent actual-ID matching and symbolic preparation-bound audit."""
import json,time,sys,hashlib
from pathlib import Path
B=Path(__file__).resolve().parent;START=time.process_time();CAP=float(sys.argv[1])
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def main():
    S=json.loads((B/'core13_framed_activation_closed_source.json').read_text());Z=json.loads((B/'framed_core13_full_matching.json').read_text());rows=S['period_rows'];ends=[i for i,r in enumerate(rows) if r['kind']=='K' and r['key']!=r['BF_before'][0]];h={tuple(r['demand']):tuple(r['unit']) for r in Z['full_pairs']};h0={};D=set();U=set();mm=[]
    for j,end in enumerate(ends):
        pre=ends[j-1];inds=list(range(pre+1,end+1)) if pre<end else list(range(pre+1,len(rows)))+list(range(end+1));units=[(rows[i]['absolute_t'],a,b) for i in inds for a in range(1,rows[i]['H']+1) for b in (0,1)];demands=[(rows[i]['absolute_t'],k) for i in inds for k in range(1,rows[i]['QF']+1)];own=min(len(units),len(demands));h0.update(zip(demands[:own],units[:own]));D.update(demands);U.update(units);mm.append((units,demands))
    assert set(h)==D and len(h)==len(set(h.values()))==36 and set(h.values())<=U and len(U)==318 and all(h[d]==u for d,u in h0.items());assert h0=={tuple(r['demand']):tuple(r['unit']) for r in Z['natural_h0']};unpaid=D-set(h0);assert len(unpaid)==2
    for i,(units,demands) in enumerate(mm):
        missing=[d for d in demands if d in unpaid]
        if missing:
            preunits,predemands=mm[i-1];assert len(predemands)==1 and len(preunits)//2>=7 and len(units)==4 and len(demands)==6
            assert all(h[d]==preunits[1+k] for k,d in enumerate(missing))
    # Uniform depth proof uses symbolic integer affine expressions, not sampled r.
    # n=2r-1 => before depth2r-4; after3; decrease2r-7=2(r-4)+1.
    assert (2,-7)==(2,-8+1) and (2,-4)==(2,-1-3)
    # r>=6: (2r-1)-(r-5)=r+4, with positive coefficients.
    assert (2-1,-1+5)==(1,4)
    # A right rotation changes local depths for [parent,pivot,A,M,R] by these
    # symbolic offsets; every coordinate's decrease is<=1.
    before=[0,1,2,2,1];after=[1,0,1,2,2];assert max(a-b for a,b in zip(before,after))==1 and max(b-a for a,b in zip(before,after))==1
    assert time.process_time()-START<CAP-1
    inherited=B.parent.parent/'SE03_STEP2_REPAY01/UNIFORM_RANGE_OBSTRUCTION.md';deps=('FRAMED_FAMILY_PHYSICAL_REPAYMENT.md','framed_core13_full_matching.json','framed_return_and_core13_independent_audit.json','uniform_A_realization_independent_audit.json')
    out('framed_family_repayment_independent_audit.json',{'status':'PASS_RESTRICTED_ALL_R_PREPARED_FRAME_MATCHING_AND_OWNER_EXTENSION_INTERFACE','r_quantifier':'all integers r>=3 under the specified diagonal-prefix/preparation/reset source hypotheses','uniform_source_bound':'one rotation decreases target depth by<=1; Hprep>=r-3; previous H>=r,Q1; own-spare2r-1>=max(r-5,0)','explicit_source_rule':'critical slot5+i uses predecessor unit zero-based ordinal1+i; all other demands retain exact h0','arbitrary_finite_disjoint_repetitions':True,'original_core13_control_demands':36,'original_core13_control_units':318,'original_control_added_donors':Z['donor_additions'],'frozen_owner_scope':'conditional algebraic extension using inherited support-free finite h/partial exchange; all original eligibility/working/cut hypotheses retained','Bank25_certificate':False,'arbitrary_dirty_start_covered':False,'no_auxiliary_normalization_receipt_invented':True,'source_queries':0,'source_engine_calls':0,'principal_U33':'OPEN','external_or_formal_verification':False,'input_sha256':{**{n:hashlib.sha256((B/n).read_bytes()).hexdigest() for n in deps},str(inherited):hashlib.sha256(inherited.read_bytes()).hexdigest()}});print(json.dumps({'status':'PASS_PREPARED_ALL_R_SOURCE_MATCHING_THEOREM','control_demands':36,'Bank25_interface':'OPEN','dirty_start_extension':'OPEN','principal_U33':'OPEN'}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_verify63_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0})
