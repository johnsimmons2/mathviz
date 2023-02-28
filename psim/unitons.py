from operator import attrgetter
import math
import numpy as np
import matplotlib.pyplot as plt

AMOUNT = 5000

def getPrimes():
    global AMOUNT
    nums = [1]
    for num in range(AMOUNT):
        if num > 1:
            for i in range(2, num):
                if (num % i) == 0:
                    break
            else:
                nums.append(num)
    return nums

PRIMES = getPrimes()

CACHE = {}

class Uniton:
    # A uniton has a value, a uniton can have any value but only a prime is stable.

    # Two unitons whose values combine to a prime will bind and produce a new uniton of prime value.
    # Two unitons whose values approach a prime will be drawn near eachother.
    def __init__(self, x):
        global PRIMES
        global CACHE

        self.lcd = 0

        if x in CACHE.keys():
            copy = CACHE[x]
            self.charge = copy.charge
            self.negativePrimes = copy.negativePrimes
            self.positivePrimes = copy.positivePrimes
            self.accumulatedPrime = copy.accumulatedPrime
            self.value = int(x)
            self.prime = copy.prime
            self.primeDistance = copy.primeDistance
            self.children = copy.children
            self.mass = copy.mass
            self.parity = x % 2 == 0
        else:
            # Negative or Positive
            if x < 0:
                x = x * -1

            # 0 if Prime
            self.charge = 0
            self.negativePrimes = 0
            self.positivePrimes = 0
            self.accumulatedPrime = 0


            self.value = int(x)
            #self.prime = self.getPrimality()
            self.prime = self.value in PRIMES
            self.primeDistance = self.getPrimeDistance()
            self.children = self.getChildren()
            self.mass = self.getMass()
            self.parity = x % 2 == 0
            CACHE[x] = self
        self.heterogenous = self.getHeterogenity()
    
    def __str__(self):
        if self.value != 0:
            st = f'[ Value: {self.value}]'
            if self.prime:
                st = st + f'\t\tPRIME'
            else:
                st = st + f'\n\t[ Prime Distance: {self.primeDistance}]\n'
                st = st + f'\t[ Children ]:\n\t'
                for c in self.children:
                    st = st + f'{c.value}\t'
            st = st + f'\n\t[ Mass ]: {self.mass}\n'
            st = st + f'\t[ Charge ]: {self.charge}\n'
            st = st + f'\t[ AccP ]: {self.accumulatedPrime}\n'
            st = st + f'\t[ PP ]: {self.positivePrimes}\n'
            st = st + f'\t[ NP ]: {self.negativePrimes}\n'
            st = st + f'\t[ Hetero ]: {self.heterogenous}\n'
            return st
        else:
            return ''
    
    def __add__(self, other):
        if self._checkInstance(other):
            return Uniton(self.value + other.value)
        else:
            raise TypeError(f"Cannot add Uniton and {type(other).__name__}")
    
    def __radd__(self, other):
        if self._checkInstance(other):
            return Uniton(self.value + other.value)
        else:
            raise TypeError(f"Cannot add Uniton and {type(other).__name__}")
    
    def __sub__(self, other):
        if self._checkInstance(other):
            return Uniton(self.value - other.value)
        else:
            raise TypeError(f"Cannot add Uniton and {type(other).__name__}")
        
    def __mul__(self, other):
        if self._checkInstance(other):
            return Uniton(self.value * other.value)
        else:
            raise TypeError(f"Cannot add Uniton and {type(other).__name__}")
        
    def __div__(self, other):
        if self._checkInstance(other):
            return Uniton(self.value / other.value)
        else:
            raise TypeError(f"Cannot add Uniton and {type(other).__name__}")

    def _checkInstance(self, obj):
        return isinstance(obj, Uniton)

    def getHeterogenity(self):
        for c in self.children:
            for k in self.children:
                if c != k:
                    if c.value == k.value:
                        return False
        return True

    def getPrimality(self):
        val = self.value

        if val == 0 or val == 1:
            return True
        elif val > 1:
            for i in range(2, val):
                if (val % i) == 0:
                    return False
            else:
                return True
        else:
            return True

    # Prime distance is the distance to the closest prime number.
    #   Also stores the charge (how close in either direction)
    #   Calculates accumulated charge in both directions
    #   Calculates accumulated primal charge
    def getPrimeDistance(self):
        global PRIMES
        val = self.value

        positive = 0
        negative = 0
        distance = 9999999

        if val > 1:
            for i in range(1, val+1):
                x = val - i
                y = val + i
                if x in PRIMES and y in PRIMES:
                    self.negativePrimes = self.negativePrimes + 1
                    self.positivePrimes = self.positivePrimes + 1
                    if positive == 0:
                        positive = y
                    if negative == 0:
                        negative = x
                    if i < distance:
                        distance = i
                elif x in PRIMES:
                    self.negativePrimes = self.negativePrimes + 1
                    if i < distance:
                        distance = i
                    if negative == 0:
                        negative = x
                elif y in PRIMES:
                    self.positivePrimes = self.positivePrimes + 1
                    if i < distance:
                        distance = i
                    if positive == 0:
                        positive = y
            if PRIMES[-1] < val * 2:
                self.charge = None
            else:
                self.charge = negative/positive - 0.5
        else:
            self.charge = val
        if distance == 9999999 or self.prime:
            distance = 0
        self.accumulatedPrime = positive - negative
        return distance
        

    def getChildren(self):
        tmp = self.value
        children = []

        if self.value == 0:
            self.lcd = 0
            return children

        if self.prime:
            self.lcd = 1
            return children

        for i in range(2, int(math.sqrt(tmp))+1):
            while tmp % i == 0:
                children.append(Uniton(i))
                tmp = tmp/i
        if tmp > 2:
            children.append(Uniton(tmp))
        self.lcd = min(children, key=attrgetter('value')).value
        return children

    def getMass(self):
        mass = 0
        if len(self.children) == 0:
            return (self.value + 1) / 2
        for c in self.children:
            mass = mass + c.value
        return (mass + 1 + self.value)/len(self.children)



    # global PRIMES
    # global UNITONS
    # o1 = []
    # o2 = []
    # o3 = []

    # TODO: Save to CSV  

    # for i in range(20):
    #    o1.append(Uniton(PRIMES[i]))
    
    # curCount = 20
    # curIndx = 0
    # while curCount > 0 and curIndx < len(UNITONS):
    #     if UNITONS[curIndx].heterogenous and len(UNITONS[curIndx].children) == 2:
    #         o2.append(UNITONS[curIndx])
    #         curCount = curCount - 1
    #     curIndx = curIndx + 1

    # curCount = 20
    # curIndx = 0
    # while curCount > 0 and curIndx < len(UNITONS):
    #     if UNITONS[curIndx].heterogenous and len(UNITONS[curIndx].children) == 3:
    #         o3.append(UNITONS[curIndx])
    #         curCount = curCount - 1
    #     curIndx = curIndx + 1

    

    # # # Order 1: All integers unique of order 1 from smallest to largest, where
    # #          the order of uniqueness is the amount of non-1 multiplicative factors.
    # #          This would be all prime numbers. That is to say, all numbers that have
    # #          only 1 way of writing it as a multiple of 2 minimized factors.
    # #               8 = 4 x 2, but 4 is not minimal:
    # #               4 = 2 x 2, since 2 x 2 or 2^2 contains duplicate terms. So, 4 has 2 possible ways of being written.
    # #           Is the 1st generation of children of a number a subset of the original generation? If so, not unique.
    # order1 = []
    # counter = 10
    # index = 0
    # while counter > 0 and index < len(unitons):
    #     if unitons[index].prime:
    #         order1.append(unitons[index])
    #         counter = counter - 1
    #     index = index + 1


    # for c in order1:
    #     print(c)


    # print('ORDER 2 V')

    # # Order 2: All integers of unique order 2 from smallest to largest, where each element may have up to 2 factors.
    # order2 = []
    # order2_cache = []
    # for i in range(4):
    #     for p in PRIMES:
    #         for q in PRIMES:
    #             if p != q:
    #                 val = p * q
    #                 if val not in order2_cache:
    #                     order2.append(Uniton(val))
    #                     order2_cache.append(val)
    # order2 = sorted(order2, key=lambda x: x)


    # for c in order2[:10]:
    #     print(c)

    # order3 = []
    # order3_cache = []
    # for i in range(10):
    #     for p in PRIMES:
    #         for q in PRIMES:
    #             for r in PRIMES:
    #                 if p != q and r != p and r != q:
    #                     val = p * q * r
    #                     if val not in order3_cache:
    #                         order3.append(Uniton(val))
    #                         order3_cache.append(val)
    # order3 = sorted(order3, key=lambda x: x)


    # for c in order3[:10]:
    #     print(c)