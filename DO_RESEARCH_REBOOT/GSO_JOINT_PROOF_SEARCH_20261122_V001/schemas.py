"""Original splay rotation schemas with arbitrary, marker-free BST holes.

No projected local splay is introduced. The marker denotes the ORIGINAL root
of one actual full-tree access. The frame induction consumes its actual path.
"""
import sys
import json
from pathlib import Path
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent


def hole(name):return ['hole',name]
def node(key,left,right,marked=False):return ['node',key,marked,left,right]


def rotate(tree,direction):
    tag,key,mark,left,right=tree;assert tag=='node'
    if direction=='right':
        _,child,cm,a,b=left
        return node(child,a,node(key,b,right,mark),cm)
    _,child,cm,b,c=right
    return node(child,node(key,left,b,mark),c,cm)


def at_path(tree,path,direction):
    if not path:return rotate(tree,direction)
    out=list(tree);side=3 if path[0]=='L' else 4
    out[side]=at_path(tree[side],path[1:],direction)
    return out


def inorder(tree):
    if tree[0]=='hole':return ['hole:'+tree[1]]
    return inorder(tree[3])+['key:'+tree[1]]+inorder(tree[4])


def marked_depths(tree,depth=0):
    if tree[0]=='hole':return []
    return ([depth] if tree[2] else [])+marked_depths(tree[3],depth+1)+marked_depths(tree[4],depth+1)


def compile_schemas():
    A,B,C,D=map(hole,('A','B','C','D'))
    rows=[
        ('ZIG_L',node('p',node('x',A,B),C,True),[('', 'right')],1,0),
        ('ZIG_R',node('p',A,node('x',B,C),True),[('', 'left')],1,0),
        ('LL',node('g',node('p',node('x',A,B),C),D,True),[('', 'right'),('', 'right')],2,1),
        ('RR',node('g',A,node('p',B,node('x',C,D)),True),[('', 'left'),('', 'left')],2,1),
        ('LR',node('g',node('p',A,node('x',B,C)),D,True),[('L', 'left'),('', 'right')],2,1),
        ('RL',node('g',A,node('p',node('x',B,C),D),True),[('R', 'right'),('', 'left')],2,1)]
    out=[]
    for name,before,moves,consumed,q in rows:
        after=before
        for path,direction in moves:after=at_path(after,path,direction)
        assert inorder(before)==inorder(after) and marked_depths(before)==[0]
        assert len(marked_depths(after))==1
        out.append({'case':name,'before':before,'rotations':[list(v) for v in moves],
                    'after':after,'consumed_path_frames':consumed,'original_B_double_cost':q,
                    'old_root_post_depth':marked_depths(after)[0],
                    'holes':'Each hole is any marker-free physical BST in its original inorder interval, including empty.'})
    return out


def proof_ir():
    return {'language':'original-splay-marker-and-affine-ledger.v1',
            'rotation_schemas':compile_schemas(),
            'frame_induction':{
                'initial':'If original depth is zero the old root is current root. Otherwise the old root is the topmost unconsumed frame and absent from all hanging subtrees and the current subtree.',
                'nonterminal':'With at least3 frames, consume the bottom2 by an unmarked LL/RR/LR/RL rewrite. At least1 outer frame remains; its marked original root is unchanged.',
                'terminal':'With2 frames use one of the four marked double schemas. With1 frame use one of the two marked zig schemas.',
                'ranking':'The nonnegative unconsumed path length decreases by2 or1. No bound on initial depth or on hanging-subtree size is assumed.',
                'coverage':'Remaining depth is0,1,2 or>=3; two branch directions enumerate exactly LL,RR,LR,RL.'},
            'scope_control':'At most two distinct original B targets, all physical keys and arbitrary A operations retained. Cyclic entry is derived, not assumed.',
            'scope_unrestricted':'Any original B target, including a third target distinct from both stored roots. This branch may not be excluded.'}


def main():
    assert not (HERE/'FINAL_MANIFEST.json').exists()
    p=HERE/'PROOF_LANGUAGE.json';assert not p.exists()
    p.write_text(json.dumps(proof_ir(),indent=2),encoding='utf-8')
    print({'schemas':6,'arbitrary_hanging_subtrees_retained':True})


if __name__=='__main__':main()
