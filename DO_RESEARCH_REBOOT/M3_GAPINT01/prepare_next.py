"""Versioned fixed-gap continuation using the already proved generic source mechanism."""
import sys
from pathlib import Path
g=int(sys.argv[1]);assert g in (2,3,4);src=Path('DO_RESEARCH_REBOOT/M3_GAPINT01');dst=Path(f'DO_RESEARCH_REBOOT/M3_GAPINT0{g}');dst.mkdir(exist_ok=False)
gate=f'''# GAPINT0{g} — Pre-execution gate for gap{g}/gap{9-g}

User authorizes continued remaining-signature work. The generic fixed-gap
source/profile proof and analytic row-discharge identities are established
in GAPINT01/RESULT.md. This is the SAME construction at a different
fixed gap; no new allocation-invariance or source-reflection premise.
Principal theorem: all mu and sigma=n e{g} or n e{9-g},0<=n<=266,
inside chi8 have the signed bound, or an exact scoped failure/UNKNOWN.

R1: two remaining single-support families, not multi-gap or all M3.
R2: known at-most3 protected-anonymous H1 classification and complete
ordered-tree recurrence parameterized by g; all H2 are Gamma0; explicit
integer recurrence from-psi. R3: one parameterized source mechanism,
one table and bounded original audit; stop on refutation/cap. R4 success
deletes these two WHOLE ORIGINAL signature families for all populations
and masks. A finite fit alone or sampled scope is not success.

Private wrong-side port populations remain forgotten in proof profiles;
only true exposed anonymous gap and hidden S order are used. Reflection
is of mathematical low/core profiles only; original high chi8 toll and
h0 correction retained. Same full state/midpoint/source q and weights.

All old files/source/Git read-only; writes only this fresh folder. Use
the frozen exact Int/Python-B/backend. No solver/install/cap/source/Git
change. Caps:120 CPU finite phase,300 completion/original audit,4m DAG,
2m states,5m materialized edges,1m source cases,32GiB. Discharge w>=2,
w1 with psi(dest)>=1 and w0 with psi(dest)=2 by the SAME proved range/
debt identities, not implicit graph storage or case thinning. Independent
regeneration and full original roots for forks, negative edges, whole
macros, boundary-touching mass266, reflected gap and mixed closure.
Any failure stops this run. M3/outside-chi8/Bank25 statuses unchanged
until actual verification. No repeat of the refuted B-only route.
'''
(dst/'PRE_EXECUTION.md').write_text(gate)
prefix="import sys\nsys.path.insert(0,'DO_RESEARCH_REBOOT/M3_GAPINT01')\n"
for name in ('build_v2.py','complete.py','verify.py','potential.py'):
    s=(src/name).read_text().replace("Path('DO_RESEARCH_REBOOT/M3_GAPINT01')",f"Path('DO_RESEARCH_REBOOT/M3_GAPINT0{g}')")
    if name=='build_v2.py':s=s.replace('build(1,BASE)',f'build({g},BASE)')
    (dst/name).write_text(prefix+s)
s=(src/'original_audit.py').read_text()
start=s.index('    # Closed full-state mixed cycle')
end=s.index('    for rr in records:',start)
block='''    # Reversible core zig with a retained anonymous fork and an opaque S port.
    z=S.LEAF;croot=g+1;right=S.balanced([16*k for k in range(g+2,9)]);rkey=right[1]//16
    core= S.node(croot,S.balanced(range(g+1)),S.balanced(range(g+2,9)))
    Afork=S.node(16*croot,S.node(16*g-8,S.balanced([16*k for k in range(g)]),S.node(16*g,z,z)),right)
    A,cuts=concrete(collapse(Afork),3,g);cuts.append((16*rkey,0));B=V.insert(scale(core),16*g-8)
    marks=[croot,rkey]+[k for k in range(9) if k not in (croot,rkey)][:3];cycle_mu=sum(1<<k for k in marks)
    ac,bc,l=low(d,L,A,B,cuts,[['K',16*rkey]],'interior_fork_cycle_low',cycle_mu);l=add(l)
    h=high(dh,H,bc,16*croot,l['destination'],l['source'],'interior_fork_cycle_high');h=add(h)
    assert l['source']==h['destination'] and l['destination']==h['source'] and l['w']+h['w']==8
'''
s=s[:start]+block+s[end:]
s=s.replace("'gaps':[1,8]","'gaps':[g,9-g]").replace("'mu':79,'n':3,'gap':1","'mu':cycle_mu,'n':3,'gap':g")
s=s.replace("'gap1_population_'+str(n)","'gap'+str(c['gap'])+'_population_'+str(n)")
s=s.replace("'wrong_side_gap1_payload_'+str(n)","'wrong_side_gap'+str(g)+'_payload_'+str(n)")
s=s.replace("reflected_gap8_three_node_fork",f"reflected_gap{9-g}_three_node_fork")
(dst/'original_audit.py').write_text(prefix+s)
print({'prepared_gap':g,'reflected_gap':9-g,'folder':str(dst)})
