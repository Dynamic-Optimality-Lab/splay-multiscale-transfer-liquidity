"""Original packet provenance for the current source grammar (not a simulator)."""
import json
from pathlib import Path
B=Path(__file__).resolve().parent
class Resolver:
    def __init__(self):
        import numpy as np
        self.native=json.loads((B/'native10_source_actions.json').read_text());self.template=np.load(B/'nonlinear_feature_projected_graph.npz')['source_records'];self.spec=json.loads((B/'diagonal_zero_source_spec.json').read_text());self.vine=np.load(B/'diagonal_zero_vine_full_arrays.npz')['source_records'];self.neg=np.load(B/'nonlinear15_batch_01_actual_source_records.npz')['records'];self.transfer=np.load(B/'nonlinear15_transfer_01_actual_source_records.npz')['records'];self.ranges=[len(self.template),len(self.spec['extra_source_origins']),len(self.vine),len(self.neg),len(self.transfer)]
    def resolve(self,e):
        n=self.native;offset=0
        for kind,size in zip(('template','corpus','vine','negative_H1','signed_transfer'),self.ranges):
            if offset<=e<offset+size:break
            offset+=size
        else:raise ValueError('Unknown original source edge')
        i=e-offset
        if kind=='corpus':return {'global_edge':e,'kind':kind,'origin':self.spec['extra_source_origins'][i]}
        rec=(self.template if kind=='template' else self.vine if kind=='vine' else self.neg if kind=='negative_H1' else self.transfer)[i];a,b=map(int,rec[:2]);y,x=(0,int(rec[2])) if len(rec)==3 else (int(rec[2]),int(rec[3]));ay=n['destination'][a][y-1] if y else a;h=(n['H'][a][y-1] if y else 0)+n['H'][ay][x-1];q=n['Q'][b][x-1];return {'global_edge':e,'kind':kind,'A':a,'B':b,'DELETE_helper_or_0':y,'KEEP_target':x,'A_after':n['destination'][ay][x-1],'B_after':n['destination'][b][x-1],'H':h,'Q':q,'price':2*h-q}
