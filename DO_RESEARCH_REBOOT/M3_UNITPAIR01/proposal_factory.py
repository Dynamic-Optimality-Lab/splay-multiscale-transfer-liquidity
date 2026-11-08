"""Clone non-authoritative fixture functions; original checker remains authoritative."""
import ast,inspect
from types import SimpleNamespace
def proposals(module):
    result=SimpleNamespace(**vars(module));edits=[]
    for name in ('low','high'):
        function=getattr(module,name);parsed=ast.parse(inspect.getsource(function));count=0
        class RemoveDuplicate(ast.NodeTransformer):
            def visit_Assert(self,node):
                nonlocal count
                t=node.test
                if isinstance(t,ast.Call) and isinstance(t.func,ast.Attribute) and t.func.attr=='ev_ground' and isinstance(t.func.value,ast.Name) and t.func.value.id=='d':
                    count+=1;return None
                return node
        parsed=RemoveDuplicate().visit(parsed);ast.fix_missing_locations(parsed);assert count==1
        namespace=dict(vars(module));exec(compile(parsed,__file__+':'+module.__name__+'.'+name,'exec'),namespace)
        setattr(result,name,namespace[name]);edits.append({'module':module.__name__,'function':name,'duplicate_root_assertions_removed':count})
    result.proposal_edits=edits;return result
