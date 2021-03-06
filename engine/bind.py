from .signals import sighandler, is_sighandler

class Args:
    """
    Object representing (args, kwargs) of a function call
    `n` contains the position of the last-bound argument
    """
    def __init__(self, args, kwargs, n=0):
        self.args = args
        self.kwargs = kwargs
        self.n = n

class Bind:
    """
    Special argument of a callback
    Bound arguments will be evaluated when at callback calls
    """
    def bind(self, cargs):
        'Bind value from call-parameters (cargs is an instance of Args)'
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

class LateBind(Bind):
    "Bind to an object that can be changed before call"
    def __init__(self, value=None):
        self.value = value
    def bind(self, cargs):
        return self.value

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
        'Evaluate an argument (obj)'
        if isinstance(obj, Bind):
            return obj.bind(cargs)
        return obj

    def call(self, cargs):
        'Evaluate parameters (bind) and call the function'
        f = self.eval(self.f, cargs)
        args = tuple(self.eval(arg, cargs) for arg in self.args)
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
    "Create a callback from a function (signal-callback if function is a sighandler)"
    if is_sighandler(f):
        return SigCallback(f, args, kwargs)
    return Callback(f, args, kwargs)
cb = callback

class SugarBind(ArgBind):
    "Helpers to create bindings"
    def __getstate__(self):
        return {}
    def __setstate__(self, state):
        self.n = None
    def __getattr__(self, name):
        "_.foo -> NamedBind('foo')"
        return NamedBind(name)
    def __getitem__(self, name):
        '''_[1] -> ArgBind(1)
        _['foo'] -> NamedBind('foo')
        '''
        if isinstance(name, int):
            return ArgBind(name)
        if isinstance(name, str):
            return NamedBind(name)
        raise KeyError(name)
    def __call__(self, f, *args, **kwargs):
        '''_(1) -> ArgBind(1)
        _('foo') -> NamedBind('foo')
        _(f, ...) -> BindCall(callback(f, ...))
        '''
        if isinstance(f, int):
            return ArgBind(f)
        if isinstance(f, str):
            return NamedBind(f)
        return BindCall(callback(f, *args, **kwargs))
_ = SugarBind()
