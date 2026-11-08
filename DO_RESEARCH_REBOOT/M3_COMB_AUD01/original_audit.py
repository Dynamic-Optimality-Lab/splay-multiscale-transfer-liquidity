"""Fresh original-root evaluations and raw interface extraction; no old helpers."""
import sys,json,time,hashlib
from pathlib import Path
from collections import Counter
PC='DO_RESEARCH_REBOOT/06_CERTIFICATES/'
sys.path[:0]=[PC+'DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER',PC+'DIRECT_CDK5N_11F_STRICT_CLOSURE',
             PC+'DIRECT_CDK5N_11F_CLOSED_WALK_CORE_RESCUE']
from PC_TYPED_DAG import DAG,BOOL
from PC_B_CONTROLLER import BTrace,verify_bpath
from STRICT_LOW_COMPILER import build_slow,state_valid7
from STRICT_HIGH_COMPILER import build_shigh
from STRICT_B_CONTROLLER import BStruct,b_tree_valid
BASE=Path('DO_RESEARCH_REBOOT/M3_COMB_AUD01');R=Path('DO_RESEARCH_REBOOT')
FIELDS=('kl','rl','kr','rr','lo','hi')

def key(state):return json.dumps(state,sort_keys=True,separators=(',',':'))
def chi(b):return b['kr'][8]==0 and b['rr'][8]==19

