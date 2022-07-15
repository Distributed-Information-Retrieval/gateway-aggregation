import time

def repeat():
    def decorator(func):
        def inner(self, *args, **kwargs):
            while True:
                func(self, *args, **kwargs)
        return inner
    return decorator