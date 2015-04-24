# set up logging #####################################
import sys,logging,logging.handlers,os.path
#in this particular case, argv[0] is likely pythonservice.exe deep in python's lib\
# so it makes no sense to write log there
log_file=os.path.splitext(__file__)[0]+".log"
l = logging.getLogger()
l.setLevel(logging.DEBUG)
f = logging.Formatter('%(asctime)s %(process)d:%(thread)d %(name)s %(levelname)-8s %(message)s')
h=logging.StreamHandler(sys.stdout)
h.setLevel(logging.NOTSET)
h.setFormatter(f)
l.addHandler(h)
h=logging.handlers.RotatingFileHandler(log_file,maxBytes=1024**2,backupCount=1)
h.setLevel(logging.NOTSET)
h.setFormatter(f)
l.addHandler(h)
del h,f
#hook to log unhandled exceptions
def excepthook(type,value,traceback):
    logging.error("Unhandled exception occured",exc_info=(type,value,traceback))
    #Don't need another copy of traceback on stderr
    if old_excepthook!=sys.__excepthook__:
        old_excepthook(type,value,traceback)
old_excepthook = sys.excepthook
sys.excepthook = excepthook
del excepthook,log_file
# ####################################################

import win32serviceutil, argparse
import rpyc.utils.server, rpyc.core, rpyc.utils.classic

class RPyCService(win32serviceutil.ServiceFramework):
    _svc_name_="RPyCService"
    _svc_display_name_="RPyCService"
    _svc_description_="""RPyC's rpyc_classis service wrapper"""
    _svc_deps_=("tcpip",)
    def SvcDoRun(self):
        l.info("Starting service")
        #launch method taken from rpyc_classic.serve_threaded()
        #the constructor binds a named logger automatically
        self.t = rpyc.utils.server.ThreadedServer(
				rpyc.core.SlaveService,
				port=rpyc.utils.classic.DEFAULT_SERVER_PORT)
        self.t.start()
    def SvcStop(self):
        l.info("Stopping service")
        self.t.close()

if __name__=='__main__':
    win32serviceutil.HandleCommandLine(RPyCService)
