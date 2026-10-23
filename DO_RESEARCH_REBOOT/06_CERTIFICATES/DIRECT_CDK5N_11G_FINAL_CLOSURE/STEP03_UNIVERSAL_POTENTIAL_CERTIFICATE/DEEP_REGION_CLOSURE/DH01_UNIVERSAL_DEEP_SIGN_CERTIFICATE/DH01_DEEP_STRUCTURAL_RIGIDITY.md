# DH-01 Deep B-Controller Structural Analysis (proved fragments + open remainder)

Finiteness: 19 slots; core slots 0..8 with BST-rank intervals; gaps
slots 9..18 with empty children (b_valid). Deep = some core slot at depth
>=7 (chain-like: 8-9 nodes on one root path possible; max depth 8).
PROVED: (i) single rotation changes only the rotated child's descendant
set (others same-or-fewer); hence at most the child joins C; (ii) marked
target splays preserve C (all rotated children are verified path nodes,
hence marked-or-ancestor-of-marked); (iii) single-event low and all high
edges cannot be self-loops (terminal/genuine B-change forces t.b != s.b;
see micro-theorem doc). OPEN: universal deep closed-walk bound (the
finiteness + single-splay facts do not telescope to arbitrary closed
walks without H1/H2 analogues for the deep region).
