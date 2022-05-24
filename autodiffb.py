# -*- coding: utf-8 -*-
"""autodiffB.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1-SdCKtJZ_RIJ1XBP6E5yAjYCIP6a3oSY

# Evaluating derivatives

Derivatives are frequently used in optimization, machine learning and statistical inference. For example, we can find function minima and maxima much faster if derivatives are available. But how can we compute derivatives?

## Symbolic differentiation

We can write (or use) a library which differentiates expressions symbolically.
"""

import sympy as sym

"""$$\frac {d \log(x) \exp(x)} {d x} = \log(x) \exp'(x) + \log'(x) \exp(x) = \log(x) \exp(x) + \frac {\exp(x)} x$$"""

x = sym.Symbol('x')
print(sym.diff(sym.log(x)*sym.exp(x), x))

"""$$\left(\frac { \log(x) + \exp(x)} {\log(x)  \exp(x)} \right)'$$"""

print(sym.diff((sym.log(x) + sym.exp(x))/(sym.log(x)*sym.exp(x)), x))

"""However, the size of the derivative can grow very fast (expression swell):

$$\left( x \cdot\frac { \log(x) + \exp(x)} {\log(x)  \exp(x)} \right)'$$
"""

print(sym.diff(x*(sym.log(x) + sym.exp(x))/(sym.log(x)*sym.exp(x)), x))

"""$$\left[\left( x \cdot\frac { \log(x) + \exp(x)} {\log(x)  \exp(x)} \right)^x \right]'$$"""

print(sym.diff((x*(sym.log(x) + sym.exp(x))/(sym.log(x)*sym.exp(x)))**x, x))

"""$$\frac{\partial \left( \frac { \log(x) + \exp(y)} {\log(x)  \exp(y)} \right)}{\partial y}$$"""

y = sym.Symbol('y')
print(sym.diff((sym.log(x) + sym.exp(y))/(sym.log(x)*sym.exp(y)), y))

"""## Automatic differentiation

Automatic differentiation is a programming technique which can compute the derivative of any function, including functions with conditionals, loops, and recursion.
"""

import jax   #  a Python library from Google for automatic differentiation
from random import random
import jax.numpy as np
import matplotlib.pyplot as plt

"""Let's algorithmically differentiate the same function."""

def foo(x):
  a = np.log(x)
  b = np.exp(x)
  return (a + b)/(a*b)

dfoo = jax.grad(foo)

x = np.linspace(1.1, 2.9, 1000)
plt.plot(x, [foo(x) for x in x], label="foo")
plt.plot(x, [dfoo(x) for x in x], label="d foo/d x")
plt.legend()

"""## Gradient based optimization

### Gradient descent

$$x \gets x - f'(x) \delta$$
$$\delta \gets \gamma\delta$$
"""

def gd(f, x0, step=0.1, decay=0.995, niter=100):
  """approximates minimum of f starting from x0
  """
  df = jax.grad(f)
  x = x0
  for i in range(niter):
    x -= df(x)*step
    step *= decay
  return x

"""$$foo(x) = \sin(x)\exp(-(x-1)^2)$$"""

def foo(x):
  a = np.exp(-(x-1)**2)
  b = np.sin(x)
  return a*b

dfoo = jax.grad(foo)

x = np.linspace(-4, 4, 100)
plt.plot(x, [foo(x) for x in x], label="foo")
plt.plot(x, [dfoo(x) for x in x], label="d foo/d x")
plt.axhline(0, lw=0.5, ls='dashed', color='black')

x = gd(foo, 0.1*(random()-0.5), niter=200)
print(f"x={x:.3f} foo({x:.3f})={foo(x):.3f}")

"""### Newton's method

$$x \leftarrow x - \frac {f'(x)} {f''(x)}$$
"""

def newton(f, x0, niter=10):
  df = jax.grad(f)
  ddf = jax.grad(df)
  x = x0
  for i in range(niter):
    x = x - df(x)/ddf(x)
  return x

x = newton(foo, 0.1*(random()-0.5), niter=10)
print(f"x={x:.8f} foo({x:.3f})={foo(x):.3f}")

ddfoo = jax.grad(dfoo)

x = np.linspace(-4, 4, 100)
_ = plt.plot(x, [(foo(x), dfoo(x), ddfoo(x)) for x in x])

"""## Application to machine learning

### Linear regression
"""

municipalities = np.array([(441976, 2359), (309912, 1311), (35821, 14), (1064523, 31664), (50022, 99), (94194, 219), (1118363, 104246), (766247, 2009), (59246, 147), (96671, 271), (293166, 5864), (24842, 63), (275797, 3920), (255611, 670), (41512, 133), (75471, 235), (34456, 13), (98014, 312), (279091, 1299), (211264, 197), (79595, 410), (168959, 60), (169312, 791), (216749, 293), (106626, 172), (150191, 334), (49265, 189), (884039, 1675), (140857, 179), (73957, 226), (244515, 256), (73131, 36), (12603, 7), (48506, 448), (50863, 551), (136575, 1167), (136690, 194), (139017, 24), (246157, 4046), (41822, 117), (31105, 65), (402087, 1614), (740243, 501), (207791, 151), (18121, 218), (171057, 580), (359594, 6872), (152634, 514), (30140, 69), (76103, 2421), (135252, 510), (367552, 4688), (58093, 163), (134205, 337), (12236, 6), (75847, 230), (148942, 1450), (98733, 960), (106797, 272), (813137, 4436), (235134, 3393), (14560, 23), (315429, 1446), (289005, 1413), (576211, 6947), (340761, 697), (287344, 827), (146912, 356), (38384, 89), (112529, 911), (35154, 41), (52997, 167), (613572, 2031), (401093, 1082), (166448, 87), (44096, 104), (39067, 79), (100361, 294), (394099, 872), (52341, 142), (298666, 378), (90943, 524), (8125, 14), (34134, 292), (29867, 13), (43846, 562), (1254812, 17713), (33761, 92), (169031, 612), (990827, 15279), (229676, 1517), (38409, 777), (199770, 666), (142900, 851), (155468, 239), (438265, 1960), (37765, 57), (66980, 63), (70981, 162), (504659, 1570)])

populations = municipalities[:, 0]
cases = municipalities[:, 1]
plt.scatter(populations, cases)
plt.xscale("log")
plt.xlabel("population")
plt.yscale("log")
plt.ylabel("number of cases")

"""$$\log(\texttt{cases}) = a_0\cdot \log(\texttt{population}) +a_1$$"""

def loss(a):
  """computes square loss of linear regression.
  """
  # we could write a loop here, but that would be too slow for optimization
  err = np.log(cases) - a[0]*np.log(populations) - a[1]
  # sumerr = 0
  # for i in range(len(cases)):
  #    err = np.log(cases[i]) - a[0]*np.log(populations[i]) - a[1]
  #    summerr += err*err
  return np.mean(err*err)

a = gd(loss, np.array([1., np.log(np.sum(cases)/np.sum(populations))]), step=0.01, decay=0.99, niter=200)
print(f"log(c)={a[0]:.3f}*log(p){a[1]:+.3f}")

plt.scatter(np.log(populations), np.log(cases))
x = np.linspace(min(np.log(populations)), max(np.log(populations)), 100)
plt.plot(x, a[0]*x + a[1],  color="green")
plt.xlabel("log(populations)")
plt.ylabel("log(cases)")

