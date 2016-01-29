from .signals import sighandler, is_sighandler

class Args:
    def __init__(self, args, kwargs, n=0):
        self.args = args
        self.kwargs = kwargs
        self.n = n

class Bind:
    """
    Special argument of a callback
    Bound arguments will be evaluated when at callback calls
    """
    def bind(self, args, kwargs):
        pass

class ArgBind(Bind):
    "Bind from next argument of the callback call"
    def __init__(self, n=None):
        self.n = n
    def bind(self, cargs):
        n = self.n
        if n is None:
            n = cargs.n
            cargs.n += 1
        return cargs.args[n]

class NamedBind(Bind):
    "Bind from named argument of the callback call"
    def __init__(self, name):
        self.name = name
    def bind(self, cargs):
        return cargs.kwargs[self.name]

class BindCall(Bind):
    "Bind by calling a sub-callback"
    def __init__(self, callback):
        self.callback = callback
    def bind(self, cargs):
        return self.callback.call(cargs)

class Callback:
    "two-times calling of a function"
    def __init__(self, f, args, kwargs):
        self.f = f
        self.args = args
        self.kwargs = kwargs

    @classmethod
    def from_args(cls, f, *args, **kwargs):
        return cls(f, args, kwargs)

    @classmethod
    def eval(cls, obj, cargs):
        if isinstance(obj, Bind):
            return obj.bind(cargs)
        return obj

    def call(self, cargs):
        f = self.eval(self.f, cargs)
        args = (self.eval(arg, cargs) for arg in self.args)
        kwargs = {self.eval(k, cargs): self.eval(v, cargs) for (k, v) in self.kwargs.items()}
        return f(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        return self.call(Args(args, kwargs))

@sighandler
class SigCallback(Callback):
    "two-times calling of a signal (handle special args)"
    def __init__(self, f, args, kwargs):
        # game & sender arguments will be automatically bound (0 and 1)
        args = (ArgBind(0), ArgBind(1)) + args
        super().__init__(f, args, kwargs)

    def __call__(self, *args, **kwargs):
        return self.call(Args(args, kwargs, 2)) # 2 to pass game & sender in auto argbinds

def callback(f, *args, **kwargs):
    if is_sighandler(f):
        return SigCallback(f, args, kwargs)
    return Callback(f, args, kwargs)

class SugarBind(ArgBind):
    def __getstate__(self):
        return {}
    def __setstate__(self, state):
        pass
    def __getattr__(self, name):
        return NamedBind(name)
    def __getitem__(self, name):
        if isinstance(name, int):
            return ArgBind(name)
        if isinstance(name, str):
            return NamedBind(name)
        raise KeyError(name)
    def __call__(self, f, *args, **kwargs):
        if isinstance(f, int):
            return ArgBind(f)
        if isinstance(f, str):
            return NamedBind(name)
        return BindCall(callback(f, *args, **kwargs))
_ = SugarBind()
