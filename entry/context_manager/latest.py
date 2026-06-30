'''
1. Class-based. Write a cd(path) context manager that chdirs into a directory on enter and always returns to the original directory on exit (even if the body raises). (import os; os.getcwd(), os.chdir().)

import os

class CdPath :
    def __init__(self, path) :
        self.path = path
        self.dir = [self.path]

    def __enter__(self) :
        try :
            # go to child directory code here
            dir = os.chdir(self.path)
            self.dir.append(dir)
        finally :
            return self.dir[0]
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        return self.dir[0]

2. Generator-based. Rewrite that same cd using @contextmanager. (This shows you the two styles side by side.)

import os
from contextlib import contextmanager

@contextmanager
def cd_path(path) :
    dir = [path]
    try :
        yield
    finally :
        return dir[0]

3. Exception handling judgment. In this code, does "done" print? Does the ValueError propagate? Explain why:


@contextmanager
def cm():
    print("enter")
    yield
    print("exit")          # <-- note: NOT in a finally
with cm():
    raise ValueError("boom")
print("done")
(Hint: this is a deliberate bug — figure out what goes wrong and how try/finally fixes it.)
done will not print the entire compiler will stuck after print enter then the valueerror and compiler can't go to next step and all gone
'''

'''
Q1 — corrected

import os

class CdPath:
    def __init__(self, path):
        self.path = path

    def __enter__(self):
        self.original = os.getcwd()   # 1. remember where we started
        os.chdir(self.path)           # 2. go into the target dir
        return self.path              #    (optional) what `as x` receives

    def __exit__(self, exc_type, exc_val, exc_tb):
        os.chdir(self.original)       # 3. ALWAYS go back — this is the point
        # return nothing → exceptions propagate normally
What was wrong in yours:

os.chdir() returns None, so dir = os.chdir(...) stored None.
You never went back to the original dir in __exit__ — so it didn't restore.
return inside a finally in __enter__ swallows errors and returns the wrong thing.
__exit__ returning self.dir[0] (a non-empty string = truthy) would secretly suppress every exception — a nasty hidden bug.
Why no try/finally here? Because the only thing between enter and exit is the user's body, and __exit__ is guaranteed by Python to run regardless. The language gives you the finally for free.

Q2 — corrected (generator style)
Same three actions; the finally is what guarantees the restore:


import os
from contextlib import contextmanager

@contextmanager
def cd_path(path):
    original = os.getcwd()    # remember origin
    os.chdir(path)            # go in   (= __enter__)
    try:
        yield path            # hand control to the `with` body
    finally:
        os.chdir(original)    # go back, no matter what  (= __exit__)
Yours never chdir'd at all, and did return dir[0] in finally — a generator CM should do the cleanup action, not return a value (that return is ignored). The teardown here is os.chdir(original), and it must be in finally so it runs even if the body raises.

Q3 — your conclusion was right, the reasoning wasn't
You said "done won't print" — ✅ correct. But "the compiler gets stuck" isn't what happens. Let me give you the precise trace, because the whole point is to see which line gets skipped:


@contextmanager
def cm():
    print("enter")
    yield
    print("exit")     # NOT in a finally
with cm():
    raise ValueError("boom")
print("done")
Step by step:

print("enter") → "enter" prints.
yield hands control to the body. The body raises ValueError.
That exception is thrown back into the generator at the yield line. Since there's no try/finally, execution jumps straight out — print("exit") is skipped, never runs. ← this is the bug.
The ValueError propagates out of the with.
So print("done") never runs; the program crashes with a traceback.
Result: enter prints, exit does NOT print, done does NOT print, ValueError propagates.

The lesson: cleanup placed after yield (not in finally) is lost whenever the body raises. The fix is exactly Q2's structure:


@contextmanager
def cm():
    print("enter")
    try:
        yield
    finally:
        print("exit")    # now guaranteed
Nothing is "stuck" — Python is doing exactly what it should: an unhandled exception unwinds the stack and stops the program. The bug is that the manager forgot to protect its cleanup.

The one sentence to remember
__enter__ does the setup action and returns the as-value; __exit__ does the teardown action and returns only True/False to decide whether to swallow the exception. Put teardown in finally (generator style) so it's guaranteed.

Quick re-do to confirm (then I'll flip to ✅)
Two short ones:

Write an @contextmanager called open_db(conn) that commits if the body succeeds and rolls back if it raises, and always works. (Pseudo conn.commit() / conn.rollback() is fine. Hint: you'll need try / except / else or try/except/raise.)

In your corrected CdPath.__exit__, if I want the manager to suppress FileNotFoundError (but let all other exceptions through), what exactly do I return, and based on which argument?
'''