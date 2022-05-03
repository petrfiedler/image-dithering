from threading import Thread
import sys


class KThread(Thread):
    """ Modify Thread class to support killing method.

    hack from: https://blog.finxter.com/how-to-kill-a-thread-in-python/
    """

    def __init__(self, *args, **kwargs):
        Thread.__init__(self, *args, **kwargs)
        self.killed = False

    def start(self):
        # replace the default run method
        self.runOld = self.run
        self.run = self.runWithTrace
        Thread.start(self)

    def runWithTrace(self):
        sys.settrace(self.globaltrace)
        self.runOld()
        self.run = self.runOld

    def globaltrace(self, _frame, why, _arg):
        if why == 'call':
            return self.localtrace
        else:
            return None

    def localtrace(self, _frame, why, _arg):
        if self.killed:
            if why == 'line':
                raise SystemExit()
        return self.localtrace

    def kill(self):
        self.killed = True
