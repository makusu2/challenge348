import sys
import math
import itertools
import time
from collections import deque
from queue import PriorityQueue

def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        if 'log_time' in kw:
            name = kw.get('log_name', method.__name__.upper())
            kw['log_time'][name] = int((te - ts) * 1000)
        else:
            print('%r  %2.2f ms' % (method.__name__, (te - ts) * 1000))
        return result
    return timed
    
    
    
class Agent348:
    def __init__(self,maxNum):
        self.maxNum = maxNum
        self.nums = tuple(range(1,self.maxNum+1))
        self.col = PriorityQueue()
        self.possibleSquares = self.getSquares()
        self.allowableNextDict = self.getAllowableNextDict()
    
    def getAllowableNextDict(self):
        d = {i:tuple(j for j in range(1,self.maxNum+1) if j!=i and self.pairMeetsReqs(j,i)) for i in range(1,self.maxNum+1)}
        return d
    def getSquares(self):
        maxSum = 2*max(self.nums) - 1
        maxSquared = int(math.sqrt(maxSum))
        allowableSquares = tuple(n**2 for n in range(1,maxSquared+1))
        return allowableSquares
    def pairMeetsReqs(self,n1,n2):
        return n1+n2 in self.possibleSquares
    def allowableNextRepetition(self,perm):
        return (num for num in self.nums if num not in perm)
    def canBeNext(self,perm,nextVal):
        return self.pairMeetsReqs(perm[-1],nextVal)
    def allowableNextComplete(self,perm):
        return (num for num in self.allowableNextRepetition(perm) if self.canBeNext(perm,num))
    def asAppendedVal(self,perm,num):
        return list(perm)+[num]
    def removeVal(self):
        return self.col.get()[1]
    def addPerm(self,perm):
        perm = tuple(perm)
        allowableNexts = self.allowableNextFast(perm)
        priority = len(allowableNexts)
        if priority != 0:
            self.col.put((priority + (1/len(perm)),(perm,allowableNexts)))
            
    def allowableNextFast(self,perm):
        return tuple(n for n in self.allowableNextDict[perm[-1]] if n not in perm)
    @timeit
    def getSolution(self):
        nodesExpanded = 0
        for perm in itertools.permutations(self.nums,2):
            if self.pairMeetsReqs(*perm):
                self.addPerm(perm)
        #start time consumption
        while not self.col.empty():
            perm,allowableNexts = self.removeVal()
            nodesExpanded += 1
            #if len(perm) == 2:
                #print('got to perm ',perm)
            for nextVal in allowableNexts:
                permChild = self.asAppendedVal(perm,nextVal)
                if len(permChild) == len(self.nums):
                    print('nodes expanded: ',nodesExpanded)
                    return permChild
                else:
                    self.addPerm(permChild)
        print('nodes expanded: ',nodesExpanded)
        return None

def testMax(maxNum):
    print('With node priority:')
    agent = Agent348(maxNum)
    sol = agent.getSolution()
    if sol is None:
        print(maxNum,' has no solution')
    else:
        print(maxNum,' has a solution:\n',sol)
try:
    maxNum = int(sys.argv[1])
except IndexError:
    for i in range(20,100):
        print('\n\nTesting ',i)
        testMax(i)
else:
    testMax(maxNum)
    
