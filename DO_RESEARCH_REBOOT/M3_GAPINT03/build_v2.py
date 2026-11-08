import sys
sys.path.append('DO_RESEARCH_REBOOT/M3_GAPINT01')
from framework_v2 import build,load as read
from pathlib import Path
BASE=Path('DO_RESEARCH_REBOOT/M3_GAPINT03')
def load():return read(BASE)
def edge_info(c,a,u,e):
    ai=a['ordinary_a'][u]
    return {'source':u,'destination':a['targets'][e],'source_B':a['ordinary_b'][u],
      'destination_B':a['ordinary_b'][a['targets'][e]],'source_shadow':ai,'csr_edge':e,'w':a['weights'][e],**c['low_options'][ai][a['meta'][e]]}
if __name__=='__main__':build(3,BASE)
