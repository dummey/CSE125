import logging

class Signal(object):
    def __init__(self, *args):
        self.callbacks = []
        logging.debug("signal with arguments {}".format(args))
        self.args = args

    def __str__(self):
        return "Signal({})".format(", ".join(self.args))

    def register(self, callback):
        self.callbacks.append(callback)

    def send(self, *args, **kwargs):
        assert len(args) + len(kwargs) == len(self.args) # pass the right arguments
        for callback in self.callbacks:
            callback(*args, **kwargs)