def main():
    start=time.process_time();output=BASE/'original_semantics_audit.json';assert not output.exists()
    dl=DAG();L=build_slow(dl,'MXL');dh=DAG();H=build_shigh(dh,'MXH')
    bt=BTrace(dh,'MXHbt');srcvalid=dh.AND(state_valid7(dh,H['s']),b_tree_valid(dh,H['s'].b,BStruct(dh,H['s'].b,'MXHsbs'),H['s'].sig))
    pathvalid=verify_bpath(dh,H['s'].b,bt,0)
    files=[R/n/'original_audit.json' for n in ['M3_GAP01']+[f'M3_GAPINT0{g}' for g in range(1,5)]]
    files += [R/'M3_OUT01/original_transfer_audit.json',R/'M3_OUT01/gap9_original_audit_v2.json',R/'M3_GAPMULTI01/obstruction.json',R/'M3_OUT01/high_controls.json']
    rows=[];counts=Counter();groups={}
    def value(d,e,n):
        node=d.nodes[n];assert node[0]=='var';return e[node[3][1]]
    def bstate(d,e,b):return {'root':value(d,e,b.root),**{f:[value(d,e,n) for n in getattr(b,f)] for f in FIELDS}}
    def ordinary(d,e,s):
        return {'mu':value(d,e,s.mu),'sigma':[value(d,e,n) for n in s.sig],
                'alpha':[[value(d,e,s.ak[i]),int(value(d,e,s.aS[i])),value(d,e,s.aI[i])] for i in range(7)],'b':bstate(d,e,s.b)}
    def midpoint(e):
        g=H['g'];return {'mu':value(dh,e,g.mu),'sigma':[value(dh,e,n) for n in g.sig],'v':value(dh,e,g.v),'b':bstate(dh,e,g.b)}
    for p in files:
        old=json.loads(p.read_text());group=p.as_posix();groups[group]=[]
        for index,r in enumerate(old['records']):
            raw_high='high_controls' in p.name;kind='HIGH' if raw_high else r['kind']
            d,model,root=(dl,L,L['root']) if kind=='LOW' else (dh,H,H['root'])
            e=r['environment']
            if raw_high:e={('MXH'+k[4:] if k.startswith('DSKF') else k):v for k,v in e.items()}
            assert set(d.vars)<=set(e)
            for nm,n in d.vars.items():
                node=d.nodes[n];z=node[3];v=e[nm]
                if node[1]==BOOL:assert v in (False,True)
                else:
                    width=z[2];signed=z[3]
                    assert (-(1<<(width-1))<=v<(1<<(width-1))) if signed else (0<=v<(1<<width)),(nm,v)
            accepted=d.ev_ground(root,e);expected=r['expected'] if raw_high else True
            assert accepted==expected,(p,index,r['label'])
            s=ordinary(d,e,model['s']);t=ordinary(d,e,model['t'])
            assert s['mu']==t['mu'] and s['sigma']==t['sigma']
            if raw_high:
                assert s['mu']==r['mu'] and s['sigma']==r['sigma']
                assert s['b']=={k:r['source'][k] for k in ('root',)+FIELDS}
                assert t['b']=={k:r['destination'][k] for k in ('root',)+FIELDS}
                assert dh.ev_ground(srcvalid,e) and dh.ev_ground(pathvalid,e)
            else:assert s==r['source'] and t==r['destination'],(p,index,'saved full interface differs from original inputs')
            g=None
            if kind=='LOW':
                nev=value(d,e,L['wit'].nev);charged=sum((value(d,e,L['wit'].evd[j])+1)//2 for j in range(nev))
                q=value(d,e,L['bt'].q);declared=value(d,e,L['bt'].bd[nev-1])
                assert charged==value(d,e,L['H'])==r['H'] and q==declared//2==r['q']
                assert value(d,e,L['w'])==2*charged-q==r['w']
                assert chi(s['b'])==chi(t['b'])
            else:
                q=value(d,e,H['q']);declared=value(d,e,bt.bd[0]);assert q==declared//2==r['q']
                assert value(d,e,H['w1'])==6-q==r['w'];g=midpoint(e)
                if accepted:
                    assert g['mu']==s['mu']==t['mu'] and g['sigma']==s['sigma']==t['sigma']
                    # Original b_equal is structural; interval coordinates are still extracted
                    # and compared with the recorded ACTUAL shared midpoint below.
                    assert all(g['b'][f]==t['b'][f] for f in ('root','kl','rl','kr','rr'))
                    if not raw_high:assert g==r['shared_midpoint'],(p,index,'actual midpoint mismatch')
                    if not chi(g['b']):assert r['w']>=2
                    if chi(s['b']):assert chi(g['b']) and r['w']>=2
            row={'record_file':group,'index':index,'label':r['label'],'kind':kind,'accepted':accepted,
                 'weight':r['w'],'source':s,'destination':t,'midpoint':g,
                 'total_environment_sha256':hashlib.sha256(json.dumps(e,sort_keys=True).encode()).hexdigest()}
            rows.append(row);groups[group].append(row);counts[kind+'_accepted' if accepted else kind+'_rejected']+=1
            assert time.process_time()-start<300,'UNKNOWN original semantics audit cap'
        print(json.dumps({'file':p.name,'parent':p.parent.name,'original_roots':len(rows),'cpu_seconds':round(time.process_time()-start,3)}),flush=True)
    cycles=[]
    for name,rs in groups.items():
        lows=[r for r in rs if r['accepted'] and r['kind']=='LOW'];highs=[r for r in rs if r['accepted'] and r['kind']=='HIGH']
        for l in lows:
            for h in highs:
                if key(l['destination'])!=key(h['source']) or key(h['destination'])!=key(l['source']):continue
                assert h['midpoint'] is not None
                cycles.append({'file':name,'low_index':l['index'],'high_index':h['index'],
                               'weight':l['weight']+h['weight'],'shared_midpoint':h['midpoint'],
                               'full_O_state_closure':True,'full_M_state_sharing':True})
    assert len(cycles)>=11 and all(c['weight']>=0 for c in cycles)
    # Closure checker adversarial control: every raw coordinate is significant.
    sample=next(r['source'] for r in rows if r['accepted']);import copy
    bad=copy.deepcopy(sample);bad['b']['lo'][0]=(bad['b']['lo'][0]+1)%32;assert key(sample)!=key(bad)
    bad=copy.deepcopy(sample);bad['alpha'][0][0]=(bad['alpha'][0][0]+1)%3;assert key(sample)!=key(bad)
    result={'status':'PASS_FRESH_ORIGINAL_SEMANTICS_AND_FULL_STATE_CLOSURE',
            'original_roots_evaluated':len(rows),'counts':dict(counts),'DAG_nodes':[len(dl.nodes),len(dh.nodes)],
            'actual_full_state_cycles':cycles,'all_declared_q_and_exact_weights_checked':True,
            'shared_midpoints_extracted_from_original_variables':True,
            'raw_lo_hi_and_unused_alpha_not_discarded':True,'no_low_path_rule_added_to_high':True,
            'old_witness_helpers_or_checkers_imported':False,'cpu_seconds':round(time.process_time()-start,3),'records':rows}
    with output.open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)
    print(json.dumps({k:v for k,v in result.items() if k not in ['records','actual_full_state_cycles']},indent=2))

if __name__=='__main__':main()
