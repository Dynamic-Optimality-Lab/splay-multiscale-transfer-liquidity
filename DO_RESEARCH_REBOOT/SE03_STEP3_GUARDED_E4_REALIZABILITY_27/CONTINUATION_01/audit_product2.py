"""Continue the bounded original-source product construction at a larger state cap.
The first bounded attempt, its code and all failures remain unchanged.
"""
from pathlib import Path
B=Path(__file__).resolve().parent
source=(B/'audit_product.py').read_text(encoding='utf-8')
source=source.replace('len(states)<22000','len(states)<120000')
source=source.replace("'product_graph_receipt.json'","'product2_graph_receipt.json'")
source=source.replace("'product_attempts.json'","'product2_attempts.json'")
source=source.replace("'audit_product_exit.json'","'audit_product2_exit.json'")
source=source.replace('for x,bf2 in full_moves(bf):','for x,bf2 in full_moves(bf):\n            C.queries+=1;C.check()')
exec(compile(source,str(B/'audit_product.py')+'[bounded-continuation]', 'exec'),globals())
