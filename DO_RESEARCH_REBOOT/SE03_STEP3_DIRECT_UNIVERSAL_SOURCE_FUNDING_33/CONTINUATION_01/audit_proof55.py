"""Source-exact falsification search for positive per-key deficit inventories."""
import os
for name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS'):os.environ[name]='1'
import json,time,hashlib
from pathlib import Path
B=Path(__file__).resolve().parent
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def main():
    import numpy as np
    z=json.loads((B/'native10_source_actions.json').read_text());D=np.array(z['destination']);H=np.array(z['H']);Q=np.array(z['Q']);batches=[np.load(B/'nonlinear15_batch_01_actual_source_records.npz')['records'],np.load(B/'nonlinear15_transfer_01_actual_source_records.npz')['records']];tested=0;failure=None
    for number,rec in enumerate(batches):
        a,b=rec[:,0],rec[:,1];y=np.zeros(len(rec),dtype=np.int32) if rec.shape[1]==3 else rec[:,2];x=(rec[:,2] if rec.shape[1]==3 else rec[:,3])-1;ay=a.copy();mask=y>0;ay[mask]=D[a[mask],y[mask]-1];at=D[ay,x];bt=D[b,x];cost=H[ay,x].copy();cost[mask]+=H[a[mask],y[mask]-1];price=2*cost-Q[b,x];old=Q[b]-2*H[a];new=Q[bt]-2*H[at];before=np.stack(((old==1).sum(1),(old==2).sum(1)),axis=1);after=np.stack(((new==1).sum(1),(new==2).sum(1)),axis=1);bad=np.flatnonzero((before==after).all(1)&(price<0));tested+=len(rec)
        if len(bad):
            k=int(bad[0]);failure={'A':int(a[k]),'B':int(b[k]),'DELETE_helper_or_0':int(y[k]),'KEEP_target':int(x[k]+1),'A_after':int(at[k]),'B_after':int(bt[k]),'H':int(cost[k]),'Q':int(Q[b[k],x[k]]),'price':int(price[k]),'positive_deficit_inventory_before':before[k].tolist(),'positive_deficit_inventory_after':after[k].tolist(),'all_key_deficits_before':old[k].tolist(),'all_key_deficits_after':new[k].tolist(),'source_dataset':number,'source_row':k};break
    result={'status':'UNCHANGED_POSITIVE_DEFICIT_INVENTORY_NEGATIVE_PACKET' if failure else 'NO_SOURCE_INVENTORY_FAILURE_NOT_A_PROOF','definition':'delta_x=floor(depth_B(x)/2)-2ceil(depth_A(x)/2); inventory is multiset of POSITIVE delta_x only','native10_positive_deficits_at_sync_boundaries':'only1 or2; inventory encoded by the two multiplicities','source_packet_checks':tested,'failure':failure,'source_closed_embedding':'PENDING if failure exists','new_source_queries':0,'principal_U33':'OPEN'};out('positive_deficit_inventory_source_candidate.json',result);print(json.dumps(result))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_proof55_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0})
