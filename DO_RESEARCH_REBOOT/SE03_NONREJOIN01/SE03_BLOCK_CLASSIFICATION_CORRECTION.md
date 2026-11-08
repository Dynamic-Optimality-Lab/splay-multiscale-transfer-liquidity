# Positive preterminal requests in a negative six-key block

This corrects the final qualification in section2 of
SE03_NEGATIVE_SOURCE_BLOCK_PARTITION.md. In the TWO one-StepEv H2 case,
the intermediate positive target u must be distinct from both y and x,
and its mode must be DELETE. All positive requests before the terminal
genuine KEEP in any H<=2 block are DELETEs.

Proof: before its terminal KEEP x, every KEEP has target y, the unchanged
B root. A starts with root y and ends with x!=y. A positive preterminal
KEEP y would require a preceding positive request leaving y, the positive
return to y itself, and a later positive request to x. That requires at
least THREE A StepEvs. It is impossible when H<=2. In the two-positive-
request H2 case, the first target u differs from y because it is positive,
and differs from x because otherwise the second x request would be a root
identity. A preterminal KEEP u would be genuinely B-changing and contradict
the block's definition, so this request is DELETE.

For H>=3 a nongenuine KEEP y CAN have positive A charge; that charge must
always be retained in equation(1) of the block proof. The original file's
warning was valid for general blocks but incorrectly included under its
H2 classification. All other numerical bounds, the complete negative
pairs, B-core consequences and1+2H active-path bound are unchanged.
The current classification is the original proof WITH this correction.
