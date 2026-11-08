import time,json
import branch_frames2 as G
if __name__=='__main__':
    error=None
    try:
        r=G.generate();G.out('branch_grammar2.json',r)
        print(json.dumps({'status':'PASS_COMPLETE_BRANCH_FRAME_SYNTAX','states':len(r['states']),'H1':len(r['H1']),'H2':len(r['H2']),'source_calls':G.calls}),flush=True)
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:G.out('audit_branch_grammar2_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_engine_calls':G.calls})
