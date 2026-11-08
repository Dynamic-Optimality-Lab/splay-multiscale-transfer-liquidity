"""Exact geodesic obstruction for all scalar normalizations; cached source."""
import json,time,sys,collections,hashlib,fractions
from pathlib import Path
B=Path(__file__).resolve().parent;START=time.process_time();CAP=float(sys.argv[1])
def fr(v):return tuple(map(fr,v)) if isinstance(v,list) else v
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def main():
    z=json.loads((B/'native10_source_actions.json').read_text());T=list(map(fr,z['trees']));idx={t:i for i,t in enumerate(T)}
    def neighbors(t):
        if isinstance(t,str):return []
        k,l,r=t;ans=[]
        if not isinstance(l,str):a,b,c=l;ans.append((a,b,(k,c,r)))
        if not isinstance(r,str):a,b,c=r;ans.append((a,(k,l,b),c))
        return ans+[(k,u,r) for u in neighbors(l)]+[(k,l,u) for u in neighbors(r)]
    adj=[[idx[u] for u in neighbors(t)] for t in T];old=json.loads((B/'native10_width2_source_countercertificate.json').read_text());records=[];cache={}
    for p in old['window_packets']:
        seg=[r for r in old['rows'] if r['occurrence'] in p['occurrences']];labels=[];dist=[]
        for state in (seg[0]['before'],seg[-1]['after']):
            a,b=(idx[fr(t)] for t in state[:2])
            if a not in cache:
                dd=[-1]*len(T);dd[a]=0;queue=collections.deque([a])
                while queue:
                    v=queue.popleft()
                    for u in adj[v]:
                        if dd[u]<0:dd[u]=dd[v]+1;queue.append(u)
                assert min(dd)>=0;cache[a]=dd
            labels.append({'source_index':a,'target_index':b,'distance_labels':cache[a]});dist.append(cache[a][b])
        records.append({'occurrences':p['occurrences'],'H':p['H'],'Q':p['Q'],'weight':p['weight'],'rho_before':dist[0],'rho_after':dist[1],'coefficient_rho_old_minus_new':dist[0]-dist[1],'exact_distance_certificates':labels})
    counter=json.loads((B/'geodesic_source_countercertificate.json').read_text());upper=fractions.Fraction(2*counter['H']-counter['Q'],counter['rho_after']-counter['rho_before']);low=[]
    for r in records:
        delta=r['coefficient_rho_old_minus_new'];w=r['weight']
        low.append({'delta':delta,'weight':w,'requires':str(fractions.Fraction(-w,delta)) if delta>0 else 'NO_NONNEGATIVE_LAMBDA'})
    impossible=any(q['requires']=='NO_NONNEGATIVE_LAMBDA' or fractions.Fraction(q['requires'])>upper for q in low)
    out('geodesic_scalar_obstruction.json',{'status':'ALL_SCALAR_GEODESIC_DEBTS_REFUTED' if impossible else 'SCALAR_COMPATIBILITY_NOT_REFUTED','candidate':'D=C-lambda*rho, lambda>=0','seven_source_upper_bound':str(upper),'ten_source_lower_bounds':low,'native10_negative_packets':records,'source_rows_reused':True,'new_source_queries':0,'input_sha256':{n:hashlib.sha256((B/n).read_bytes()).hexdigest() for n in ('native10_width2_source_countercertificate.json','geodesic_source_countercertificate.json','native10_source_actions.json')},'principal_U33':'OPEN','CD_refutation':False});print(json.dumps({'status':'ALL_SCALAR_GEODESIC_DEBTS_REFUTED' if impossible else 'NOT_REFUTED','upper':str(upper),'lower':low}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_proof28_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0})
