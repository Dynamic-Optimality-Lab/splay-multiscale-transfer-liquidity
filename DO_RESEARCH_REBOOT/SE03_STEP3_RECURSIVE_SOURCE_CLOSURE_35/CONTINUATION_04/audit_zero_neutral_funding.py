"""Distinct derivation and literal source-bit audit, reusing accepted traces."""
import collections,hashlib,json,sys,time
from pathlib import Path
F=Path(__file__).resolve().parent;B=F.parents[1]/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
CAP=float(sys.argv[1]);START=time.process_time()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def labels(t,S):
    out=set()
    def go(u):
        if u is None:return frozenset()
        v=go(u[1])|go(u[2])|({u[0]} if u[0] in S else set())
        if v:out.add(frozenset(v))
        return frozenset(v)
    go(t);return out
def psi(A,B,S):return len(labels(B,S)-labels(A,S))
def main():
    deriv=json.loads((F/'zero_neutral_funding_derivation.json').read_text())
    for name,digest in deriv['input_sha256'].items():assert sha(F.parents[1]/name)==digest
    assert deriv['output_sha256']==sha(F/'ZERO_NEUTRAL_FULL_SOURCE_FUNDING.md')
    annotation=json.loads((F/'independent_core_sector_neutral.json').read_text())
    sourcepath=F/'maximal_completion_original_source.json'
    assert annotation['input_sha256'][str(sourcepath)]==sha(sourcepath)
    control=next(r for r in annotation['controls'] if r['source']=='NONMAX')
    assert control['B0']==0 and control['B1']+control['B2']==control['Q']
    # Exact polynomial identity, over indeterminates rather than sample costs.
    delta={'P':1,'N':-1,'B1':-1,'B2':-2,'Z1':-1}
    price={'H':2,'B1':-1,'B2':-1}
    difference=collections.Counter(price)
    for k,v in delta.items():difference[k]-=v
    assert {k:v for k,v in difference.items() if v}=={'H':2,'P':-1,'N':1,'B2':1,'Z1':1}
    src=json.loads(sourcepath.read_text());rows=src['period_rows'];S=set(control['S'])
    ends=[i for i,r in enumerate(rows) if r['genuine_F']]
    macros=[];h0={}
    for j,end in enumerate(ends):
        start=(ends[j-1]+1)%len(rows)
        ids=list(range(start,end+1)) if start<=end else list(range(start,len(rows)))+list(range(end+1))
        seg=[rows[i] for i in ids]
        units=[(r['t'],k,b) for r in seg for k in range(1,r['a']+1) for b in (0,1)]
        demands=[(seg[-1]['t'],k) for k in range(1,seg[-1]['qF']+1)]
        h0.update(dict(zip(demands,units)))
        a=psi(seg[0]['A_before'],seg[0]['BF_before'],S)
        z=psi(seg[-1]['A_after'],seg[-1]['BF_after'],S)
        H=sum(r['a'] for r in seg);Q=len(demands)
        assert 2*H-Q-(z-a)>=0
        macros.append({'indices':ids,'H':H,'Q':Q,'before':a,'after':z,'units':units,'demands':demands})
    old={tuple(x['demand']):tuple(x['unit']) for x in src['h0_full_own']}
    assert h0==old
    minimum=min(m['after'] for m in macros);cuts=[i for i,m in enumerate(macros) if m['after']==minimum]
    reports=[];full={};admitted=set();working=0
    for j,end in enumerate(cuts):
        start=(cuts[j-1]+1)%len(macros)
        mids=list(range(start,end+1)) if start<=end else list(range(start,len(macros)))+list(range(end+1))
        ms=[macros[k] for k in mids]
        assert ms[0]['before']==ms[-1]['after']==minimum
        H=sum(m['H'] for m in ms);Q=sum(m['Q'] for m in ms);assert 2*H>=Q
        groupunits=[u for m in ms for u in m['units']];groupdem=[d for m in ms for d in m['demands']]
        owns={d:h0[d] for d in groupdem if d in h0};inv={u:d for d,u in owns.items()}
        events=[]
        for k in range(0,len(groupunits),2):
            pair=groupunits[k:k+2];assert len(pair)==2 and pair[0][:2]==pair[1][:2];events.append(pair)
        missing=collections.deque(d for d in groupdem if d not in owns);queue=collections.deque();trace=[]
        for pair in events:
            assert not admitted.intersection(pair);admitted.update(pair)
            queue.extend(u for u in pair if u not in inv);working=max(working,len(queue))
            for u in pair:
                if u in inv:
                    d=inv[u];assert d not in full;full[d]=u
            while missing and queue:
                d=missing.popleft();assert d not in full;full[d]=queue.popleft()
            if not missing:queue.clear()
            trace.append({'event':pair[0][:2],'working_after':len(queue)})
        assert not missing and not queue
        reports.append({'macro_indices':mids,'H':H,'Q':Q,'Psi_endpoint':minimum,'event_visits':trace})
    U={(r['t'],j,b) for r in rows for j in range(1,r['a']+1) for b in (0,1)}
    D={(r['t'],j) for r in rows for j in range(1,r['qF']+1)}
    assert admitted==U and set(full)==D and len(set(full.values()))==len(full)
    assert all(full[d]==u for d,u in old.items()) and working<=2
    review="""# Distinct review of JR35-N0

This is same-agent independent source checking and a separate mathematical
derivation, not external peer review or formal proof-assistant verification.

Recompute the local law without the global period identity: each A +/-
rotation changes Psi by +/-1; each nonneutral B double changes it by -1/-2,
and each decreasing B zig by -1. Subtract this local delta from the
actual price. What remains is (2H-P)+N+B2+Z1, termwise nonnegative.
The audit verifies this as a formal polynomial identity, not finite tests
standing in for arbitrary costs. The inequalities use original source
rotation facts proved in ND35, including anonymous duplicate labels.

The grouping chooses minimum-Psi GENUINE full boundaries before any
allocation is attempted. It has endpoints of equal source potential;
the local source laws telescope within each disjoint actual group.
This independently derives the grouped budget. Selecting every actual
unit includes the literal natural h0 owner inventory. Thus the inherited
static Type-B block constructor is applicable with D=0, c=H, K=0.
Its streamed bound depends on K, not group length or c. No source
causality at original demand times is asserted, and no already assigned
pair is hidden in the working bank.

Both endpoints must use the original C14 cyclic transport, including
the h0 map. This is an internal construction cut only, not a new legal
Step1 auxiliary cut. No event is borrowed across symbolic period copies.
The theorem licenses the independent h construction only. Additional
frozen fE reservation/chi compatibility is deliberately not asserted.

Check that the explicit g_plus alternative also extends h0: in a finite
union of two injections an h0-unmatched start cannot enter a cycle and,
when g_plus covers every demand, cannot terminate at another demand.
It must reach an h0-unowned actual unit. Two starts cannot merge.
This establishes an independent endpoint proof; its output need not be
the same matching as the block-streaming construction.

The accepted NONMAX original paired-closed control has B0=0; this audit
reuses its already checked source events/closure and independently
recomputes boundary labels, all local laws, grouping, exact original
unit IDs, immutable h0 values, full injection and bank. This control
already has complete h0, so it does NOT experimentally exercise a
nonlocal unpaid-demand branch. That branch is justified by the uniform
streaming proof above, not by this finite control.

No-neutral is a real restriction. AF and CCR have neutral doubles.
There is no proof here that arbitrary neutral-terminal liabilities
reach eligible bits. JR35, UCF35 and unconditional Gate U remain OPEN.
"""
    (F/'ZERO_NEUTRAL_PROOF_REVIEW.md').write_text(review,encoding='utf-8')
    result={'status':'PASS_RESTRICTED_JR35_N0_PROOF_REVIEW_AND_SOURCE_BIT_CONTROL',
      'source_queries':0,'source_engine_calls':0,'polynomial_identity':'EXACT',
      'source_control':'NONMAX','source_full_injection':[{'demand':d,'unit':u} for d,u in sorted(full.items())],
      'natural_h0_preserved':len(old),'working_bound_observed':working,'groups':reports,
      'fresh_source_replays':0,'universal_scope_from':'written symbolic proof, not control enumeration',
      'nonlocal_unpaid_branch_control':'NOT_EXERCISED','JR35':'OPEN','reservation':'DEFERRED',
      'input_sha256':{p.name:sha(p) for p in [F/'zero_neutral_funding_derivation.json',F/'ZERO_NEUTRAL_FULL_SOURCE_FUNDING.md',F/'independent_core_sector_neutral.json',sourcepath]},
      'review_sha256':sha(F/'ZERO_NEUTRAL_PROOF_REVIEW.md')}
    with (F/'independent_zero_neutral_funding.json').open('x',encoding='utf8') as f:json.dump(result,f,indent=2)
    print(json.dumps({k:v for k,v in result.items() if k not in ('groups','source_full_injection','input_sha256')}),flush=True)
    assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error=repr(ex);raise
    finally:
        with (B/'audit_verify125_exit.json').open('x',encoding='utf8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0},f)
