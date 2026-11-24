"""Isolated exact physical replay. No historical engine is changed.

Integers encode S labels as bitsets over sorted physical keys. Every primitive
has an original actor/operation/StepEv/bit ID. Complete pointer states are kept
at operation boundaries and reconstructed at any primitive from the source.
"""
from __future__ import annotations
from bisect import bisect_left, bisect_right
from collections import defaultdict, Counter
from fractions import Fraction
import hashlib
import json


def digest(x):
    return hashlib.sha256(json.dumps(x, separators=(",", ":"), sort_keys=True).encode()).hexdigest()


class Tree:
    def __init__(self, state):
        self.keys = sorted(int(k) for k in state["children"])
        self.ch = {int(k): list(v) for k, v in state["children"].items()}
        self.root = state["root"]
        self.par = {k: None for k in self.keys}
        for k, v in self.ch.items():
            for c in v:
                if c is not None:
                    assert self.par[c] is None
                    self.par[c] = k
        assert self.par[self.root] is None
        self.validate()

    def state(self):
        return {"root": self.root, "children": {str(k): list(self.ch[k]) for k in self.keys}}

    def validate(self):
        seen = set()
        todo = [(self.root, None, None)]
        while todo:
            k, lo, hi = todo.pop()
            assert k not in seen and (lo is None or lo < k) and (hi is None or k < hi)
            seen.add(k)
            for s, c in enumerate(self.ch[k]):
                if c is not None:
                    assert self.par[c] == k
                    todo.append((c, lo if s == 0 else k, k if s == 0 else hi))
        assert seen == set(self.keys)

    def path(self, x):
        out, k = [], self.root
        while k != x:
            assert k is not None
            out.append(k)
            k = self.ch[k][x > k]
        return out + [x]

    def labels(self, bits):
        out = {}
        stack = [(self.root, False)]
        while stack:
            k, done = stack.pop()
            if done:
                l, r = self.ch[k]
                out[k] = bits.get(k, 0) | out.get(l, 0) | out.get(r, 0)
            else:
                stack.append((k, True))
                stack.extend((c, False) for c in self.ch[k] if c is not None)
        return out

    def edges(self):
        return {(k, c, s) for k in self.keys for s, c in enumerate(self.ch[k]) if c is not None}

    def rotate(self, u, side):
        """Promote side-child of u (side 0 = right rotation)."""
        v = self.ch[u][side]
        assert v is not None
        c = self.par[u]
        external = None if c is None else int(self.ch[c][1] == u)
        middle = self.ch[v][1-side]
        deleted = {(u, v, side)}
        added = {(v, u, 1-side)}
        if c is None:
            self.root = v
        else:
            deleted.add((c, u, external))
            added.add((c, v, external))
            self.ch[c][external] = v
        self.par[v] = c
        self.ch[u][side] = middle
        if middle is not None:
            self.par[middle] = u
            deleted.add((v, middle, 1-side))
            added.add((u, middle, side))
        self.ch[v][1-side] = u
        self.par[u] = v
        return v, c, middle, deleted, added


def vine(keys):
    keys = sorted(keys)
    return {"root": keys[0], "children": {str(k): [None, keys[i+1] if i+1<len(keys) else None] for i,k in enumerate(keys)}}


def closure(tree, targets):
    ans = set()
    for k in targets:
        ans.update(tree.path(k))
    return ans


