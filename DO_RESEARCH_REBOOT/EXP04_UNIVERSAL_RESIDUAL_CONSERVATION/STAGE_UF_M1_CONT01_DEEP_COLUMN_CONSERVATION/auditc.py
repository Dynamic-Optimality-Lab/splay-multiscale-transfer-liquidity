from basec import *
from birthc import reconstruct
import ast,gc

def known_star(entry):
    if entry['origin']=='M0':
        return load(M0/'RESIDUAL_AUDIT.json')[entry['index']]['original_R_star']
    i=entry['index'];pi=M1/f'NEW_ORIGINAL_PI_{i:02}.json'
    if pi.exists():return load(pi)['original_R_star']
    if entry['source']['family']=='matched_root_toggle_volume_test':return []
    return None

def compare_reference(entry,result):
    ref=None
    if entry['origin']=='M0' and entry['index']<6:
        z=load(base0.C5/'INDEPENDENT_RESULTS.json')[entry['index']]
        if z.get('full_original_Pi'):ref=z['immutable_primitive_check']['independently_reconstructed_all_original_U']
    if entry['origin']=='M1':
        p=M1/f'NEW_ORIGINAL_PI_{entry["index"]:02}.json'
        if p.exists():ref=load(p)['independent_Pi']['independently_reconstructed_all_original_U']
    if ref is None:return 'No earlier full independent U record compared in this call.'
    assert set(ref)==set(result['U'])
    for key,z in ref.items():
        for fld,val in z.items():assert result['U'][key][fld]==val,(entry['source']['name'],key,fld)
    return 'Exact all-U IDs, Gamma/kappa/postA and hit/exposure metadata match earlier independent certificate.'

if __name__=='__main__':
    meter=Meter('birth_and_extreme_audit');out=[];catalog=controls()
    write('SOURCE_CATALOG.json',[{**z,'source_sha256':digest(z['source']),
        'input_sha256':{k:hfile(z[k]) for k in ('physical','forest','weights','M1_audit')}} for z in catalog])
    for i,entry in enumerate(catalog):
        s=entry['source'];phys=load(entry['physical']);forest=load(entry['forest']);m1audit=load(entry['M1_audit']);w=load(entry['weights'])
        assert s['name']==phys['source']==forest['source'] and digest(s)==phys['source_sha256']
        z=reconstruct(s,phys,forest,m1audit,known_star(entry),w)
        z['reference_Pi_comparison']=compare_reference(entry,z)
        write(f'BIRTH_{i:02}.json',z)
        row={k:v for k,v in z.items() if k not in ('U','double_classes','C_U_births','deep_original_R_star_C_births',
            'original_cohorts','original_pairs','original_R6','eligible_S_operations','eligible_I_operations','original_I')}
        row['original_R6_count']=len(z['original_R6'])
        row['U_count']=len(z['U']);row['index']=i;row['audit_file']=f'BIRTH_{i:02}.json'
        row['counts_by_C_birth_kind']=dict(Counter(v['output_kind'] for v in z['C_U_births']))
        row['counts_by_deep_C_status']=dict(Counter(v['status'] for v in z['C_U_births'] if v['distance']>2))
        out.append(row);write('BIRTH_RESULTS.json',out)
        print('PASS',i,s['name'],'U',len(z['U']),'deep U-C',z['all_deep_U_C'],'nonU births',z['nonU_deep_U_C'],flush=True)
        del z,phys,forest,m1audit,w;gc.collect()
    meter.info.update(complete_sources=len(out));meter.ok=True
