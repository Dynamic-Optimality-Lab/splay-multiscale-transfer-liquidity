import sys,time
import audit_bf_independent as m
if __name__=='__main__':
    error=None
    try:m.main(8)
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:m.out('audit_core8_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_engine_calls':m.calls})
