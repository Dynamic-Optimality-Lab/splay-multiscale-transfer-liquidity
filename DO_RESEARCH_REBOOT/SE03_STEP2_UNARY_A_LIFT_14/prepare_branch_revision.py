"""Preserve the unpromoted first branch syntax; add a missing first frame.
The separately sealed unary grammar already contains this case.
"""
from pathlib import Path
B=Path(__file__).resolve().parent
s=(B/'branch_frames.py').read_text()
old="""                for TTT,yy in decorations(TT,y,2):add(TTT,yy,'old_unary_target')
        for path,sub in [(q,v) for q,v in leafpaths(T) if 1<=len(q)<=2]:"""
new="""                for TTT,yy in decorations(TT,y,2):add(TTT,yy,'old_unary_target')
                # A shallow OLD unary parent may carry marks on one side
                # and the private first target on the other. Contracting
                # that parent makes its private side look deep in BASE.
                if len(path)==1:
                    U=get(TT,path)
                    private_side='L' if not node(U[1]) else 'R'
                    pp=path+private_side
                    lo,hi=bound(TT,pp);v=(lo+hi)//2
                    add(put(TT,pp,(v,'a','b')),v,'private_child_of_old_unary_parent')
        for path,sub in [(q,v) for q,v in leafpaths(T) if 1<=len(q)<=2]:"""
assert old in s;s=s.replace(old,new)
with (B/'branch_frames2.py').open('x',encoding='utf-8') as f:f.write(s)
a=(B/'audit_branch_grammar.py').read_text().replace('import branch_frames as G','import branch_frames2 as G')
a=a.replace("'branch_grammar.json'","'branch_grammar2.json'").replace("'audit_branch_grammar_exit.json'","'audit_branch_grammar2_exit.json'")
with (B/'audit_branch_grammar2.py').open('x',encoding='utf-8') as f:f.write(a)
a=(B/'audit_branch9.py').read_text().replace("'branch_grammar.json'","'branch_grammar2.json'")
a=a.replace("'branch9_candidate.json'","'branch9_candidate2.json'").replace("'audit_branch9_exit.json'","'audit_branch9_2_exit.json'")
with (B/'audit_branch9_2.py').open('x',encoding='utf-8') as f:f.write(a)
