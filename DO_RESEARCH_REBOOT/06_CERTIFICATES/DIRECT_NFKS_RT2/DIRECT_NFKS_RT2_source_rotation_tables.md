# RT2 source rotation tables (authoritative: wp6_eventflow.py:111-182)

Unit top at depth D. Conventions: y = splayed node; gainers listed with exact deltas.

## First-splay steps (splay z; tracked v arbitrary)

- zig-L (z left child of p): z−1; A=z.left −1; T=z.right 0; p+1; R(p)=p.right +1
  (rigid). Gainers: {p, R(p)}, keys >z.
- zig-R (mirror): z−1; A'''=z.left 0; B''=z.right −1; p+1; L(p)+1. Gainers <z.
- zigzig-LL (z,p,g left-line): z−2; A−2; B=z.right −1; p 0; C=p.right +1; g+2;
  T3=g.right +2. Gainers {C,g,T3}, all >z-side keys.
- zigzig-RR (mirror): z−2; A'=z.left −1; B'=z.right −2; p 0; C'=p.left +1; g+2;
  T3'=g.left +2. Gainers on z's near side.
- zigzag-RL (z right of p, p left of g): z−2; T1=z.left −1; T3=z.right −1;
  T0=p.left 0; p 0; g+1; T4=g.right +1. Gainers {g,T4}.
- zigzag-LR (mirror): z−2; A_y−1; B_y−1; C_y=p.right 0; p 0; g+1; D_y=g.left +1.
  Gainers {g,D_y}.

Consequences: single-step gain ≤+2 (LL/RR outer only); no step gains on both
sides of z (monochromatic); every gainer enters z's subtree (validated V1/V2,
0 violations over 5,448 steps).

## Return step (splay y in T1; y at depth 1 or 2 by orientation lemma)

- R-zig (y child of z): y−1; near-side sibling regions 0; far side F=+1 rigid;
  z(parent)+1. Exactly one +1 region (F = z's non-y child subtree).
- R-zigzig (y same-side grandchild): y−2; near-inner −1/−2; C=+1 (y's sibling:
  p's far child); T3=+2 (z's far child); z +2 (tracked only if v=z, handled
  separately). Exactly two gain regions (C +1, T3 +2), both inside z's subtree.

Hanging subtrees: every non-listed region changes by exactly 0 (above untouched,
p-as-p, beside-0) or as listed; nodes that never rotate are covered (no-rotation
≠ no-change is accounted: ancestor-chain shortening/lengthening is exactly the
listed ±0/±1/±2).
