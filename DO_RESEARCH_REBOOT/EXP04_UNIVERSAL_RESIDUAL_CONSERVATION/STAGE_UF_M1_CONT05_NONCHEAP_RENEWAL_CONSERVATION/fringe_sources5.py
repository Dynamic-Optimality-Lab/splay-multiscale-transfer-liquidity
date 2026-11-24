from base5 import *
from sources2 import padded
from coercion import advance,coerce

def make(extra_encloser):
    old=padded(4,5);A=copy.deepcopy(old['initial_A']);B=old['initial_B'];low=old['low_guard'];high=old['high_guard'];m=old['critical_g'];M=old['max_core']
    for block in old['blocks']:
        ts=block['extra'];A['children'][str(block['p'])][1]=ts[-1]
        for i,x in enumerate(ts):A['children'][str(x)]=[ts[i-1] if i else None,None]
    body=[];critical=[]
    for block in reversed(old['blocks']):
        critical.append(len(body)+1);body += [['K',block['x']],['K',block['y']]]
        if extra_encloser:body.append(['K',block['z']])
    visit=[low]+list(range(m,high))[::-1]+[high,low]
    b,_=advance(B,[x for tag,x in body]+visit);back,bs=coerce(b,B)
    def guard(x):
        if x==low:return [['D',m],['K',x],['D',m]]
        if x==high:return [['D',M],['K',x],['D',M]]
        return [['K',x]]
    ops=body+[z for x in visit+back for z in guard(x)];a,_=advance(A,[x for tag,x in ops])
    def core(st):return {'root':st['root'],'children':{j:[None if x in (low,high) else x for x in cs] for j,cs in st['children'].items() if int(j) not in (low,high)}}
    assert a['children'][str(m)][0]==low and a['children'][str(M)][1]==high
    ret,ars=coerce(core(a),core(A));ops += [['D',x] for x in ret]
    assert advance(A,[x for tag,x in ops])[0]==A and advance(B,[x for tag,x in ops if tag=='K'])[0]==B
    prefix,ps=coerce(B,A)
    return {'name':f'M1C5_left_padding_extra_encloser{int(extra_encloser)}','family':'repeated_column_lower_cohort_repair',
        'n':high,'k':4,'L':5,'initial_A':A,'initial_B':B,'diagonal_initial':B,'reaching_prefix':[['D',x] for x in prefix],
        'operations':ops,'critical_operations':critical,'creator_operation':critical[1],'critical_operation':critical[2],
        'extra_encloser':extra_encloser,'protected_labels':[],'B_return_statistics':bs,'A_repair_statistics':ars,'prefix_statistics':ps,
        'scope':'Left-vine A fringe repair; original cyclic exposure and all predicates must be independently recomputed.'}

if __name__=='__main__':
    m=Meter('left_fringe_planning');ss=[make(False),make(True)];write('FRINGE_SOURCE_CATALOG.json',ss);m.ok=True
    print('PLANNED2 exact left-fringe cohort repair sources',flush=True)
