import sys,json,time
from profiles import *
def main():
    g,h=map(int,sys.argv[1:3]);folder=BASE/f'p{g}_{h}';folder.mkdir(exist_ok=False);out=folder/'relation.json';start=time.process_time()
    counts=json.loads((BASE/'counts.json').read_text());row=next(p for p in counts['pairs'] if (p['g'],p['h'])==(g,h));assert row['count']<=1000000
    shadows=[];sid={};options=[];seen=[];cases=[];queries=0;nopt=0
    def ident(a):
        if a not in sid:sid[a]=len(shadows);shadows.append(a);options.append([]);seen.append(set())
        return sid[a]
    for helper,word in families(g,h):
        number,iterator,keys=generate(g,h,helper,word)
        if not number:continue
        family=len(cases);cases.append({'helper':helper,'word':word,'count':number});num=0
        for tree in iterator():
            queries+=1;num+=1;owner=tree[0];a=ident(observation(tree,owner));t=tree
            for p in word:t=move(t,p)
            b=ident(observation(t,owner));x=t[0]//16;H=len(word);key=(H,x,b,helper)
            if key not in seen[a]:
                seen[a].add(key);options[a].append([H,x,b,helper,family,encode(tree,keys)]);nopt+=1
            if queries%4096==0:assert queries<=1000000 and time.process_time()-start<120 and len(shadows)<2000000 and nopt<5000000,'UNKNOWN profile cap'
        assert num==number
    assert queries==row['count']
    result={'status':'COMPLETE_PREFIX_RELATION_UNAUDITED','g':g,'h':h,'keys':keys,'queries':queries,'classes':len(shadows),
      'option_count':nopt,'shadows':shadows,'options':options,'families':cases,'cpu_seconds':round(time.process_time()-start,3)}
    with out.open('x',encoding='utf-8') as f:json.dump(result,f,separators=(',',':'))
    print(json.dumps({k:v for k,v in result.items() if k not in ('shadows','options','families','keys')},indent=2),flush=True)
if __name__=='__main__':main()
