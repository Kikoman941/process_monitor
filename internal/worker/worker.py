from threading import Thread, Timer,  Event


class Worker(Thread):
    def __init__(self, fn):
        Thread.__init__(self)
        self._fn = fn
        self._stop = Event()
        self._connections = None

    def connect(self, *args):
        self._connections = args

    def start(self) -> True:
        for elem in self._connections:
            elem.start()
        _ = self._fn()
        self.stop()

    def stop(self):
        for elem in self._connections:
            elem.stop()
        self._stop.set()


class IntervalWorker(object):
    def __init__(self, t, fn):
        self._t = t
        self._fn = fn
        self._thread = Timer(self._t, self.handle_function)

    def handle_function(self):
        self._fn()
        self._thread = Timer(self._t, self.handle_function)
        self._thread.start()

    def start(self):
        self._fn()
        self._thread.start()

    def stop(self):
        self._thread.cancel()
