# Answer
'''
1. Spot the impurity. Why is this impure, and rewrite it pure:

cart = []
def add_item(item):
    cart.append(item)
    return cart

this is impure because we are updating a global list in a function that's why this list cart become mutable

cart = []
def add_item(cart, item) :
    cart.append(item)
    return cart

2. Functional core / imperative shell. Given a function that reads a list of order dicts from a file, computes each order's total with tax, and prints them — split it into a pure compute_totals(orders, tax) and a thin impure wrapper.
def compute_totals(orders, tax) :
    for order in orders :
        print(f"Total: {order.get("value") + tax}")

3. Immutability. Write with_discount(order, pct) that returns a new frozen Order dataclass with the price reduced — without mutating the original.

def with_discount(order, pct) ;
    new_order["price"] = order["price"] * pct

    return new_order

4. Fold. Using reduce, write group_by_first_letter(words) that returns {'a': [...], 'b': [...]}. Then tell me whether reduce was actually the clearest tool here, or if a plain loop / defaultdict would be better (this judgment is the point).

I don't know how to do this
'''

'''
Q1 — diagnosis ✅, fix ❌ (still impure)
Your diagnosis is correct: the global cart is the problem. But your fix still mutates the list you were given:


def add_item(cart, item):
    cart.append(item)   # ⚠️ still a side effect — the caller's list is changed
    return cart
The caller's cart is now modified behind their back. Pure version returns a brand-new list:


def add_item(cart, item):
    return [*cart, item]      # or:  cart + [item]

a = [1, 2]
b = add_item(a, 3)
# a == [1, 2]   <- untouched ✅
# b == [1, 2, 3]
That's the whole game: new data out, inputs untouched.

Q2 — the print is still inside (so it's not pure)
The task was to make compute_totals pure and put I/O in a shell. Your version keeps print inside compute_totals (that's the side effect) and returns nothing:


def compute_totals(orders, tax):
    for order in orders:
        print(f"Total: {order.get('value') + tax}")   # ⚠️ I/O inside the core; returns None
Split it:


# PURE CORE — no I/O, returns new data, trivially testable
def compute_totals(orders, tax):
    return [order["value"] * (1 + tax) for order in orders]

# IMPURE SHELL — all the I/O lives here
def report_orders(path, tax):
    orders = read_orders(path)          # side effect: read file
    totals = compute_totals(orders, tax)  # pure call
    for t in totals:
        print(t)                         # side effect: output
Now you can test the logic with zero setup: assert compute_totals([{"value": 100}], 0.1) == [110.0]. That's why this matters for your testing gap.

(Side note: I used * (1 + tax) treating tax as a rate like 0.1 → 10%. Your + tax would add a flat amount. Either's fine as long as it's intentional.)

Q3 — three bugs + it must be a frozen dataclass
Issues: ; instead of :, new_order is never defined (NameError), you used a dict not a frozen dataclass, and * pct reduces in the wrong direction.

The clean way uses dataclasses.replace (makes a new frozen instance with one field changed):


from dataclasses import dataclass, replace

@dataclass(frozen=True)
class Order:
    price: float

def with_discount(order, pct):
    return replace(order, price=order.price * (1 - pct))   # 1 - pct = discount

o = Order(100)
d = with_discount(o, 0.2)
# o.price == 100   <- original untouched ✅
# d.price == 80.0
# o.price = 50     <- would raise FrozenInstanceError
replace() is the immutable-update idiom: "give me a copy, but with this changed."

Q4 — let me teach reduce properly (this is the valuable one)
reduce(fn, iterable, initial) folds a whole sequence into one value by repeatedly applying fn(accumulator, item). It carries an accumulator across the loop:


from functools import reduce

def group_by_first_letter(words):
    def fold(acc, word):
        letter = word[0]
        acc.setdefault(letter, []).append(word)   # add word to its bucket
        return acc                                 # pass the dict to the next step
    return reduce(fold, words, {})                  # start with empty dict {}

group_by_first_letter(["apple", "avocado", "banana"])
# {'a': ['apple', 'avocado'], 'b': ['banana']}
How it runs: start {} → fold({}, "apple") → {'a':['apple']} → fold(that, "avocado") → {'a':['apple','avocado']} → … one value at the end.

Now the judgment (the actual point of Q4): is reduce the clearest tool here? No. A plain loop with defaultdict is clearer:


from collections import defaultdict

def group_by_first_letter(words):
    groups = defaultdict(list)
    for word in words:
        groups[word[0]].append(word)
    return dict(groups)
reduce is the right tool when you're folding to a single scalar (a sum, a max, a running product) and no built-in exists. For building up a collection, a loop or defaultdict reads better — and Python's own docs/Guido recommend exactly that. Knowing when not to reach for a functional tool is real fluency, not a failure.
'''