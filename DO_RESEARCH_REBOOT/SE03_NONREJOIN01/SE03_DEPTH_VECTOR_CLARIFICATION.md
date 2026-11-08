# Full labeled depth vectors and partial depth observations

This clarifies an overbroad sentence in the inherited SE02
ROTATION_INTERFERENCE.md. A COMPLETE labeled depth vector for every key,
together with the fixed key order, DOES uniquely determine a BST. What
does not determine full state is a root, selected queried depths, double-
depth bands, or an unrestricted difference vector without either base tree.

Proof of the complete-vector statement: the unique depth-zero key is the
root in both trees. All keys below it in key order form the left subtree,
and all keys above it form the right subtree. Subtract one from their
depths and apply induction to each smaller ordered key set. Empty sets
have one empty tree. Thus equality of full labeled depth vectors forces
equality of both complete subtrees and of the entire BST.

For the common fixed B skeleton S of SE03, its full labeled depth vector
therefore determines that skeleton. Together with the exact fixed gap
BSTs F_i it determines the full original B tree. Knowing one skeleton and
the complete signed depth difference to the other also determines both.
The difference vector alone, and the floor-depth differences used for
signed charge accounting, have not been proved sufficient.

Every accepted SE02 and SE03 closure identity used exact tree terms or
the proved rigid-hanger projection, not the incorrect overbroad sentence.
The signed cost equations, recurrent alignment, restricted compensation
and novelty limitations are unchanged. No inherited artifact is edited.
