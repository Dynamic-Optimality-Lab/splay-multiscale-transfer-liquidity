"""Validate all raw trees and bind the new words to the predeclared source domain."""
import hashlib
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent

def main():
    cp=HERE/'shared_shallow_certificate.json';c=json.loads(cp.read_text(encoding='utf-8'))
    def vine(n):
        t=None
        for k in range(n,0,-1):t=[k,None,t]
        return t
    def mirror(t,n):return None if t is None else [n+1-t[0],mirror(t[2],n),mirror(t[1],n)]
    def inorder(t):
        if t is None:return []
        assert isinstance(t,list) and len(t)==3 and type(t[0]) is int
        return inorder(t[1])+[t[0]]+inorder(t[2])
    total=0
    for i,w in enumerate(c['witnesses']):
        n=w['n'];expected=vine(n)
        if i%2:expected=mirror(expected,n)
        assert w['initial_diagonal']==expected
        trees=[w['initial_diagonal'],w['cycle_initial_A'],w['cycle_initial_B']]
        for row in w['prefix_replay']+w['full_replay']:
            assert 1<=row['key']<=n and row['mode'] in ('D','K')
            trees.extend(row[k] for k in ('source_A','source_B','destination_A','destination_B'))
        for t in trees:
            assert inorder(t)==list(range(1,n+1))
            total+=1
    word=([['K',13],['K',12],['K',11],['K',2]]+[['K',k] for k in range(3,14)]+
          [['K',k] for k in range(1,14)]+[['K',k] for k in range(12,0,-1)]+[['D',9]])
    assert c['witnesses'][0]['word']==word and c['witnesses'][0]['prefix']==[['D',9]]
    assert c['witnesses'][1]['word']==[[m,14-x] for m,x in word] and c['witnesses'][1]['prefix']==[['D',5]]
    result=dict(status='PASS',raw_tree_occurrences_validated=total,
                exact_ranked_key_sets=True,strict_BST_order=True,initial_vines_bound=True,
                new_word_and_reflection_bound_to_gate=True,
                certificate_sha256=hashlib.sha256(cp.read_bytes()).hexdigest())
    with (HERE/'source_domain_audit.json').open('x',encoding='utf-8') as f:json.dump(result,f,indent=2);f.write('\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
