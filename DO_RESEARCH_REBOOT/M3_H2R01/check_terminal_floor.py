"""Complete finite checks supporting the universal zero-fringe H=2 debt law."""
import sys,json,time,hashlib
from pathlib import Path
sys.path.insert(0,'DO_RESEARCH_REBOOT/M3_CHR01')
from fragment_graph import load,BASE as OLD_BASE
from terminal_potential import CappedPotential,CATALOG
OUT=Path('DO_RESEARCH_REBOOT/M3_H2R01/terminal_floor_certificate.json')

def main():
    assert not OUT.exists();start=time.process_time();c,a=load();P=CappedPotential()
    psi=P.psi;potential=P.joint.p;checks=0
    for u,b in enumerate(a['ordinary_b']):
        assert -2<=potential[u]<=-psi[b];checks+=1
    edges=json.loads(CATALOG.read_text())['edges'];rows=[];physical_checks=0
    for e in edges:
        q=e['depth']//2;delta=q-2;s=e['source'];t=e['destination']
        assert q in (3,4) and psi[t]>=psi[s]+delta and psi[t]>=delta
        checks+=1;root=P.trees[t][1];vals=[]
        if root in c['mask']:
            base=c['B_bases'][t]
            for j,ai in enumerate(c['shadows_by_root'][str(root)]):
                v=potential[base+j];assert v<=-delta
                vals.append(v);checks+=1;physical_checks+=1
        assert checks<=1000000 and time.process_time()-start<120,'UNKNOWN: certificate cap'
        rows.append({**e,'terminal_q':q,'psi_destination':psi[t],
                     'capped_destination_upper_bound':-delta,
                     'physical_destination_checks':len(vals),
                     'physical_maximum':max(vals) if vals else None,
                     'physical_values_sha256':hashlib.sha256(json.dumps(vals).encode()).hexdigest()})
    result={'status':'COMPLETE','old_joint_ordinary_values_checked':len(a['ordinary_b']),
            'terminal_rows':len(rows),'physical_destination_checks':physical_checks,
            'total_checks':checks,'ordinary_range':[-2,0],'joint_below_negative_psi':True,
            'all_masks_and_A_shadows_via_fallback':'capped value <= -psi by definition',
            'q4_destination_bound':-2,'q3_destination_bound':-1,
            'cpu_seconds':round(time.process_time()-start,3),'rows':rows}
    with OUT.open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)
    print(json.dumps({k:v for k,v in result.items() if k!='rows'}),flush=True)
if __name__=='__main__':main()
