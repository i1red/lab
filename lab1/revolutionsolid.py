from math import pi
from scipy.integrate import quad
from scipy.misc import derivative
import inspect
import time

class RevolutionSolid:
    def __init__(self, f, a, b):
        self.__f = f
        self.__a = float(a)
        self.__b = float(b)

    @property
    def a(self):
        return self.__a

    @property
    def b(self):
        return self.__b

    @property
    def f(self):
        return self.__f

    def volume(self):
        integral = quad(lambda x: self.f(x) ** 2, self.a, self.b)[0]
        return pi * integral

    def square(self):
        deriv = lambda x: derivative(self.f, x)
        integral = quad(lambda x: self.f(x) * (1 + deriv(x) ** 2) ** 0.5, self.a, self.b)[0]
        return 2 * pi * integral



cilindor = RevolutionSolid(lambda x: 1, 2, 8)

def a(x):
    return x ** 2


print(time.asctime())

print(cilindor.volume(), cilindor.square())
