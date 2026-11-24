from core import *


def periodic_cost(targets,J):
    if not targets:return {'cyclic_blocks':0,'cyclic_integer_rank_travel':0,'B_cyclic':0}
    rank={x:i for i,x in enumerate(sorted(J))}
    m=sum(x!=targets[i-1] for i,x in enumerate(targets))
    L=sum(abs(rank[x]-rank[targets[i-1]]).bit_length() for i,x in enumerate(targets))
    return {'cyclic_blocks':m,'cyclic_integer_rank_travel':L,'B_cyclic':m+L}


def from_normalization(norm):
    assert norm['initial_B']==norm['ending_B']
    z=periodic_cost(norm['targets'],norm['J']);z.update(A=norm['A'],
        original_retained_Q=norm['retained_actual_Q'],eligible_B_cyclic_le_10A=z['B_cyclic']<=10*norm['A'])
    return z


if __name__=='__main__':
    meter=Meter('CONT01_periodic_initialization_cancellation');out=[]
    for row in json.loads((ROOT/'GUARDED_RETURN_RESULTS.json').read_text()):
        out.append({'source':row['source'],'variant':'G','cut_before':1,
                    **from_normalization(row['normalized_full_period'])})
    for row in json.loads((ROOT/'KEEP_GAP_PAYMENT_RESULTS.json').read_text()):
        out.append({'source':row['source'],'variant':'H','cut_before':1,
                    **from_normalization(row['hard_guarded_full_period'])})
    if (ROOT/'INTRINSIC5_RESULTS.json').exists():
        row=json.loads((ROOT/'INTRINSIC5_RESULTS.json').read_text())
        for variant,key in [('G','normalized'),('H','hard_normalized')]:
            out.append({'source':row['source'],'variant':variant,'cut_before':1,
                        **from_normalization(row[key])})
    write('PERIODIC_PAYMENT_RESULTS.json',out)
    for row in out:print(row['source'],row['variant'],'cyclic cost',row['B_cyclic'],'A',row['A'],flush=True)
    meter.success=True
