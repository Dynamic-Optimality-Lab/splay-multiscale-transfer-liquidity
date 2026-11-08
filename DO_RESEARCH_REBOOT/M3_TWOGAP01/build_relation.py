"""Enumerate the complete finite prefix superrelation, without a B product."""
from prefix_profiles_v2 import *
def main():
    start=time.process_time();out=BASE/'relation.json';assert not out.exists()
    shadows=[];sid={};opts=[];seen=[];witnesses=[];counts=[];queries=0;edges=0
    def ident(a):
        if a not in sid:
            sid[a]=len(shadows);shadows.append(a);opts.append([]);seen.append(set())
        return sid[a]
    for word in cases():
        expected,gen,_=genword(word);n=0
        if not expected:continue
        for tree in gen():
            n+=1;queries+=1
            assert queries<=1000000 and time.process_time()-start<120,'UNKNOWN enumeration cap'
            owner=tree[0];src=shadow(tree,owner);a=ident(src);t=tree;targets=[]
            for p in word:
                targets.append(get(t,p)[0]);t=access_path(t,p)
            assert core(targets[-1]);assert len(word)==1 or targets[0]==-8
            dst=shadow(t,owner);b=ident(dst);H=len(word);x=targets[-1]//16
            key=(H,x,b)
            if key not in seen[a]:
                seen[a].add(key);wi=len(witnesses);witnesses.append({'tree':tree,'paths':word,'targets':targets})
                opts[a].append({'H':H,'target':x,'destination':b,'witness':wi});edges+=1
            assert len(shadows)+len(witnesses)<2000000 and edges<=5000000,'UNKNOWN live profile cap'
        assert n==expected,(word,n,expected)
        counts.append({'word':word,'count':n})
        print(json.dumps({'word':word,'count':n,'queries':queries,'shadows':len(shadows),'options':edges}),flush=True)
    assert queries==462916
    old=json.loads(Path('DO_RESEARCH_REBOOT/M3_GAPMULTI01/obstruction.json').read_text())
    controls=[]
    for r in old['records']:
        s=normalize(r['source']['alpha']);t=normalize(r['destination']['alpha']);a=sid[s];b=sid[t]
        found=[o for o in opts[a] if o['H']==1 and o['target']==6 and o['destination']==b];assert found
        controls.append({'label':r['label'],'source_class':a,'destination_class':b,'matching_options':len(found)})
    obj={'status':'COMPLETE_FINITE_SUPERRELATION_UNAUDITED','queries':queries,'classes':len(shadows),'options_count':edges,
      'shadows':shadows,'options':opts,'witnesses':witnesses,'case_counts':counts,'equal_state_controls':controls,
      'cpu_seconds':round(time.process_time()-start,3),'original_sign_theorem':False,
      'representation':'all private branch choices retained; normalized RAW alpha, no S port filling'}
    with out.open('x',encoding='utf-8') as f:json.dump(obj,f,separators=(',',':'))
    print(json.dumps({k:v for k,v in obj.items() if k not in ('shadows','options','witnesses','case_counts')},indent=2),flush=True)
if __name__=='__main__':main()
