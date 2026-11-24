from verify_scoped_classes import geometry
from campaign3 import *


if __name__=='__main__':
    meter=Meter('historical_fringe_roots')
    archive=json.loads((PARENT/'EXP04_SOURCE_WITNESSES.json').read_text())
    srcs={s['name']:s for s in archive['inherited_sources']+archive['new_sources']}
    old=json.loads((C2/'INHERITED_LOCAL_PAYMENT_AUDIT.json').read_text())['sources'];out=[]
    for z in old:
        ds=z['original_events'];gmap={tuple(d['original_parent']):d['old_g'] for d in ds}
        out.append(geometry(srcs[z['source']],ds,gmap))
    write('HISTORICAL_FRINGE_ROOT_AUDIT.json',{'records':out,
        'scope':'Pinned original R_star, fresh actual A paths and rotation witnesses. Not a universal availability proof.'})
    print('audited',sum(len(z['records']) for z in out),'original gaps;',sum(len(z['fringe_paid_original_gaps']) for z in out),'immediate-fringe gaps',flush=True)
    meter.success=True
