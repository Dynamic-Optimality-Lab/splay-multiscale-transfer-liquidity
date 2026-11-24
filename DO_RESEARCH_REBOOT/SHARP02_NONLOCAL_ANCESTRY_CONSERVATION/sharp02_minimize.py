"""Greedy controlled source minimization; every proposal is warmed and closed."""
from sharp02_common import *
from sharp02_fast import evaluate,recurrent
from sharp02_graph import solve
from sharp01_oracle import vine

def main():
    with Run('minimize_principal_witness_v001',limit=90) as run:
        raw=read(BASE/'SHARP02_PRINCIPAL_COUNTEREXAMPLE_RAW.json');best=raw['source'];word=best.get('generating_word',best['operations'])
        diag=best.get('diagonal_initial',best['initial_A']);history=[];trials=0
        def test(w,st):
            nonlocal trials
            trials+=1
            ss=recurrent({'name':'minimization_diagonal','initial_A':st,'initial_B':st,'reaching_prefix':[]},w,f'S02_min_trial_{trials}')
            if ss is None:return None
            d=evaluate(ss)
            if d['Delta']>0:
                write(BASE/'SHARP02_POSSIBLE_SHARP_COUNTEREXAMPLE.json',{'source':ss});raise RuntimeError('positive scalar deficit; independent replay required')
            if not d['U']:return None
            rr=solve(d['weights'],d['adj'],d['free'],tight=False)
            if not rr['unmatched']:return None
            oo=solve(d['weights'],d['all_adj'],d['units'],d['capacities'],tight=False)
            return ss,d,rr,oo
        def accept(ans,w,st,why):
            nonlocal best,word,diag
            best,d,rr,oo=ans;word=[list(x) for x in w];diag=st
            history.append({'reason':why,'n':d['n'],'word_length':len(word),'period_length':d['operations'],
                'A':d['A'],'Q':d['Q'],'U':d['U'],'C':d['C'],'unmatched':rr['unmatched'],'optimized_unmatched':oo['unmatched']})
            write(BASE/'SHARP02_MINIMIZED.checkpoint.json',{'source':best,'history':history,'trials':trials})
        changed=True
        while changed:
            changed=False
            for chunk in (max(1,len(word)//4),max(1,len(word)//8),1):
                i=0
                while i<len(word):
                    if time.process_time()-run.t>80:break
                    w=word[:i]+word[i+chunk:]
                    ans=test(w,diag) if w else None
                    if ans:accept(ans,w,diag,f'delete {chunk} operations at {i+1}');changed=True
                    else:i+=max(1,chunk)
            # A NEW smaller universe is a controlled source construction, never
            # physical deletion during a KEEP/DELETE period. Retain its own diagonal.
            keys=sorted(map(int,diag['children']))
            for key in keys:
                if len(keys)<=7:break
                smaller=[k for k in keys if k!=key];st=vine(smaller);w=[list(op) for op in word if op[1]!=key]
                ans=test(w,st) if w else None
                if ans:accept(ans,w,st,f'new universe omits key {key}');keys=smaller;changed=True
            run.check(trials=trials,accepted=len(history),current_n=len(diag['children']),current_word_length=len(word))
            if time.process_time()-run.t>75:break
        # Rank normalize while retaining every surviving physical key and edge.
        keys=sorted(map(int,diag['children']));mp={k:i+1 for i,k in enumerate(keys)}
        normalized=vine(range(1,len(keys)+1));nw=[[tag,mp[x]] for tag,x in word]
        ans=test(nw,normalized)
        if ans:accept(ans,nw,normalized,'order-preserving rank normalization')
        best['name']='SHARP02_MINIMAL_RESERVATION_OBSTRUCTION';best['family']='SHARP02_minimized_counterexample'
        d=evaluate(best);rr=solve(d['weights'],d['adj'],d['free']);oo=solve(d['weights'],d['all_adj'],d['units'],d['capacities'])
        result={'source':best,'summary':{k:d[k] for k in ('n','operations','A','Q','U','C','Delta')},'broad':rr,'optimized':oo,
                'trials':trials,'accepted_transformations':history,'minimality':'greedy deletion/key-universe local minimization only; no globally shortest source claim'}
        write(BASE/'SHARP02_MINIMIZED_COUNTEREXAMPLE.json',result)
        print(json.dumps({k:v for k,v in result.items() if k not in ('source','accepted_transformations')}))

if __name__=='__main__':main()
