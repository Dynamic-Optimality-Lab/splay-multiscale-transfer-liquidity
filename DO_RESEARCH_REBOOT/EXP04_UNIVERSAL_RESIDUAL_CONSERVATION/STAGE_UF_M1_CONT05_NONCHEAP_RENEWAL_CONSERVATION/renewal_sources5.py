from base5 import *
from sources2 import padded
from coercion import advance,coerce

def make(k,L,tour):
    old=padded(k,L);low=old['low_guard'];high=old['high_guard'];m=old['critical_g'];M=old['max_core']
    body=old['operations'][:2*k]
    corekeys=list(range(m,high))
    if tour=='descending':corekeys.reverse()
    elif tour=='groups':corekeys=[x for i in range(0,len(corekeys),4) for x in reversed(corekeys[i:i+4])]
    else:raise ValueError(tour)
    visit=[low]+corekeys+[high,low]
    b,_=advance(old['initial_B'],[x for tag,x in body]+visit);back,bs=coerce(b,old['initial_B'])
    def guarded(x):
        if x==low:return [['D',m],['K',x],['D',m]]
        if x==high:return [['D',M],['K',x],['D',M]]
        return [['K',x]]
    ops=body+[p for x in visit+back for p in guarded(x)]
    a,_=advance(old['initial_A'],[x for tag,x in ops])
    def core(st):return {'root':st['root'],'children':{j:[None if x in (low,high) else x for x in cs] for j,cs in st['children'].items() if int(j) not in (low,high)}}
    assert a['children'][str(m)][0]==low and a['children'][str(M)][1]==high
    repair,ars=coerce(core(a),core(old['initial_A']));ops += [['D',x] for x in repair]
    assert advance(old['initial_A'],[x for tag,x in ops])[0]==old['initial_A']
    assert advance(old['initial_B'],[x for tag,x in ops if tag=='K'])[0]==old['initial_B']
    return {'name':f'M1C5_repeated_chain_k{k}_L{L}_{tour}','family':'repeated_C_old_packet_enrichment_attempt',
        'k':k,'L':L,'n':high,'initial_A':old['initial_A'],'initial_B':old['initial_B'],'diagonal_initial':old['diagonal_initial'],
        'reaching_prefix':old['reaching_prefix'],'operations':ops,'critical_operations':old['critical_operations'],
        'creator_operation':1,'critical_operation':5,'protected_labels':[],
        'B_return_statistics':bs,'A_repair_statistics':ars,'tour':tour,
        'scope':'True repeated old-g chain; new future support tour, original predicates and frozen accounting recomputed.'}

if __name__=='__main__':
    m=Meter('renewal_packet_planning');ss=[make(4,5,'descending'),make(8,5,'descending'),make(4,5,'groups'),make(4,9,'descending')]
    write('RENEW_SOURCE_CATALOG.json',ss);m.ok=True
    print('PLANNED4 complete repeated-column future-tour deformations',flush=True)
