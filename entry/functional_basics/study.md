The one core idea
Functional programming = build behavior out of functions that take input and return output, and avoid changing things in place. That's it. Everything below is a consequence.

The enemy is hidden state changes. The more your code's result depends only on its inputs (not on "what happened before"), the easier it is to test, reason about, cache, and parallelize.

1. Pure functions
A function is pure if:

Same input → always same output (no dependence on external/changing state).
No side effects (doesn't mutate anything outside itself, no I/O, no printing, no DB writes).

# PURE — depends only on args, changes nothing outside
def total_price(items, tax_rate):
    return sum(i.price for i in items) * (1 + tax_rate)

# IMPURE — reads external state + mutates external state + does I/O
discount = 0.1                      # external state
def total_price_bad(items):
    global discount
    discount += 0.01                # mutation of outside world (!)
    print("calculating...")         # side effect (I/O)
    return sum(i.price for i in items) * (1 - discount)
Why you should care (directly ties to your roadmap):

Testing (your 🔴 gap): a pure function needs no mocks, no DB, no setup. assert total_price(items, 0.1) == 110. Done. The reason mocking is hard is impure code — so writing pure functions is how you make testing easy.
Caching: pure functions can be memoized safely (@lru_cache) — impure ones can't.
Concurrency (your ✅ area): pure functions are thread-safe by definition — no shared mutable state to race on.
2. Side effects — isolate them at the edges
You can't avoid side effects entirely (you must eventually write to a DB, call an LLM, print). The skill is pushing them to the boundary and keeping the core pure. This is the "functional core, imperative shell" pattern:


# IMPURE SHELL (edge): does I/O
def handle_order(order_id):
    order = db.get(order_id)               # side effect: read
    total = compute_total(order.items)     # <- pure core
    db.save_total(order_id, total)         # side effect: write

# PURE CORE: all the logic, fully testable, no I/O
def compute_total(items):
    return sum(i.price * i.qty for i in items)
Notice: all the interesting logic is pure and trivially testable; the messy I/O is a thin wrapper. This single habit will make your testing gap dramatically easier to close.

3. Immutability
Don't change data in place — produce new data. In Python:


# MUTATION (functional style avoids this)
def add_tax(prices):
    for i in range(len(prices)):
        prices[i] *= 1.1     # mutates the caller's list — spooky action at a distance
    return prices

# IMMUTABLE — returns a new list, original untouched
def add_tax(prices):
    return [p * 1.1 for p in prices]
Python's immutable tools:

Need	Mutable	Immutable version
sequence	list	tuple
set	set	frozenset
record	dict / class	@dataclass(frozen=True) or NamedTuple

from dataclasses import dataclass, replace

@dataclass(frozen=True)          # can't reassign fields after creation
class Money:
    amount: int
    currency: str

m = Money(100, "USD")
# m.amount = 200      # -> raises FrozenInstanceError
m2 = replace(m, amount=200)      # make a NEW one with a change
Why care: immutable data can't be changed by some other function behind your back. Fewer bugs, and it's safe to share across threads (your concurrency work) without locks.

4. Higher-order functions + map/filter/reduce
Functions are values in Python — pass them around, return them.


def apply_twice(f, x):
    return f(f(x))

apply_twice(lambda n: n + 3, 10)   # 16
map / filter / reduce:


from functools import reduce

nums = [1, 2, 3, 4, 5]
list(map(lambda n: n*n, nums))              # [1,4,9,16,25]  -> transform each
list(filter(lambda n: n % 2 == 0, nums))    # [2,4]          -> keep some
reduce(lambda acc, n: acc + n, nums, 0)     # 15             -> fold to one value
⚠️ Pythonic note (important): In Python, idiomatic code prefers comprehensions/generator expressions over map/filter — they're more readable:


[n*n for n in nums]              # ✅ preferred over map
[n for n in nums if n % 2 == 0]  # ✅ preferred over filter
reduce has no comprehension equivalent, so it's the one that stays useful — but even then, prefer a built-in when one exists (sum, max, any, all). Use reduce only for genuine custom folds.

The functools toolkit worth knowing:


from functools import reduce, partial, lru_cache

@lru_cache            # only safe because the function is PURE — ties back to §1
def fib(n):
    return n if n < 2 else fib(n-1) + fib(n-2)

double = partial(lambda factor, x: factor * x, 2)   # pre-fill an argument
double(10)            # 20