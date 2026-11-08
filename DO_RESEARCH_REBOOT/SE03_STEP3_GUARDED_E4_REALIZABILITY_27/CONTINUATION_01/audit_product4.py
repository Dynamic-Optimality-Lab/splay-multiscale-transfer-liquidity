"""Larger bounded source-product construction with a reusable graph checkpoint."""
from pathlib import Path
B=Path(__file__).resolve().parent
wrapper=(B/'audit_product3.py').read_text(encoding='utf-8')
wrapper=wrapper.replace('product3_','product4_')
wrapper=wrapper.replace('len(states)<120000','len(states)<350000')
marker="exec(compile(source,str(B/'audit_product.py')+'[varied-source-prehistory]', 'exec'),globals())"
addition='''source=source.replace('len(states)<350000 and time.process_time()',
    'len(states)<350000 and C.queries<780000 and time.process_time()')
source=source.replace('min(12,CAP-5)','min(10,CAP-7)')
source=source.replace('    # SCCs in the explored actual graph.',
    "    import pickle\\n    with (B/'product4_graph_cache.pkl').open('xb') as f:pickle.dump({'states':states,'ids':ids,'parent':parent,'adj':adj,'rev':rev,'queue':queue,'tour':tour,'u':u},f)\\n    # SCCs in the explored actual graph.")
'''
assert marker in wrapper
wrapper=wrapper.replace(marker,addition+marker)
exec(compile(wrapper,str(B/'audit_product3.py')+'[larger-checkpointed-source-product]', 'exec'),globals())
