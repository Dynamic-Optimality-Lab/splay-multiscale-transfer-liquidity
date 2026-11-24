"""Read-only canonical source extraction; no previous replay engine is called."""
import gzip
import json
from functools import lru_cache
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent


@lru_cache(maxsize=1)
def read(path):
    with (gzip.open(path,'rt',encoding='utf-8') if path.suffix=='.gz' else path.open(encoding='utf-8')) as f:
        return json.load(f)


def state_from_tuple(t):
    out={};stack=[t]
    while stack:
        x=stack.pop()
        if x is None:continue
        k,l,r=x
        out[str(k)]=[l[0] if l else None,r[0] if r else None]
        stack.extend((l,r))
    return {'root':t[0],'children':out}


def vine(n,mirror=False):
    return {'root':n if mirror else 1,'children':{str(k):[k-1 if k>1 else None,None] if mirror else [None,k+1 if k<n else None] for k in range(1,n+1)}}


def canonical(ref):
    if ref['kind']=='generated':return read(HERE/ref['file'])
    o=read(ROOT/ref['path'])
    if ref['kind']=='historical':
        entries=o['sources'] if isinstance(o,dict) else o
        s=next(x for x in entries if x['name']==ref['name'])
        return {'name':ref['name'],'initial_A':s['initial_A'],'initial_B':s['initial_B'],
                'operations':s['operations'],'prefix':s.get('reaching_prefix',[]),
                'diagonal':s.get('diagonal_initial'),
                'expected_A':s.get('A',s.get('costs',{}).get('A')),
                'expected_Q':s.get('Q_B',s.get('costs',{}).get('Q_B'))}
    if ref['kind']=='sealed':
        s=o['source']
        if s.get('family')=='H_pq':
            initial=vine(s['n'],s['reflected'])
        else:initial=state_from_tuple(s['initial'])
        return {'name':ref['name'],'initial_A':initial,'initial_B':initial,
                'operations':[[mode,x] for _,mode,x in s['word']],
                'prefix':[],'diagonal':initial,'expected_A':o['result'].get('A'),'expected_Q':o['result'].get('Q_B')}
    raise ValueError(ref)


def references():
    result=[]
    for relative in ['EXP01_PHYSICAL_RESIDUAL_DISCOVERY/EXP01_SOURCE_WITNESSES.json',
                     'EXP04_UNIVERSAL_RESIDUAL_CONSERVATION/EXP04_ADVERSARIAL_SOURCES.json',
                     'EXP04_UNIVERSAL_RESIDUAL_CONSERVATION/EXP04_SPARSE_SOURCES.json']:
        p='DO_RESEARCH_REBOOT/'+relative;o=read(ROOT/p)
        ss=o['sources'] if isinstance(o,dict) else o
        result.extend({'kind':'historical','path':p,'name':s['name']} for s in ss)
    for dirname,pattern in [('INTERNAL_LIFECYCLE_20261121_V001','*complete_witness.json'),
                            ('INTERLEAVED_MULTISCALE_20261121_V001','*complete_witness.json'),
                            ('COVER_FLOW_AUDIT_20261121_V001','H_*.json.gz')]:
        for path in sorted((ROOT/'DO_RESEARCH_REBOOT'/dirname).glob(pattern)):
            result.append({'kind':'sealed','path':path.relative_to(ROOT).as_posix(),'name':path.name.removesuffix('.json.gz').removesuffix('_complete_witness.json')})
    assert len(result)==209
    return result
