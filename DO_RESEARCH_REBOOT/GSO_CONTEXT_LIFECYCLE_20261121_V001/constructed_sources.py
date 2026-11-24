"""Unbounded physical contexts, changing active keys, exact paired restoration."""
import json
import context as C
K=C.K


def changing_contexts(blocks,repetitions):
    assert blocks>=1 and repetitions>=1
    n=5*blocks;v=K.SOURCES.vine(n);base=K.load(C.PREVIOUS/'run_001/optimum_cycle_n5.json')['source'];word=[]
    for block in range(blocks):
        offset=5*block
        if offset:word.append(['K',offset+1])
        lift=lambda items:[[mode,x+offset] for mode,x in items]
        word+=lift(base['prefix'])
        for _ in range(repetitions):word+=lift(base['operations'])
        # These are actual counted original KEEPs, retaining every hanging
        # subtree. The active five-key skeleton returns to its right vine.
        word += [['K',offset+x] for x in range(1,6)]+[['K',offset+x] for x in range(4,0,-1)]
    word += [['K',x] for x in range(1,n+1)]+[['K',x] for x in range(n-1,0,-1)]
    return {'name':f'changing_contexts_b{blocks}_r{repetitions}','initial_A':v,'initial_B':v,'diagonal':v,'prefix':[],'operations':word,'recipe':{'blocks':blocks,'repetitions':repetitions,'all_physical_keys_genuinely_KEEP':True}}


def main():
    import source_audit as S
    out=C.HERE/'sources_001';result=[];start=len(list(out.glob('source_*.json.gz')))
    for i,(blocks,reps) in enumerate(((3,3),(9,7),(17,3)),start):
        s=changing_contexts(blocks,reps);z=S.audit(s);assert z['entire_source_boundary_core5'];assert len(z['original_S'])==5*blocks and 2*z['Q_B']<=3*z['A']
        C.write(out/f'source_{i:02d}.json.gz',z)
        row={'file':f'source_{i:02d}.json.gz','name':s['name'],'keys':5*blocks,'ops':z['operations'],'A':z['A'],'Q_B':z['Q_B'],'U':len(z['original_U']),'maximum_core':z['maximum_boundary_core'],'U_pre_core5':len(z['U_pre_core5']),'U_beyond_prefix':len(z['U_beyond_direct_A_gap_prefix']),'U_core5_beyond_prefix':len(z['core5_beyond_direct_prefix'])}
        result.append(row);print(json.dumps(row),flush=True)
    C.write(C.HERE/'CONSTRUCTED_CONTEXT_AUDIT.json',{'cases':result,'scope':'All-parameter source recipe and complete finite examples; no claim these escape older periodic or guarded certificates.'})


if __name__=='__main__':main()
