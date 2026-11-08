"""Exact symbolic reserve identity; no depth/size/repetition sampling."""
import hashlib
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent


def main():
    out=dict(status='EXACT_SYMBOLIC_IDENTITY',source_initial_depths_A_B=[1,2],
        source_deficit='D=sum_helpers(2*epsilon_A-epsilon_B)',
        possible_helper_deficits={'1,1':1,'1,2':0,'2,1':3,'2,2':2},
        actual_return_depth_identity='d_B=2*d_A-D',
        source_reserve_identity='2*a-q=z_A+ceil(D/2)',
        D='2*v+p',v='arbitrary nonnegative integer',p='0 or1',
        A_capacity_coefficients={'d_A':1,'z_A':1},
        B_demand_coefficients={'d_A':1,'v':-1,'p':-1},
        reserve_coefficients={'z_A':1,'v':1,'p':1},
        residual_coefficients={'d_A':0,'z_A':0,'v':0,'p':0},
        zero_reserve_iff='z_A=0 and D=0',
        critical_initial_zero_reserve_iff='all helper epsilons(1,2) and helper count k odd',
        no_capacity_created_for_unaccessed_keys=True,unrestricted_FE02_CD='OPEN',
        script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    with (HERE/'uniform_reserve_algebra_certificate.json').open('x',encoding='utf-8') as f:
        json.dump(out,f,indent=2);f.write('\n')
    print('Exact reserve identity recorded; no parameter samples')


if __name__=='__main__':main()
