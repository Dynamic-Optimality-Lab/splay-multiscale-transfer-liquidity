"""Falsify the larger FP + watched-edge-creator + own-unit source rule."""
from pathlib import Path
p=Path(__file__).with_name('search_FP_access_countercut.py')
s=p.read_text()
s=s.replace("if a in seen:lo=seen[a];break\n            seen[a]=len(keys)",
 """if a in seen and 16<=len(keys)-seen[a]<=160 and len(set(keys[seen[a]:]))>=7:
                lo=seen[a];break
            if a not in seen or len(keys)-seen[a]>160:seen[a]=len(keys)""")
s=s.replace("generated<2000","generated<25000")
s=s.replace("attempts=[];witness=None;generated=0","attempts=[];witness=None;generated=0;closed_count=0;digest=hashlib.sha256()")
s=s.replace("else:attempts.append({'generated':generated,'status':'CLOSURE_NOT_FOUND_WITHIN_BOUND'});continue",
 "else:continue")
needle="        graph={};info=[];h0={}"
assert s.count(needle)==1
s=s.replace(needle,needle+"""
        def edge(state,parent,child):
            node=T[state]
            while node and node[0]!=parent:node=node[1] if parent<node[0] else node[2]
            return bool(node and any(c and c[0]==child for c in node[1:]))
""")
needle="            h0.update(zip(dd,units))"
assert s.count(needle)==1
s=s.replace(needle,needle+"""
            creator_units=set();watch=None;creator_t=None
            if len(local)==1:
                node=T[row['A_before']];ap=[]
                while True:
                    ap.append(node[0])
                    if node[0]==x:break
                    node=node[1] if x<node[0] else node[2]
                assert len(ap) in (2,3)
                watch=(ap[-2],x) if len(ap)==2 or ap[-2] not in rkeys else (ap[0],ap[1])
                assert edge(row['A_before'],*watch) and not edge(row['A_after'],*watch)
                for delta in range(1,n+1):
                    br=rows[(e-delta)%n]
                    if not edge(br['A_before'],*watch) and edge(br['A_after'],*watch):
                        creator_t=br['t'];creator_units={(creator_t,1,b) for b in (0,1)};break
                assert creator_t is not None
""")
needle="                graph[d]=g;info.append("
assert s.count(needle)==1
s=s.replace(needle,"                g.update(creator_units)\n                graph[d]=g;info.append(")
s=s.replace("'candidate_units':sorted(g)","'candidate_units':sorted(g),'watched_edge':watch,'creator_access_t':creator_t")
start=s.index("        attempts.append({'generated':generated")
end=s.index("        if S:",start)
s=s[:start]+"""        trial={'generated':generated,'word_length':len(word),'r':len(rkeys),'period_copies':v-u,'A':Acount,'QF':qtotal,
          'matched':len(out),'deficiency':len(S)-len(neigh),'word':word}
        digest.update(json.dumps(trial,sort_keys=True).encode());closed_count+=1
        if len(attempts)<40:attempts.append(trial)
"""+s[end:]
s=s.replace("'closed_trials':len(attempts)","'closed_trials':closed_count,'passing_trial_digest':digest.hexdigest(),'stored_passing_examples_limit':40")
s=s.replace("'FP_ACCESS_RULE_EXACT_CLOSED_COUNTERCUT'","'FP_CREATOR_RULE_EXACT_CLOSED_COUNTERCUT'")
s=s.replace("'BOUNDED_FP_ACCESS_CUT_SEARCH_CHECKPOINT'","'BOUNDED_FP_CREATOR_CUT_SEARCH_CHECKPOINT'")
s=s.replace("all own-macro bits plus both source-tag proxies first-loss whole-access bits; A actions H1",
 "all own bits + both source-tag proxy first-loss accesses + H1 watched-edge birth whole-access bits")
s=s.replace("f'FP_access_countercut_{BATCH:02d}.json'","f'FP_creator_countercut_{BATCH:02d}.json'")
exec(compile(s,str(Path(__file__).resolve()),'exec'))
