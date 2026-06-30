The core idea
A context manager guarantees setup runs, and teardown runs no matter what — even if the body raises an exception or returns early. It's the clean replacement for try/finally.


# Without — easy to leak if something throws between open and close
f = open("data.txt")
data = f.read()        # if this raises, f.close() never runs → leaked file handle
f.close()

# With — close() is guaranteed, even on exception
with open("data.txt") as f:
    data = f.read()
# f is closed here, guaranteed
with is essentially this try/finally written for you:


f = open("data.txt")
try:
    data = f.read()
finally:
    f.close()          # always runs
The pattern matters anywhere you acquire something that must be released: files, DB connections/transactions, locks, sockets, temporary state changes.

The protocol: __enter__ and __exit__
Any object with these two methods is a context manager:


class Timer:
    def __enter__(self):
        from time import perf_counter
        self.start = perf_counter()
        return self                      # <- this is what `as t` receives

    def __exit__(self, exc_type, exc_val, exc_tb):
        from time import perf_counter
        self.elapsed = perf_counter() - self.start
        print(f"took {self.elapsed:.4f}s")
        # returning None/False → exceptions propagate normally

with Timer() as t:
    sum(range(10_000_000))
# prints: took 0.12s
Two things to lock in:

1. __enter__ return value = the as variable. with open(...) as f works because file.__enter__() returns the file. If you don't return self, as t would be None.

2. __exit__ always runs — on normal exit and on exception. Its three args tell you whether an exception occurred.

__exit__ and exceptions (the part most people miss)

def __exit__(self, exc_type, exc_val, exc_tb):
    ...
Normal exit: all three args are None.
Exception in the body: they hold the exception's type, value, and traceback.
Return value controls propagation:
return False/None → "I didn't handle it" → the exception propagates (default, what you want 99% of the time).
return True → "I handled it, swallow it" → the exception is suppressed.

class Suppress:
    def __init__(self, *exceptions):
        self.exceptions = exceptions
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        return exc_type is not None and issubclass(exc_type, self.exceptions)

with Suppress(ZeroDivisionError):
    x = 1 / 0          # swallowed, no crash
print("still running")  # runs
This is exactly how a DB transaction manager decides commit vs rollback:


class Transaction:
    def __init__(self, conn):
        self.conn = conn
    def __enter__(self):
        return self.conn
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.conn.commit()     # body succeeded → commit
        else:
            self.conn.rollback()   # body raised → roll back
        # return None → re-raise the error after rolling back
The shortcut: @contextmanager (uses your generator skills)
Writing a whole class is heavy. contextlib.contextmanager lets you write one with a generator — everything before yield is __enter__, everything after is __exit__:


from contextlib import contextmanager
from time import perf_counter

@contextmanager
def timer(label):
    start = perf_counter()
    try:
        yield                       # <- control goes to the `with` body here
    finally:
        print(f"{label}: {perf_counter() - start:.4f}s")

with timer("query"):
    sum(range(10_000_000))
Whatever you yield becomes the as variable.
The try/finally is how you guarantee cleanup even on exceptions — always put the teardown in finally.
This generator form is the idiomatic way to write most custom context managers. The class form is for when you need to store state across methods or reuse the object.

contextlib toolkit worth knowing

from contextlib import suppress, closing, nullcontext, ExitStack

# suppress — clean "ignore this error"
with suppress(FileNotFoundError):
    os.remove("maybe.txt")

# closing — make any object with .close() a context manager
with closing(urlopen(url)) as page:
    ...

# nullcontext — a no-op CM, useful for "optional" with-blocks
cm = open(path) if path else nullcontext()
with cm as f:
    ...

# ExitStack — manage a DYNAMIC number of context managers
with ExitStack() as stack:
    files = [stack.enter_context(open(p)) for p in paths]
    # all of them closed at the end, in reverse order
ExitStack is the pro tool — when you don't know how many resources you'll open until runtime.

Why this matters for your roadmap
Concurrency (your ✅): with lock: is a context manager — acquire on enter, release on exit, even if the body raises. You've used locks; now you know why with is the safe way.
Testing (your 🔴): unittest.mock.patch is a context manager (with patch(...)). Understanding CMs makes mocking click.
DB engineering (your 🔴): with transaction.atomic(): in Django is exactly the commit/rollback pattern above.
