import sys,time
import bf_comparison as m
if __name__=='__main__':
    error=None
    try:m.main(9,sys.argv[1])
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:m.out('audit_bf9_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_engine_calls':m.calls})
