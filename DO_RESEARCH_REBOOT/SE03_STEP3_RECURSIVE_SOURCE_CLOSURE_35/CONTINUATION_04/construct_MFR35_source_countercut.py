"""Literal closed B plus canonical original A preparation counterconstruction.

Only accepted native11 primitives via the arbitrary non-target-leaf identity
are substituted. No original source engine call or finite tree catalogue.
"""
import hashlib,json,pickle,sys,time
from pathlib import Path
F=Path(__file__).resolve().parent;P=F.parents[1];B=P/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
sys.path.insert(0,str(F));import ranked_source_bst as R
CAP=float(sys.argv[1]);START=time.process_time()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def N(k,l=None,r=None):return (k,l,r)
def vine(a,b,right=True):
    t=None
    for k in (range(b,a-1,-1) if right else range(a,b+1)):t=N(k,None,t) if right else N(k,t,None)
    return t
def path(t,x):
    p=[]
    while True:
        p.append(t[0])
        if t[0]==x:return p
        t=t[1] if x<t[0] else t[2]
def inverse(anc):
    if not anc:return []
    return [anc[0]]+[z for y in inverse(anc[1:]) for z in (y,anc[0])]
def allkeys(t):return [] if t is None else allkeys(t[1])+[t[0]]+allkeys(t[2])
def main():
    with (F/'probe11_source_actions.pkl').open('rb') as f:old=pickle.load(f)
    lift=R.Lift(old);m=3;size=6*m+3;y=2*m+1;marks=set(range(1,size+1,2));g=2*m-1
    B0=N(g,vine(1,g-1,False),N(y+1,N(y-1,None,N(y)),vine(y+2,size)))
    Bprev,h,q=lift.action(B0,size,g-2);assert (h,q)==(1,1)
    forward=[z for i in range(m,0,-1) for z in (2*i-1,6*m+7-4*i)]+[y]+list(range(1,2*m,2))
    expect=[1,3,2,3,2,3,4,1,2,2];current=Bprev;rows=[];original=[];inverse_word=[]
    def action(x,role):
        nonlocal current
        before=current;pp=path(before,x);depth=len(pp)-1;assert depth>0 and depth%2==0
        for j in range(len(pp)-3,-1,-2):
            G,P0=pp[j:j+2];assert G in marks and P0 not in marks and ((x<G and x<P0) or (x>G and x>P0))
        current,h,q=lift.action(before,size,x);assert h==q==depth//2
        core=set().union(*(set(path(current,z)) for z in marks));assert core==set(range(1,size+1))
        row={'B_ordinal':len(rows)+1,'target':x,'before':before,'after':current,'Q':q,'role':role,
          'old_marked_grandparents_root_order':pp[:-1:2]};rows.append(row);return row
    for x,qq in zip(forward,expect):
        row=action(x,'forward');assert row['Q']==qq;original.append(row)
    for orig in reversed(original):
        assert current==orig['after'];ww=inverse(orig['old_marked_grandparents_root_order'])
        assert len(ww)==2**orig['Q']-1
        beforeQ=sum(r['Q'] for r in rows)
        for x in ww:action(x,'inverse');inverse_word.append(x)
        assert current==orig['before'] and sum(r['Q'] for r in rows)-beforeQ==2**(orig['Q']+1)-orig['Q']-2
    assert current==Bprev and len(rows)==60 and sum(r['Q'] for r in rows)==100
    assert {r['target'] for r in rows}==marks and allkeys(Bprev)==list(range(1,size+1))
    critical=[]
    for stage,i in enumerate(range(m,0,-1)):
        G=2*i-1;X=6*m+7-4*i;P0=G+1;left=vine(1,G-1);middle=vine(G+2,X-1);right=vine(X+1,size)
        a=N(G,left,N(P0,None,N(X,middle,right)));out,H,_=lift.action(a,size,X)
        mid=N(P0,N(G,left,None),N(X,middle,right));want=N(X,N(P0,N(G,left,None),middle),right)
        assert H==1 and out==want and G in path(a,y)[:-1] and G not in path(mid,y)[:-1]
        br=original[2*stage+1];assert br['target']==X and br['Q']==3 and br['old_marked_grandparents_root_order'][0]==G
        critical.append({'stage':stage,'old_proxy':G,'consumer':X,'forward_B_ordinal':br['B_ordinal'],
          'demand_double_index':3,'H':H,'Q':3,'natural_h0_owned_double_indices':[1,2],
          'A_before':a,'A_first_rotation_after':mid,'A_after':out,'first_loss_bit':[f'X{G}',1,0],
          'Gamma_preparation':'canonical shortest original A-only word to A_before, ending BEFORE genuine KEEP(old_proxy)'})
    Ay=N(y,N(y-1,vine(1,y-2,False),None),vine(y+1,size));a,h,q=lift.action(Ay,size,y-1)
    assert (h,q)==(1,0) and a==N(y-1,vine(1,y-2,False),N(y,None,vine(y+1,size)))
    controls=[{'kind':'DELETE','target':y-1,'before':Ay,'after':a,'H':h}]
    for G in range(1,2*m,2):
        before=a;a,h,_=lift.action(a,size,G);assert y not in path(a,G)[:-1]
        controls.append({'kind':'KEEP','target':G,'before':before,'after':a,'H':h})
    reset_after=a
    # Check the selected FIRST direct groups on the literal B word. These
    # proxies have right-side demotions only at their own X and contact y
    # before their next genuine reset; all intervening opposite-side targets
    # cannot share the X event's rightward ancestor loss.
    for c in critical:
        G=c['old_proxy'];start=next(j for j,r in enumerate(original) if r['target']==G)
        stop=next(j for j in range(2*m+1,len(original)) if original[j]['target']==G)
        right_demotions=[]
        for r in original[start+1:stop]:
            if G in r['old_marked_grandparents_root_order'] and r['target']>G:right_demotions.append(r['target'])
        assert right_demotions==[c['consumer'],y]
        c['next_group_contact']=y;c['next_proxy_reset_forward_ordinal']=stop+1
    out={'status':'PRODUCER_SOURCE_EXACT_ALL_MFR_RETURN_COUNTERCUT','m':m,'physical_keys':list(range(1,size+1)),
      'genuine_marks':sorted(marks),'initial_common_Bprev':Bprev,'B0_after_first_genuine5':B0,
      'forward_word':forward,'inverse_word':inverse_word,'full_B_rows':rows,'full_B_Q':100,'genuine_macros':60,
      'critical_unpaid_claims':critical,'contact_y':y,'A_contact_before_KEEP':Ay,'post_contact_A_controls':controls,
      'A_after_low_resets':reset_after,
      'original_word_spec':['Gamma(Bprev,A_before_G5); KEEP5; KEEP13',
        'Gamma(A_after13,A_before_G3); KEEP3; KEEP17','Gamma(A_after17,A_before_G1); KEEP1; KEEP21',
        'Gamma(A_after21,Ay); KEEP7; DELETE6; KEEP1; KEEP3; KEEP5',
        'KEEP(inverse_word); Gamma(A_v,Bprev)'],
      'Gamma':'shortest ordinary bottom-up access word, lexicographic tie-break, all letters original DELETE; existence by accepted n>=4 transformation theorem',
      'A_v':'actual ordinary A result of all literal inverse_word KEEPs from A_after_low_resets; symbolically specified, not numerically expanded',
      'paired_closure':'repeat this exact A/full-B-closed word; erase genuine9; true erased BST and actual finite charts choose their first recurrence after warmup, as accepted source bridge; numeric u,L not replayed',
      'absolute_ids':{'consumer_stage_j':'b + sum(ell_h,h=0..j) + 2(j+1), j=0,1,2','contact_y':'b+sum(ell_h,h=0..3)+7',
        'sole_return_event_c':'contact_y+1','reset_Gi':'c+i for Gi=2i-1'},
      'all_return_cut':{'demands':[[f'X{c["old_proxy"]}',3] for c in critical],
        'full_event_neighborhood':[['c',1,0],['c',1,1]],'deficiency':1,
        'exhaustion':'DELETE6 is the only actual pivot7 loss of any old proxy1,3,5 before its next genuine reset; all later accesses until resets are<7 and leave the entire 7-right-subtree rigid'},
      'not_a_CD_counterexample':True,'CD_margin_lower_bound':20,'actual_Gamma_costs_retained':True,
      'source_queries':0,'source_engine_calls':0,'source_leaf_substitutions':lift.substitutions,'JR35':'OPEN',
      'input_sha256':{str(p):sha(p) for p in (F/'probe11_source_actions.pkl',F/'independent_probe11_source_actions.json',
        B/'OFF_PATH_LEAF_SOURCE_LIFT.md',B/'UNIFORM_A_REALIZATION_OVER_CLOSED_B.md',F/'construct_MFR35_source_countercut.py')}}
    with (F/'MFR35_unpaid_source_countercut.json').open('x',encoding='utf8') as f:json.dump(out,f,indent=2)
    print(json.dumps({'status':out['status'],'BF_word_length':len(rows),'Q':100,'critical_claims':len(critical),'units':2,'deficiency':1,'source_queries':0,'JR35':'OPEN'}),flush=True)
    assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error=repr(ex);raise
    finally:
        with (B/'audit_core66_exit.json').open('x',encoding='utf8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0},f)
