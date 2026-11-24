"""Do not mistake failure at capacity4 for failure of every finite constant."""
import sys
sys.dont_write_bytecode=True
import trace as X
import trace_teacher as T
import resource_audit as R


def main():
    cases=[]
    for i in range(18):
        z=X.K.load(X.HERE/f'run_001/trace_{i:02d}.json.gz');old=X.K.load(X.HERE/f'run_001/bank_{i:02d}.json.gz')
        if old['status']=='FINITE_EXACT_BANK':continue
        attempts=[];accepted=None
        for h in (5,6,8,16):
            b=T.bank(z,c=4,d=0,capacity=h);attempts.append({'capacity':h,'status':b['status'],'paid':b['paid'],'Q_B':b['demand']})
            X.write(f'bank_relax_001/source_{i:02d}_H{h}.json.gz',b)
            if b['status']=='FINITE_EXACT_BANK':
                X.write(f'bank_relax_001/resources_{i:02d}_H{h}.json.gz',R.decompose(z,b));accepted=h;break
        cases.append({'index':i,'name':z['source']['name'],'first_passing_tested_capacity':accepted,'attempts':attempts})
    result={'cases':cases,'c':4,'d':0,'scope':'A bounded capacity diagnostic on the declared source population. Neither a universal policy nor a refutation of all finite bank capacities.','root_status':'OPEN'}
    X.write('bank_relax_001/SUMMARY.json',result);print(result)


if __name__=='__main__':main()
