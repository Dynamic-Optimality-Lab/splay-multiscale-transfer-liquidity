"""Allow all source-valid prehistories for the same 5,7,9 low A preparation.
Prior fixed-Sstar searches and failures remain unchanged.
"""
from pathlib import Path
B=Path(__file__).resolve().parent
source=(B/'audit_product.py').read_text(encoding='utf-8')
source=source.replace('len(states)<22000','len(states)<120000')
source=source.replace("'product_graph_receipt.json'","'product3_graph_receipt.json'")
source=source.replace("'product_attempts.json'","'product3_attempts.json'")
source=source.replace("'audit_product_exit.json'","'audit_product3_exit.json'")
source=source.replace('for x,bf2 in full_moves(bf):','for x,bf2 in full_moves(bf):\n            C.queries+=1;C.check()')
helper='''@functools.lru_cache(None)
def valid_start(t):
    if t[0]!=1:return False
    for k in (5,7,9):
        par,ch=L.marked_tree(t,M);anc=[];a=par[k]
        while a is not None:anc.append(a);a=par[a]
        beta=sum(len(ch[a])>=2 for a in anc)
        if ch[k] or not C.ss(t,k):return False
        if k==5:
            if beta<1:return False
        elif len(anc)!=2 or beta!=2:return False
        t=nxt(t,k)
    return True
'''
source=source.replace('def main():',helper+'\ndef main():',1)
source=source.replace('if bf==S and sizes[component[i]]>5','if valid_start(bf) and sizes[component[i]]>5')
source=source.replace("a=V;bf=S;be=answer['initial_BE']","a=V;bf=answer['initial_BF'];be=answer['initial_BE']")
source=source.replace("(initialA,S,answer['initial_BE'])","(initialA,answer['initial_BF'],answer['initial_BE'])")
source=source.replace('C.replay(initialA,S,be,word)','C.replay(initialA,answer[\'initial_BF\'],be,word)')
source=source.replace('(initialA,S,be)','(initialA,answer[\'initial_BF\'],be)')
source=source.replace("'initial_BF':S,","'initial_BF':answer['initial_BF'],")
exec(compile(source,str(B/'audit_product.py')+'[varied-source-prehistory]', 'exec'),globals())
