from campaign3 import *


BATCHES=[('SCALING_SOURCES.json','SCALING_RESULTS.json'),('REPEAT_ATTACK_SOURCES.json','REPEAT_ATTACK_RESULTS.json'),
         ('REPEAT_HELPER_SOURCES.json','REPEAT_HELPER_RESULTS.json'),('RETARGET_SOURCES.json','RETARGET_RESULTS.json'),
         ('FAR_RETARGET_SOURCES.json','FAR_RETARGET_RESULTS.json')]


def collect():
    ss=[];rows={};provenance={}
    for sf,rf in BATCHES:
        sources=json.loads((ROOT/sf).read_text());zs=json.loads((ROOT/rf).read_text())
        assert len(sources)==len(zs)
        for s,z in zip(sources,zs):
            assert s['name']==z['source'] and s['A']==z['A'] and s['Q_B']==z['Q_B']
            ss.append(s);rows[s['name']]=z;provenance[s['name']]={'source_batch':sf,'result_batch':rf}
    assert len(ss)==len(rows)==17
    return ss,rows,provenance
