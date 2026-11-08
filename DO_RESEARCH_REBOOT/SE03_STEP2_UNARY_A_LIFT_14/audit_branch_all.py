import json,sys,time
import branch_all as A
if __name__=='__main__':
    error=None
    try:A.main(sys.argv[1])
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:A.out('audit_branch_all_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_engine_calls':A.calls})
