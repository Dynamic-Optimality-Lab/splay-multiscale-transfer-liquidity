import json,time
import unary_grammar as G
if __name__=='__main__':
    error=None
    try:
        base=json.loads((G.B.parent/'SE03_STEP2_MULTICORE_FUNDING_CLOSURE_13/cheap_A_comparison.json').read_text())['reports'][0]['A_trees']
        r=G.generate(base);r['status']='COMPLETE_NECESSARY_UNARY_SOURCE_GRAMMAR';G.out('unary_grammar.json',r)
        print(json.dumps({'status':'PASS','states':len(r['states']),'H1':len(r['H1']),'H2':len(r['H2']),'source_calls':G.calls}),flush=True)
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:G.out('audit_grammar_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_engine_calls':G.calls})