class Replay:
    def __init__(self, source, certify=True, independent=True):
        self.source = source
        self.ops = source["operations"]
        self.a, self.b = Tree(source["initial_A"]), Tree(source["initial_B"])
        assert self.a.keys == self.b.keys
        self.keys = self.a.keys
        # M is the complete genuine B support, determined in a preliminary
        # physical replay, not by dropping root-repeat keys in the requested word.
        tmp = Tree(source["initial_B"])
        genuine = set()
        for tag, x in self.ops:
            if tag == "K":
                if tmp.root != x:
                    genuine.add(x)
                self.plain_splay(tmp, x)
        self.M = genuine
        self.S = closure(Tree(source["initial_B"]), genuine) if genuine else set()
        self.bits = {k: 1 << i for i,k in enumerate(self.keys) if k in self.S}
        self.full = sum(self.bits.values())
        self.extremes = 0 if not self.S else self.bits[min(self.S)] | self.bits[max(self.S)]
        self.I = {k for k, lab in self.b.labels(self.bits).items() if k in self.S and lab & ~self.bits[k]}
        self.events = []
        self.doubles = {}
        self.boundaries = []
        self.a_changes = defaultdict(list)
        self.b_creates = defaultdict(list)
        self.b_losses = defaultdict(list)
        self.initial_a_labels = set(self.a.labels(self.bits).values()) - {0}
        self.a_current = self.initial_a_labels.copy()
        self.b_current = set(self.b.labels(self.bits).values()) - {0}
        self.A = self.Q = self.VA = self.ZB = self.KB = 0
        self.PA = self.NA = self.DB = 0
        self.independent_checks = 0
        self._independent = independent
        if independent:
            import sys
            from pathlib import Path
            repo = Path(__file__).resolve().parents[2]
            sys.path.insert(0, str(repo / "python"))
            from independent import splay as ind
            self.ind = ind
            self.ia = self.as_tuple(self.a)
            self.ib = self.as_tuple(self.b)
        for t, (tag, x) in enumerate(self.ops, 1):
            apre, bpre = self.a.state(), self.b.state()
            apath = self.a.path(x)
            bpath = self.b.path(x) if tag == "K" else None
            start = len(self.events)
            self.A += (len(apath)) // 2
            self.VA += (len(apath)-1) % 2
            self.splay(self.a, x, "A", t)
            post_a_time = len(self.events)
            if tag == "K":
                assert set(bpath) <= self.S or len(bpath) == 1
                self.KB += int(len(bpath)>1)
                self.Q += (len(bpath)-1)//2
                self.ZB += (len(bpath)-1)%2
                self.splay(self.b, x, "B", t)
            self.boundaries.append({"t": t, "tag": tag, "x": x,
                "A_path": apath, "B_path": bpath, "a": len(apath)//2,
                "q": 0 if bpath is None else (len(bpath)-1)//2,
                "pre_A": apre, "pre_B": bpre,
                "post_A": self.a.state(), "post_B": self.b.state(),
                "start_time": start, "post_A_time": post_a_time, "end_time": len(self.events)})
            if independent:
                self.ia, ea = ind.trace(self.ia, x)
                assert self.ia == self.as_tuple(self.a)
                assert len(ea) == len(apath)//2
                if tag == "K":
                    self.ib, eb = ind.trace(self.ib, x)
                    assert self.ib == self.as_tuple(self.b)
                    assert sum(e[0] != "ZIG" for e in eb) == (len(bpath)-1)//2
                self.independent_checks += 1
        self.T = len(self.events)
        self.closed = self.a.state() == source["initial_A"] and self.b.state() == source["initial_B"]
        assert self.closed, (source["name"], "not paired closed")
        assert self.a_current == self.initial_a_labels
        assert self.DB == self.PA-self.NA
        assert sum(e["actor"] == "A" for e in self.events) == 2*self.A-self.VA
        assert self.KB <= self.A
        self.event_by_id = {tuple(e["id"]): e for e in self.events}
        self.eligible_S, self.windows_S = self.scan_windows(self.S)
        self.eligible_I, self.windows_I = self.scan_windows(self.I, isolated=True)
        if certify:
            self.certify()

    @staticmethod
    def plain_splay(tree, x):
        while tree.par[x] is not None:
            p = tree.par[x]
            g = tree.par[p]
            s = int(x > p)
            if g is None:
                tree.rotate(p, s)
            else:
                z = int(p > g)
                if s == z:
                    tree.rotate(g, z)
                    tree.rotate(p, s)
                else:
                    tree.rotate(p, s)
                    tree.rotate(g, z)

    def as_tuple(self, tree):
        vals = {None: self.ind.LEAF}
        stack = [(tree.root, False)]
        while stack:
            k, done = stack.pop()
            if done:
                l,r = tree.ch[k]
                vals[k] = self.ind.node(k, vals[l], vals[r])
            else:
                stack.append((k, True))
                stack.extend((c, False) for c in tree.ch[k] if c is not None)
        return vals[tree.root]

    def splay(self, tree, x, actor, t):
        j = 0
        while tree.par[x] is not None:
            j += 1
            p = tree.par[x]
            g = tree.par[p]
            s = int(x > p)
            z = int(p > g) if g is not None else None
            case = "ZIG" if g is None else ("R" if z else "L")+("R" if s else "L")
            frame = tree.labels(self.bits)[g] if g is not None else None
            rotations = [(p,s)] if g is None else [(g,z),(p,s)] if s == z else [(p,s),(g,z)]
            evs = []
            for bit, (u, side) in enumerate(rotations):
                before = tree.labels(self.bits)
                oldset = set(before.values())-{0}
                v,c,middle,deleted,added = tree.rotate(u,side)
                after = tree.labels(self.bits)
                newset = set(after.values())-{0}
                lost, created = oldset-newset, newset-oldset
                assert len(lost)<=1 and len(created)<=1
                if actor == "A":
                    sign = len(lost & self.b_current)-len(created & self.b_current)
                    self.PA += sign == 1
                    self.NA += sign == -1
                    self.a_current = newset
                else:
                    sign = len(newset-self.a_current)-len(oldset-self.a_current)
                    assert sign in (-1,0)
                    self.DB += sign == -1
                    self.b_current = newset
                time = len(self.events)+1
                ev = {"id": [actor,t,j,bit], "time": time, "actor": actor,
                      "case": case,"target":x,"pivot":u,"promoted":v,
                      "external":c,"middle":middle,"side":side,
                      "deleted": sorted(deleted),"added": sorted(added),
                      "lost":sorted(lost),"created":sorted(created),"sign":sign,
                      "demoted_label":after[u], "frame":frame}
                self.events.append(ev)
                evs.append(ev)
                if actor == "A":
                    for lab in lost:
                        self.a_changes[lab].append((time,False))
                    for lab in created:
                        self.a_changes[lab].append((time,True))
                else:
                    for lab in lost:
                        self.b_losses[lab].append(time)
                    for lab in created:
                        self.b_creates[lab].append(time)
            if actor == "B" and g is not None:
                chosen = evs[0 if case in ("RR","LL") else 1]
                self.doubles[(t,j)] = {"id":(t,j),"case":case,"g":g,"F":frame,
                    "events":[e["time"] for e in evs],"signs":[e["sign"] for e in evs],
                    "nu":chosen["time"],"J":chosen["demoted_label"]}
            if actor == "B" and g is None:
                assert evs[0]["sign"] == -1

    def label_keys(self, lab):
        return [k for k in self.keys if self.bits.get(k,0) & lab]

    def present(self, lab, time):
        if not self.T:
            return lab in self.initial_a_labels
        time %= self.T
        changes = self.a_changes[lab]
        i = bisect_right(changes, (time,True))-1
        return changes[i][1] if i>=0 else lab in self.initial_a_labels

    def any_present(self, lab, lo, hi):
        """Actual snapshots strictly after lo through hi, on an unrolled circle.
        B births/removals do not change A, so testing at lo is equivalent there.
        """
        assert hi>=lo and hi-lo<=self.T
        if self.present(lab,lo):
            return True
        for time, on in self.a_changes[lab]:
            if on:
                k=(lo-time)//self.T+1
                if time+k*self.T<=hi:
                    return True
        return False

    def previous(self, times, before):
        assert times
        period, rem = divmod(before-1,self.T)
        i = bisect_left(times,rem+1)-1
        return times[i]+period*self.T if i>=0 else times[-1]+(period-1)*self.T

    def next_hit(self, d):
        t = d["id"][0]
        for dt in range(1,len(self.ops)+1):
            h = (t+dt-1)%len(self.ops)+1
            tag,x = self.ops[h-1]
            if tag == "K" and self.bits.get(x,0)&d["J"]:
                return h, self.boundaries[h-1]["post_A_time"] + (self.T if h<=t else 0)
        raise AssertionError("chosen output never hit")

    def scan_windows(self, domain, isolated=False):
        if len(domain)<2:
            return set(),[]
        # Cyclic constant-target blocks, retaining outside-domain barriers.
        keeps = [(i+1,x) for i,(tag,x) in enumerate(self.ops) if tag == "K"]
        if not keeps:
            return set(),[]
        cut = next((i for i in range(len(keeps)) if keeps[i][1]!=keeps[i-1][1]), None)
        if cut is None:
            return set(),[]
        keeps = keeps[cut:]+keeps[:cut]
        blocks=[]
        for t,x in keeps:
            if not blocks or blocks[-1]["x"]!=x:
                blocks.append({"x":x,"ts":[]})
            blocks[-1]["ts"].append(t)
        ranks = {k:i for i,k in enumerate(sorted(domain))}
        eligible, windows = set(),[]
        for i,bl in enumerate(blocks):
            for direction in (1,-1):
                anchor=min(domain) if direction==1 else max(domain)
                if bl["x"]!=anchor:
                    continue
                run=[bl]
                rank=ranks[anchor]
                for di in range(1,len(blocks)):
                    nxt=blocks[(i+di)%len(blocks)]
                    if nxt["x"] not in ranks or ranks[nxt["x"]]!=rank+direction:
                        break
                    rank += direction
                    run.append(nxt)
                state=self.boundaries[bl["ts"][0]-1]["pre_B"]
                physical = closure(Tree(state),domain)==domain
                long = len(run)>=(len(domain)+1)//2+1
                ok=long and (physical or not isolated)
                ts=[t for b in run for t in b["ts"]]
                windows.append({"anchor":bl["ts"][0],"direction":direction,"length":len(run),
                    "threshold":(len(domain)+1)//2+1,"isolated":physical,"eligible":ok,
                    "operations":ts})
                if ok:
                    eligible.update(ts)
        return eligible,windows

    def state_after(self, actor, time):
        tree=Tree(self.source["initial_"+actor])
        for ev in self.events[:time]:
            if ev["actor"]==actor:
                tree.rotate(ev["pivot"],ev["side"])
        return tree

    def certify(self):
        self.U={}
        for key,d in self.doubles.items():
            if d["signs"] != [0,0] or d["F"] & self.extremes:
                continue
            post=self.boundaries[key[0]-1]["post_A_time"]
            gamma=self.previous(self.b_creates[d["F"]],post+1)
            # Gamma may be cyclically in the previous copy. Look up removal
            # in that same unrolled chronology, rather than comparing modulo IDs.
            kapp=self.previous(self.b_losses[d["F"]],gamma)
            assert 0<post-kapp<=self.T, (key,post,gamma,kapp)
            d["Gamma"],d["kappa"],d["post_A"] = gamma,kapp,post
            if self.any_present(d["F"],kapp,post):
                continue
            h,hit_time=self.next_hit(d)
            d["h"],d["hit_time"] = h,hit_time
            d["exposed"] = self.any_present(d["J"],d["nu"],hit_time)
            self.U[key]=d
        self.cohorts=defaultdict(list)
        for key,d in self.U.items():
            self.cohorts[d["h"]].append(key)
        for h,ds in self.cohorts.items():
            ds.sort(key=lambda k:self.U[k]["J"].bit_count())
            for a,b in zip(ds,ds[1:]):
                assert self.U[a]["J"] != self.U[b]["J"] and self.U[a]["J"] & self.U[b]["J"] == self.U[a]["J"]
        self.pairs=[]
        for h,ds in self.cohorts.items():
            tree=Tree(self.boundaries[h-1]["pre_B"])
            labs=tree.labels(self.bits)
            for left,right in zip(ds,ds[1:]):
                a,b=self.U[left],self.U[right]
                path=[a["g"]]
                while path[-1]!=b["g"]:
                    path.append(tree.par[path[-1]])
                    assert path[-1] is not None
                path.reverse()
                edges={(u,v,int(v>u)) for u,v in zip(path,path[1:])}
                start=self.boundaries[h-1]["post_A_time"]
                end=self.boundaries[h-1]["end_time"]
                beta=next(e for e in self.events[start:end] if edges.intersection(map(tuple,e["deleted"])))
                parent=tuple(beta["id"][1:3])
                shared_lo=b["nu"]
                shared_hi=b["hit_time"]
                sep=any(self.any_present(labs[k],shared_lo,shared_hi) for k in path[1:-1])
                if a["exposed"] or b["exposed"]:
                    cls="E_ctl"
                elif sep:
                    cls="R_sep"
                elif beta["sign"] == -1:
                    cls="R_dec"
                elif self.doubles[parent]["signs"] != [0,0]:
                    cls="R_mix"
                elif parent not in self.U:
                    cls="R_out"
                elif len(self.cohorts[self.U[parent]["h"]]) == 1:
                    cls="T"
                elif h in self.eligible_S:
                    cls="R_scan"
                elif h in self.eligible_I:
                    cls="R_fringe"
                else:
                    cls="R6"
                self.pairs.append({"rho":[h,list(left),list(right)],"class":cls,"path":path,
                    "intermediate_labels":[self.label_keys(labs[k]) for k in path[1:-1]],
                    "beta":beta["id"],"parent":list(parent),
                    "beta_sign":beta["sign"],"path_edges":sorted(edges)})
        assert sum(len(ds)-1 for ds in self.cohorts.values())==len(self.pairs)
        assert len(self.cohorts)<=self.KB
        self.counts=Counter(p["class"] for p in self.pairs)
        loads=Counter(tuple(p["parent"]) for p in self.pairs if p["class"] in ("T","R_scan","R_fringe","R6"))
        assert max(loads.values(),default=0)<=3

    def summary(self):
        counts={c:self.counts[c] for c in ("E_ctl","R_sep","R_dec","R_mix","R_out","T","R_scan","R_fringe","R6")}
        r6=counts["R6"]
        r6pairs=[p for p in self.pairs if p["class"]=="R6"]
        def ratio(x):
            f=Fraction(x,self.A) if self.A else Fraction(0)
            return {"numerator":f.numerator,"denominator":f.denominator}
        return {"name":self.source["name"],"population":len(self.keys),"operations":len(self.ops),
            "A":self.A,"Q_B":self.Q,"R6":r6,"Q_over_A":ratio(self.Q),"R6_over_A":ratio(r6),
            "R_A":2*self.A-self.VA,"V_A":self.VA,"Z_B":self.ZB,"K_B":self.KB,
            "P_A":self.PA,"N_A":self.NA,"D_B":self.DB,
            "S":sorted(self.S),"M":sorted(self.M),"I":sorted(self.I),
            "U_int":len(self.U),"H":len(self.cohorts),"E":len(self.pairs),"classes":counts,
            "paired_closed":self.closed,"independent_operation_checks":self.independent_checks,
            "R6_events":r6pairs,"S_windows":self.windows_S,"I_windows":self.windows_I,
            "max_A_access_cost":max((b["a"] for b in self.boundaries),default=0),
            "max_R6_consuming_double_load":max(Counter(tuple(p["parent"]) for p in r6pairs).values(),default=0),
            "initial_hash":digest([self.source["initial_A"],self.source["initial_B"]]),
            "closing_hash":digest([self.a.state(),self.b.state()]),
            "trace_hash":digest(self.events)}

    def cyclic_A_gap_witnesses(self):
        keeps=[b for b in self.boundaries if b["tag"]=="K"]
        used=set();result=[]
        for i,row in enumerate(keeps):
            if len(row["B_path"])==1:
                continue
            prev=keeps[i-1]
            lo=prev["post_A_time"];hi=row["post_A_time"]
            if row["t"]<=prev["t"]:
                hi+=self.T
            candidates=[]
            for e in self.events:
                if e["actor"]!="A" or e["id"][3]!=0:
                    continue
                time=e["time"]+(self.T if e["time"]<=lo else 0)
                if time<=hi:
                    candidates.append((time,e))
            assert candidates
            ev=min(candidates,key=lambda z:z[0])[1]
            key=tuple(ev["id"][1:3])
            assert key not in used
            used.add(key)
            result.append({"KEEP":row["t"],"previous_KEEP":prev["t"],"A_StepEv":list(key),"real_bit":ev["id"]})
        assert len(result)==self.KB and len(used)<=self.A
        return result
