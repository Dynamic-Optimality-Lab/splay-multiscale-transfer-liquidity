# Three-marked-key depth ≤4 (PROVED from RT2 + idempotence + 26AL)

**Claim.** root(T)=x, distinct y,z≠x, W any finite word over {y,z}:
d_{SW(T)}(x) ≤ 4.

**Proof.** Delete consecutive duplicates (root no-ops: splaying the root
changes nothing). The reduced word alternates; assume it starts with y
(mirror case symmetric). After Sy: d(x)≤2 by 26AJ Lemma 2 (former-root depth;
x was root). After following Sz: d(x)≤2+2=4 by banked 26AL-L1 (x≠z, one
splay). State is now rooted at z with x at depth ≤4; next access y returns to
a y-rooted state. Apply RT2 with (root=y-state, splay z, return y)? Careful
with order: RT2 bounds Sy(Sz(U)) relative to U rooted at y. Take U = state
after first Sy (rooted y, dU(x)≤2). Then Sz(U) has d≤4; Sy(Sz(U)) has, by RT2,
d ≤ dU(x)+2 ≤ 4. By idempotence, every subsequent y/z alternation revisits the
established post-y / post-z states (F(F(T))=F(T) applied to the y/z pair at
each cycle), so the bound 4 persists for arbitrarily long W. The z-first
orientation is identical with y,z swapped. DELETEs do not affect B-depths and
are irrelevant here (single-tree statement). ∎

**Corroboration.** Independent n≤8 screen (charter §10): no violations of the
depth-4 bound. Tightness: depth 4 attained (e.g. vine configurations).
