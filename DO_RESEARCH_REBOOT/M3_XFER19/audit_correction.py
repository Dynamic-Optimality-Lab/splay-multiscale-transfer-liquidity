"""Strictly smaller complete-zero safe-correction construction.

No finite population/prefix/mask tests: all private productions and
legal masks are universal. Only critical target CORE types get an
unknown correction, and all potential source increases are checked.
"""
import json,sys,time,itertools
from pathlib import Path
import z3
from universal_grammar_v2 import build
from symbolic_prefix import PATHS
from compatibility import source_compatible
from complete_floor import lower_floor
from target_floor import N,opp,opposite_alpha
BASE=Path(__file__).resolve().parent;CAP=min(300,float(sys.argv[1]))
def write(name,obj):
    with (BASE/name).open('x',encoding='utf-8') as f:json.dump(obj,f,indent=2)
def freeze(t):return None if t is None else (t[0],freeze(t[1]),freeze(t[2]))
def main():
    assert z3.get_version_string()=='5.1.0'
    bank=json.loads((BASE.parent/'M3_LDR01/negative_run_census.json').read_text())
    tab=json.loads((BASE.parent/'M3_H1F01/cheap_census.json').read_text())
    ker=json.loads((BASE.parent/'M3_H2R01/fringe_kernel_certificate.json').read_text())
    ts=[freeze(q['tree']) for q in bank['nodes']];ids={t:i for i,t in enumerate(ts)}
    psi=[q['psi'] for q in bank['nodes']];dd=tab['B_depth'];nx=tab['B_destination']
    critical={}
    for i,t in enumerate(ts):
        if psi[i]==0:continue
        for x in range(9):
            if dd[i][x] in (4,5) and psi[i]>psi[nx[i][x]]:
                critical.setdefault((t[0],x,nx[i][x],psi[i]),[]).append(i)
    I={k[2] for k in critical};assert len(I)<=len(critical)==378
    print(json.dumps({'critical_groups':len(critical),'unknown_core_functions':len(I),'all_core_types':4862}),flush=True)
    mu=z3.Int('mask');rr,xx=z3.Ints('sourceRoot terminalScore')
    bits=[(mu/(1<<k))%2==1 for k in range(9)]
    legal=z3.And(mu>=0,mu<512,z3.Sum(*(z3.If(v,1,0) for v in bits))==5)
    proto=z3.Ints('floor_L floor_R floor_LL floor_LR floor_RL floor_RR')
    unknown={i:z3.Function('Correction_'+str(i),*[z3.IntSort()]*7,z3.IntSort()) for i in I}
    solver=z3.Solver();definitions=[];floors={};records=[];seen=set();dag=0
    def count_ast(e):
        nonlocal dag
        todo=[e]
        while todo:
            v=todo.pop();k=v.get_id()
            if k in seen:continue
            seen.add(k);dag+=1;assert dag<=4000000,'INPUT_DAG_CAP'
            todo.extend(v.children())
    T=N(2,N(0,None,N(1)),N(5,N(3,None,N(4)),N(6,None,N(7,None,N(8)))))
    def rt(t,a,b):return z3.And(z3.Not(b[4]),a[2]==4,a[6]==8) if t==T else z3.BoolVal(False)
    def get_floor(i):
        if i in floors:return floors[i]
        t=ts[i];r=t[0];a=(z3.IntVal(r),)+proto
        margin=[2-dd[i][x]//2+psi[nx[i][x]] for x in range(9)]
        pred=[]
        for k in (1,2):
            if psi[i]>=k:pred.append(z3.BoolVal(True));continue
            expr=z3.Or(lower_floor(t,a,bits,psi[i],margin,k),z3.Not(source_compatible(a)))
            if k==1:expr=z3.Or(expr,rt(t,a,bits),rt(opp(t),opposite_alpha(a),list(reversed(bits))))
            expr=z3.simplify(expr)
            if z3.is_true(expr) or z3.is_false(expr):pred.append(expr);continue
            fn=z3.Function('KnownFloor_'+str(i)+'_'+str(k),*[z3.IntSort()]*7,z3.BoolSort())
            definition=z3.ForAll([mu]+list(proto),fn(mu,*proto)==expr)
            solver.add(definition);definitions.append(definition);count_ast(definition);pred.append(fn)
        floors[i]=pred;return pred
    def lower(i,a):
        p=get_floor(i)
        one=p[0](mu,*a[1:]) if isinstance(p[0],z3.FuncDeclRef) else p[0]
        two=p[1](mu,*a[1:]) if isinstance(p[1],z3.FuncDeclRef) else p[1]
        return z3.If(two,z3.IntVal(2),z3.If(one,z3.IntVal(1),z3.IntVal(0)))
    def corr(i,a):
        if i not in unknown:return z3.IntVal(0)
        v=unknown[i](mu,*a[1:]);return z3.If(v<0,z3.IntVal(0),z3.If(v>2,z3.IntVal(2),v))
    words={}
    allfamilies=[(None,(p,)) for p in PATHS]
    for h in (0,9):
        first=[p for p in PATHS if p[0]==int(h==9)]
        second=[p for p in PATHS if p[0]==int(h==0)]
        allfamilies.extend((h,(p,q)) for p,q in itertools.product(first,second))
    assert len(allfamilies)==24
    for k,(helper,word) in enumerate(allfamilies):words[helper,word]=build(word,rr,xx,helper,'g'+str(k))
    def instance(helper,word,r,x):
        u=words[helper,word]
        repl=[(rr,z3.IntVal(r)),(xx,z3.IntVal(x))]
        # Eliminate forced physical labels/gaps by exact substitution.
        typnames={str(v):v for v in u['private_variables']}
        for p,(kind,label) in u['forced'].items():
            name='g'+str(allfamilies.index((helper,word)))
            tag=''.join(map(str,p)) or 'r'
            tv=typnames[name+'_type_'+tag]
            val=9 if kind=='F' else (r if p==() else x)
            repl.append((tv,z3.IntVal(val)))
            if kind=='F':repl.append((typnames[name+'_gap_'+tag],z3.IntVal(label)))
        # Root equality is independent, including old-root terminals.
        rootvar=typnames['g'+str(allfamilies.index((helper,word)))+'_type_r']
        if not any(rootvar.eq(p) for p,v in repl):repl.append((rootvar,z3.IntVal(r)))
        sub=lambda e:z3.simplify(z3.substitute(e,*repl))
        C=[sub(q) for q in u['constraints']]
        C.append(z3.IntVal(r)==z3.IntVal(x) if u['terminal_source_address']==() else z3.BoolVal(True))
        vs=[v for v in u['private_variables'] if not any(v.eq(p) for p,q in repl)]
        return C,tuple(sub(v) for v in u['source']),tuple(sub(v) for v in u['target']),vs
    def add_clause(kind,helper,word,i,x,j,w,k=None):
        assert time.process_time()<CAP-5 and len(records)<2000000
        r=ts[i][0];C,a,b,vs=instance(helper,word,r,x)
        static=z3.And(legal,bits[r],bits[x],*C)
        if z3.is_false(z3.simplify(static)):return
        target=z3.If(lower(j,b)>=corr(j,b),lower(j,b),corr(j,b))
        if kind=='ZERO':body=z3.Implies(static,target>=k)
        else:
            source=corr(i,a)
            body=z3.Implies(z3.And(static,source>lower(i,a)),w+target>=source)
        formula=z3.ForAll([mu]+vs,body)
        solver.add(formula);count_ast(formula)
        records.append({'kind':kind,'helper':helper,'word':word,'source_core':i,'target':x,
          'destination_core':j,'weight':w,'source_psi_requirement':k})
        if len(records)%1000==0:print(json.dumps({'clauses':len(records),'input_DAG':dag,'CPU':time.process_time()}),flush=True)
    for (r,x,j,k),sources in critical.items():
        for p in PATHS:
            if p[0]==int(x>r):add_clause('ZERO',None,(p,),sources[0],x,j,0,k)
    hrows={}
    mirror=[ids[opp(t)] for t in ts]
    for q in ker['rows']:
        if not q['gap0_childless_at_exit'] or q['w']>=2:continue
        i,x,j,w=q['entry_core'],q['target'],q['exit_core'],q['w']
        hrows[0,i,x]=(j,w);hrows[9,mirror[i],8-x]=(mirror[j],w)
    side_omitted=0
    for i in sorted(I):
        r=ts[i][0]
        for x in range(9):
            j=nx[i][x];w=2-dd[i][x]//2
            if w+psi[j]>=2:side_omitted+=1;continue
            for p in PATHS:
                if p[0]==int(x>r):add_clause('SIDE',None,(p,),i,x,j,w)
        for h in (0,9):
            for x in range(9):
                if (h,i,x) not in hrows:continue
                j,w=hrows[h,i,x]
                if w+psi[j]>=2:side_omitted+=1;continue
                for helper,word in allfamilies:
                    if helper==h:add_clause('SIDE',h,word,i,x,j,w)
    write('correction_schema.json',{'status':'COMPLETE_SYMBOLIC_CORRECTION_SYSTEM_ASSEMBLED',
      'correction_domain':sorted(I),'critical_groups':len(critical),'universal_clauses':records,
      'input_DAG_nodes':dag,'known_floor_definitions':len(definitions),'range_floor_omissions':side_omitted,
      'source_families':24,'impossible_helper_families_omitted_by_proof':54,
      'new_finite_population_or_mask_tests':0,'proof_target':'ALL remaining marked zero H1 plus signed source-increase safety'})
    remaining=CAP-time.process_time()-5;assert remaining>0
    print(json.dumps({'clauses_complete':len(records),'DAG':dag,'CPU_before_solve':time.process_time(),'remaining_CPU':remaining}),flush=True)
    solver.set(timeout=int(remaining*1000));v=solver.check()
    report={'status':'MODEL_REQUIRES_INDEPENDENT_AUDIT' if v==z3.sat else 'NO_COMPLETE_CORRECTION_CERTIFICATE',
      'solver_result':str(v),'reason':solver.reason_unknown() if v==z3.unknown else None,
      'new_symbolic_queries':1,'universal_clauses':len(records),'correction_core_count':len(I),
      'input_DAG_nodes':dag,'Step4_complete':False,'new_finite_population_or_mask_tests':0,
      'UNSAT_would_only_refute_this_stronger_correction_template':True}
    if v==z3.sat:
        model=solver.model();params=z3.Ints('public_mask public_L public_R public_LL public_LR public_RL public_RR')
        bodies={str(i):model.eval(fn(*params),model_completion=True).sexpr() for i,fn in unknown.items()}
        write('correction_raw_bodies.json',{'parameter_names':[str(p) for p in params],'function_bodies':bodies})
        with (BASE/'correction_model.smt2').open('x',encoding='utf-8') as f:f.write(model.sexpr())
    write('audit_correction.json',report);print(json.dumps(report,indent=2),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:
        error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:write('audit_correction_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error})
