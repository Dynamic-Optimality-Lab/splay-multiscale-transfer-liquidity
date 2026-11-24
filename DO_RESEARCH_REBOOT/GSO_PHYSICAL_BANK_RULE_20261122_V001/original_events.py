"""Old original-model producer for the two complete new obstruction witnesses."""
import sys
sys.dont_write_bytecode=True
import bank_rule as B


def main():
    for key,path in [('H8','scaling_001/trace_08.json.gz'),('W_H1','counter_001/W_H1_complete_trace.json.gz')]:
        z=B.K.load(B.HERE/path);s=z['source'];A=z['A'];Q=z['Q_B'];del z
        r=B.K.OLD.replay(s);assert (r['A'],r['Q_B'])==(A,Q)
        out={'source':s,'A':r['A'],'Q_B':r['Q_B'],'S':r['S'],'original_U':r['demands'],'real_rotations':r['rotations'],'period_clock':r['period_clock'],'reaching_rotations':r['reach_rotations'],'scope':'Literal old original-model producer, including every full cyclic Pi test; independently rechecked by verify.py.'}
        B.write(f'counter_001/{key}_original_events.json.gz',out);print({'source':key,'A':A,'Q_B':Q,'original_U':len(r['demands']),'real_rotations':r['rotations']},flush=True)


if __name__=='__main__':main()
