from verbal_expressions import *
from string import printable
from inspect import getargspec
import unittest
import random
def rand():
  return str([random.choice(choosefrom) for i in random.randint(1,900)])
class TestRandom(unittest.TestCase):
  def setupUp(self):
    choosefrom = list(printable)
    self.totest = rand()
  def breakrandom(self,value):
    l = []
    while True:
      try:
        l.extend(value[:random.randint(1,5)])
      except:
        break
    return l
  def test_add(self):
    "Very Simple Test To Add Values and to see if they work"
    v = VerEx()
    for i in breakrandom(self.totest):
      v.add(self,value)
    self.assertEqual(str(v),value)
  def test_broken(self):
    "Test Whether It raises an Exception on cases"
    v = VerEx()
    v.add(self.totest)
    for i in dir(b):
      if len(getargspec(i)[0]) == 2: #check whether It has two args
        continue
      if type(i) == type(lambda x:x):
        self.assertRaises(TypeError,lambda:eval "v."+meth+"()",())
        self.assertRaises(TypeError,lambda:eval "v."+meth+"()",[])
        self.assertRaises(TypeError,lambda:eval "v."+meth+"()",6)
        self.assertRaises(TypeError,lambda:eval "v."+meth+"()","f")
