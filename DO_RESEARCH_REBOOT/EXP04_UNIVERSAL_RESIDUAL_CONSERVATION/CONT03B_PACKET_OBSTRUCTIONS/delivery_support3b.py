from campaign3b import *


BATCHES=[('WARM_SOURCES.json','WARM_RESULTS.json'),('PAIR_SOURCES.json','PAIR_RESULTS.json'),
         ('COHORT_SOURCES.json','COHORT_RESULTS.json'),('NEUTRALITY_SOURCES.json','NEUTRALITY_RESULTS.json'),
         ('DILATED_PACKET_SOURCES.json','DILATED_PACKET_RESULTS.json'),('SCALED_SOURCE.json','SCALED_RESULT.json')]
BATCHES.append(('WIDTH_SOURCE.json','WIDTH_RESULT.json'))


def collect():
    sources=[];rows={};provenance={}
    for sf,rf in BATCHES:
        ss=json.loads((ROOT/sf).read_text());zs=json.loads((ROOT/rf).read_text())
        ss=ss if isinstance(ss,list) else [ss];zs=zs if isinstance(zs,list) else [zs]
        assert len(ss)==len(zs)
        for s,z in zip(ss,zs):
            assert s['name']==z['source']
            assert s['A']==z['A'] and s['Q_B']==z['Q_B']
            sources.append(s);rows[s['name']]=z;provenance[s['name']]={'source_batch':sf,'result_batch':rf}
    assert len(sources)==len(rows)==301
    return sources,rows,provenance
