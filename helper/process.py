import threading as thread

class Process(thread.Thread):
    def __init__(self, obj, method):
        thread.Thread.__init__(self)
        self.obj_ = obj
        self.method_ = method

    def run(self):
        getattr(self.obj_, self.method_)()