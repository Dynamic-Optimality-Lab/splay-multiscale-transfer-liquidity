"""Typed GSO composition gate; numerical coverage cannot bypass legality."""
import argparse
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent


def gate(*,source_binding,local_ordinary_histories,coverage,A_reuse,boundary_balance,interaction_budget):
    checks={'original_source_binding':source_binding,'local_ordinary_history_or_costed_interface':local_ordinary_histories,'literal_B_coverage':coverage,'global_original_A_reuse':A_reuse,'potential_boundary_balance':boundary_balance,'absolute_interaction_budget':interaction_budget}
    missing=[key for key,value in checks.items() if value!='PROVED_ALL_SOURCES']
    return {'root_status':'OPEN' if missing else 'PROVED_FROM_THE_DECLARED_PREMISES','first_missing':missing[0] if missing else None,'missing':missing,'checks':checks}


def status():
    return {'engine':'GSO physical composition backend1','root_status':'OPEN','result':'Exact obstruction to direct interval-history composition; temporal balance and raw physical A attribution proved.','composition_gate':gate(source_binding='PROVED_ALL_SOURCES',local_ordinary_histories='REFUTED_FOR_DIRECT_INTERVAL_RESTRICTION',coverage='PROVED_FOR_LITERAL_INTERNAL_VS_INTERFACE_PARTITION',A_reuse='PROVED_FOR_RAW_ATTRIBUTION_ONLY_LEGALIZATION_BUDGET_OPEN',boundary_balance='PROVED_FOR_FIXED_PROJECTED_ENDPOINTS_BUT_LOCAL_TRANSITION_LICENSE_MISSING',interaction_budget='OPEN_EQUIVALENT_TO_ORIGINAL_TARGET_FOR_FIXED_BLOCKS'),'unrestricted_overlapping_adaptive_composition':'OPEN','all_source_nonconstant_upper_bound':'O(log log n * log^2 log log n) A using the separately cited2026 external competitiveness theorem and checked periodic cost transport. The factor is not an absolute constant.','new_unrestricted_original_constant_obligations_deleted':0}


def main():
    p=argparse.ArgumentParser();p.add_argument('command',choices=('status','verify'));args=p.parse_args()
    if args.command=='status':print(json.dumps(status(),indent=2));return
    import subprocess,sys
    subprocess.run([sys.executable,'-B',str(HERE/'verify.py')],check=True,cwd=str(HERE.parent.parent))


if __name__=='__main__':main()
