"""Prepare only new original-event companions, using the sealed audit API."""
import sys
sys.dont_write_bytecode=True
import trace as X


def main():
    A=X.K.readonly_module('trace_pinned_source_audit',X.C.PREVIOUS/'source_audit.py')
    for i in range(13,18):
        z=X.K.load(X.HERE/f'run_001/trace_{i:02d}.json.gz');s=z['source'];n=len(s['initial_A']['children'])
        name=f'original_event_companions/trace_{i:02d}.json.gz'
        if (X.HERE/name).exists():continue
        selected={n//5+7} if i>=16 else {n+7}
        r=A.audit(s,selected);assert (r['A'],r['Q_B'])==(z['A'],z['Q_B'])
        X.write(name,r)
    print('Prepared five new complete original-event witnesses; old companions remain read-only.')


if __name__=='__main__':main()
