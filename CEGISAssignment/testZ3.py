
from z3 import *
import sys


# construct the candidate expression x-1
x = Int('x')
candidate = x - 1
# the synthesized function has type Int -> Int
f = Function('f', IntSort(), IntSort())
# construct the invocation f(x) used in the specification
invocation = f(x)
# the specification f(x)>1
spec = invocation > 1

# we first substitute the invocation in the specification with the candidate expression
# = x-1>1
query = substitute(spec, (invocation, candidate))
# we negate the query for the seek of finding counterexamples
# = Not(x-1>1)
query = Not(query)

# check the query and print the result
# >: sat
s = Solver()
s.add(query)
print (s.check())
# get the model and print the counterexample
# >: 0
m = s.model()
print (m)

print (m[x])
