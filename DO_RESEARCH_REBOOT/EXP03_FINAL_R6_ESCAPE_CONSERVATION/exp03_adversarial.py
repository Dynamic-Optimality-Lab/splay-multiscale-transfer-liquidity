from exp03_experiments import *
from exp03_sources import additional_corpus,separated_private


if __name__=='__main__':
    meter=Meter('adversarial')
    archive=json.loads((ROOT/'EXP03_SOURCE_WITNESSES.json').read_text())
    results=json.loads((ROOT/'EXP03_CAUSAL_EPISODE_RESULTS.json').read_text())
    sources=additional_corpus();names={s['name'] for s in archive['new_sources']}
    assert not names.intersection(s['name'] for s in sources)
    assert len(sources)+len(names)<=100
    checks=0
    for i,s in enumerate(sources):
        r=Replay(s);c=current_classification(r);z=analyze(r,c)
        s.update(trace_hash=digest(r.events),A=r.A,Q_B=r.Q)
        archive['new_sources'].append(s);results['new_sources'].append(z);checks+=r.independent_checks
        print(i+1,s['name'],'A',r.A,'Q',r.Q,'unhandled',dict(Counter(e['type'] for e in c['unhandled'])),
            'lossload',z['last_loss_selector']['maximum_primitive_load'],'undefined',z['last_loss_selector']['undefined_parents'],flush=True)
        write('EXP03_SOURCE_WITNESSES.json',archive);write('EXP03_CAUSAL_EPISODE_RESULTS.json',results)
    rejected=separated_private(1)
    a=Tree(rejected['initial_A']);b=Tree(rejected['initial_B'])
    for tag,x in rejected['operations']:
        Replay.plain_splay(a,x)
        if tag=='K':Replay.plain_splay(b,x)
    assert a.state()==rejected['initial_A'] and b.state()!=rejected['initial_B']
    write('EXP03_REJECTED_CONSTRUCTIONS.json',{'sources':[{'source':rejected,'actual_closing_A':a.state(),'actual_closing_B':b.state(),
        'reason':'Mapped even-key core restores A but changes complete B; not an admissible paired-closed period. Excluded from all theorems/counts.'}],
        'failed_pilots':'outside_pilot: missing summary metadata; restart_pilot: dict/value instrumentation mismatch; no independent engine mismatch'})
    meter.details.update(new_sources=len(sources),independent_original_operations=checks);meter.success=True
