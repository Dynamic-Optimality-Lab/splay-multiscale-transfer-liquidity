"""Complete original sources with explicitly selected adversarial feature rows."""
import time
from kernel import HERE,ROOT,PARAM,SOURCES,dump,load,selected_replay


def source_population():
    result=[];seen=set()
    parameters=[PARAM.H(p,5) for p in range(1,11)]
    parameters += [PARAM.H(3,q) for q in (1,17,65,257)]
    parameters += [PARAM.H(p,17) for p in (5,6)]
    parameters += [PARAM.compressed(q) for q in (1,5,17,65)]
    parameters += [PARAM.family(s,k) for s in (2,5) for k in ('F1','F2','F3')]+[PARAM.F4(s) for s in (2,5)]
    assert len(parameters)<=32
    for source in parameters:
        if source['name'] in seen:continue
        seen.add(source['name']);word=source['operations'];m=len(word);n=len(source['initial_A']['children'])
        if source['name'].startswith('F'):selected=set(range(1,m+1))
        elif source['name'].startswith('compressed'):
            selected=set(range(n,n+4))|set(range(n+4,min(m,n+30)+1))
        else:
            p=source['p'];selected={n-1+2**j for j in range(p+1)}|set(range(2*n,2*n+18))
        selected|={1,m};selected.update(1+j*(m-1)//31 for j in range(32));selected={i for i in selected if 1<=i<=m}
        result.append((source,selected,'parameterized',None))
    old=load(ROOT/'DO_RESEARCH_REBOOT/GLOBAL_ACCOUNTING_SYNTHESIS_20261121_V001/AUDIT_RESULTS.json')
    for item in old['cases']:
        if not item['label'].startswith('control_'):continue
        raw=load(ROOT/('DO_RESEARCH_REBOOT/GLOBAL_ACCOUNTING_SYNTHESIS_20261121_V001/'+item['label']+'.json.gz'))
        s=raw['source'];m=len(s['operations']);selected=set(range(1,min(m,24)+1))|set(range(max(1,m-12),m+1))
        selected.update(1+j*(m-1)//63 for j in range(64));selected.update(z['op'] for z in raw['rows'])
        result.append((s,selected,'historical',item.get('source_ref')))
    return result


def build_sources(out):
    start=time.process_time();summary=[];allrows=[];rotations=0
    for i,(source,selected,kind,ref) in enumerate(source_population()):
        path=out/f'source_{i:02d}.json.gz'
        if path.exists():w=load(path);assert w['source']==source
        else:w=selected_replay(source,selected);dump(path,w)
        rotations+=w['period_rotations'];assert rotations<=3000000 and time.process_time()-start<=360
        allrows.extend(w['rows']);assert len(allrows)<=10000
        record={'file':path.name,'name':source['name'],'N':len(source['initial_A']['children']),'operations':len(source['operations']),'A':w['A'],'Q_B':w['Q_B'],'selected_rows':len(w['rows']),'period_rotations':w['period_rotations'],'kind':kind,'source_ref':ref}
        summary.append(record);print(record['name'],record['N'],record['selected_rows'],flush=True)
    dump(out/'SOURCE_SUMMARY.json',{'cases':summary,'sources':len(summary),'selected_rows':len(allrows),'period_rotations':rotations,'cpu_seconds':time.process_time()-start,'scope':'Complete original periods and selected feature rows. Selected rows are sufficient to refute a candidate, never to certify universal success.'})
    return allrows


def holdouts(out):
    result=[]
    for q in (2,3,129,257):
        path=out/f'holdout_compressed_q{q}.json.gz'
        if path.exists():w=load(path)
        else:
            s=PARAM.compressed(q);n=len(s['initial_A']['children']);w=selected_replay(s,{n+15});dump(path,w)
        result.append({'source':w['source']['name'],'selected_row':w['rows'][0]['id'],'a':w['rows'][0]['a'],'q':w['rows'][0]['q'],'delta':w['rows'][0]['delta']})
    dump(out/'HOLDOUT_OBSERVATIONS.json',{'scope':'Finite observations only. A fixed restoration index does not have one inferred affine all-q formula. No universal claim is made from these changing patterns.','cases':result})
    return result
