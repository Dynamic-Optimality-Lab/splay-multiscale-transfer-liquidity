from stage5 import *
from fast_physics import physical_replay
from ledger5 import audit
from forest5 import forest
from packed_states import install

def list_archive(p):
    x=load(p)
    if isinstance(x,list):return x
    return x.get('sources',x.get('inherited_sources',[])+x.get('new_sources',[]))

if __name__=='__main__':
    meter=Meter('challenge')
    ep=REPO/'DO_RESEARCH_REBOOT'
    p1=ep/'EXP01_PHYSICAL_RESIDUAL_DISCOVERY/EXP01_SOURCE_WITNESSES.json'
    p3=ep/'EXP03_FINAL_R6_ESCAPE_CONSERVATION/EXP03_SOURCE_WITNESSES.json'
    pb=BASE/'CONT03B_PACKET_OBSTRUCTIONS/DILATED_PACKET_SOURCES.json'
    a1=list_archive(p1)
    cases=[(next(s for s in a1 if s['name']==nm),p1) for nm in
           ['G_4_1_L31_r1_z1','DH_4_1_at31_c1','DW_5_1_at31','DW_6_1_at31']]
    cases += [(next(s for s in list_archive(p3) if s['name']=='mixed_p5_Gcopies2'),p3),
              (list_archive(pb)[-1],pb)]
    new=ROOT/'SOURCE_WITNESSES.json'
    cases += [(s,new) for s in list_archive(new) if len(s['initial_B']['children'])<100]
    pool,restore=install(inherited.Tree);rows=[]
    try:
        for s,p in cases:
            r=inherited.Replay(s);ft=forest(r)
            a=audit(r,r.doubles,mode='promotion')
            eligible=set()
            if r.S==set(r.keys):
                f=physical_replay(s);xs=[x for tag,x in s['operations'] if tag=='K']
                raw=sum((x!=xs[i-1])+abs(x-xs[i-1]).bit_length() for i,x in enumerate(xs))
                if raw<=10*r.A:eligible={z['t'] for z in f['rows'] if z.get('guard_H',False)}
            b=audit(r,r.doubles,mode='promotion',prefix_payment=True,protected_paid_ops=eligible)
            rows.append({'source':s['name'],'archive':str(p),'source_sha256':digest(s),
                'complete_source_replayed':True,'A':r.A,'Q_B':r.Q,
                'scope':'Diagnostic pool all original B doubles, NOT the frozen residual tail.',
                'actual_root_count':ft['roots'],'maximum_forest_depth':ft['maximum_depth'],
                'last_promotion_classes':a['counts'],'additional_priced_classes':b['counts'],
                'selected_restore_examples':{k:next(z for z in a['rows'] if z['classification']==k)
                   for k in a['counts'] if k not in ('A_reset','continuous_retention')},
                'example_overlapping_branch':next(iter(ft['overlapping_child_frames']),None)})
            write('CHALLENGE_RESULTS.json',rows)
            print('PASS',s['name'],r.A,r.Q,a['counts'],flush=True)
            del r,ft,a,b;pool.clear()
    finally:restore()
    meter.success=True
