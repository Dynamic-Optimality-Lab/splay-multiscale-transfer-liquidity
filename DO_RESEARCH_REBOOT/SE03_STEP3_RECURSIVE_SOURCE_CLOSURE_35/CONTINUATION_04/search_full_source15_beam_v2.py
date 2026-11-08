"""Original fifteen-key sources; only source-valid maximal-core B steps.

The eight potential genuine B keys are odd. A helpers retain every key.
Beam pruning sacrifices search coverage. No positive universal claim.
"""
from pathlib import Path
p=Path(__file__).with_name('search_full_source13_beam_v2.py');s=p.read_text()
s=s.replace("exec(compile(s,str(Path(__file__).resolve()),'exec'))",'')
env={'__file__':str(p),'__name__':'source_builder_only'};exec(compile(s,str(p),'exec'),env);s=env['s']
s=s.replace('import ranked_source_bst as R','import ranked_source_bst15 as R')
s=s.replace('full_source13_beam_','full_source15_beam_')
s=s.replace('R.unrank(13,1,','R.unrank(15,1,').replace('R.rank_tree(out,1,13)','R.rank_tree(out,1,15)').replace('R.rank_tree(bt,1,13)','R.rank_tree(bt,1,15)')
s=s.replace('lift.action(ta,13,','lift.action(ta,15,').replace('lift.action(tb,13,','lift.action(tb,15,')
a="    if BATCH in (1,2):\n        with (F/'ranked13_LOW_search_01.pkl').open('rb') as f:z=pickle.load(f)"
start=s.index(a);end=s.index("    status='CHECKPOINT';newfront={};i=0;substitutions=0",start)
init='''    def allowed(t,x):
        if x%2==0:return False
        p=[];u=t
        while True:
            p.append(u[0])
            if u[0]==x:break
            u=u[1] if x<u[0] else u[2]
        if (len(p)-1)%2:return False
        for j in range(len(p)-3,-1,-2):
            g0,p0=p[j:j+2]
            if g0%2==0 or p0%2!=0 or not ((x<g0 and x<p0) or (x>g0 and x>p0)):return False
        return True
    def balanced(lo,hi):
        if lo>hi:return None
        k=(lo+hi)//2;return (k,balanced(lo,k-1),balanced(k+1,hi))
    if BATCH==1:
        bf=None
        for k in range(15,0,-1):bf=(k,None,bf)
        seedbf=[bf]
        for step in range(64):
            choices=[x for x in range(1,16,2) if x!=bf[0] and allowed(bf,x)]
            assert choices
            x=choices[(step*104729+step*step*7919)%len(choices)]
            bf,h,q=lift.action(bf,15,x);assert h==q
            if step%2==0:seedbf.append(bf)
        for bf in dict.fromkeys(seedbf):
            b=R.rank_tree(bf,1,15);g=bf[0]
            candidates=[bf]
            for x in range(1,16,2):
                if x==g or not allowed(bf,x):continue
                if x<g:t=(g,(x,balanced(1,x-1),balanced(x+1,g-1)),balanced(g+1,15))
                else:t=(g,balanced(1,g-1),(x,balanced(g+1,x-1),balanced(x+1,15)))
                candidates.append(t)
            for a0 in candidates:
                a=R.rank_tree(a0,1,15);records.setdefault((a,b),(0,None,None,None,None,None));frontier.append((a,b))
        frontier=list(dict.fromkeys(frontier))
'''
s=s[:start]+init+s[end:]
s=s.replace("if ar!=br:actions.append(('KEEP',ar,ta,0))", "if ar!=br and allowed(tb,ar):actions.append(('KEEP',ar,ta,0))")
s=s.replace("                    actions.extend((('KEEP',x,out,1),('DELETE',x,out,1)))", "                    actions.append(('DELETE',x,out,1))\n                    if allowed(tb,x):actions.append(('KEEP',x,out,1))")
s=s.replace("F/'ranked_source_bst.py'", "F/'ranked_source_bst.py',F/'ranked_source_bst15.py'")
s=s.replace("F/'search_full_source13_beam_v2.py')}}", "F/'search_full_source13_beam_v2.py',F/'search_full_source15_beam.py')}}")
exec(compile(s,str(Path(__file__).resolve()),'exec'))
