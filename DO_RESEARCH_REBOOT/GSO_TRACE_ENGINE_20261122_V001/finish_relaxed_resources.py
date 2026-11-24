"""Add literal provenance to already preserved capacity5 bank certificates."""
import sys
sys.dont_write_bytecode=True
import trace as X
import resource_audit as R


def main():
    for i in (11,12,14,15):
        z=X.K.load(X.HERE/f'run_001/trace_{i:02d}.json.gz');b=X.K.load(X.HERE/f'bank_relax_001/source_{i:02d}_H5.json.gz');name=f'bank_relax_001/resources_{i:02d}_H5.json.gz'
        if not (X.HERE/name).exists():X.write(name,R.decompose(z,b))
    print('Added four complete finite funding maps with shared c=4 and capacity5.')


if __name__=='__main__':main()
