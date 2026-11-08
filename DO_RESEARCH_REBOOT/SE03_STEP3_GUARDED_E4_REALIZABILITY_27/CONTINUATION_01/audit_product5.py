"""Resume the saved actual-source graph without repeating its expanded edges."""
from pathlib import Path
B=Path(__file__).resolve().parent
wrapper=(B/'audit_product3.py').read_text(encoding='utf-8').replace('product3_','product5_')
marker="exec(compile(source,str(B/'audit_product.py')+'[varied-source-prehistory]', 'exec'),globals())"
addition='''source=source.replace('len(states)<120000','len(states)<500000 and C.queries<330000')
old="base=(V,ee);states=[base];ids={base:0};parent=[None];adj=[];rev=[[]];queue=collections.deque([0])"
new="import pickle\\n    with (B/'product4_graph_cache.pkl').open('rb') as f:data=pickle.load(f)\\n    states=data['states'];ids=data['ids'];parent=data['parent'];adj=data['adj'];rev=data['rev'];queue=data['queue']"
assert old in source
source=source.replace(old,new)
source=source.replace('    # SCCs in the explored actual graph.',
    "    with (B/'product5_graph_cache.pkl').open('xb') as f:pickle.dump({'states':states,'ids':ids,'parent':parent,'adj':adj,'rev':rev,'queue':queue,'tour':tour,'u':u},f)\\n    # SCCs in the explored actual graph.")
'''
assert marker in wrapper
wrapper=wrapper.replace(marker,addition+marker)
exec(compile(wrapper,str(B/'audit_product3.py')+'[resume-saved-source-graph]', 'exec'),globals())
