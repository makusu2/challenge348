import sys
import math
import itertools
import time

def pairMeetsReqs(n1,n2):
    def isWholeNum(n):
        return n == int(n)
    return isWholeNum(math.sqrt(n1+n2))
def meetsReqs(vals):
    vals = iter(vals)
    prevVal = next(vals)
    for val in vals:
        if not pairMeetsReqs(prevVal,val):
            return False
        prevVal = val
    return True
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
@timeit
def getSolution(maxNum,genmaker):
    nums = range(1,maxNum+1)
    try:
        for testVals in genMaker(nums):
            if meetsReqs(testVals):
                return testVals
    except NoSolutionsException:
        return None
class NoSolutionsException(BaseException):
    pass
class Stack:
     def __init__(self):
         self.items = []

     def isEmpty(self):
         return self.items == []

     def push(self, item):
         self.items.append(item)

     def pop(self):
         return self.items.pop()

     def peek(self):
         return self.items[len(self.items)-1]

     def size(self):
         return len(self.items)
         
class Queue:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def enqueue(self, item):
        self.items.insert(0,item)

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)

def genMaker(nums):
    def allowableNextRepetition(permList,nums):
        return (num for num in nums if num not in permList)
    def canBeNext(permList,nextVal):
        return pairMeetsReqs(permList[-1],nextVal)
    def allowableNextComplete(permList,nums):
        return (num for num in allowableNextRepetition(permList,nums) if canBeNext(permList,num))
    def asAppendedVal(permList,num):
        return permList+[num]
    container = Queue()
    nums = list(nums)
    startPerms = (list(perm) for perm in itertools.permutations(nums,2) if meetsReqs(perm))
    currentPerms = startPerms
    curLen = 2
    if not currentPerms:
        raise NoSolutionsException
    while(curLen < len(nums)):
        currentPerms = (asAppendedVal(perm,nextVal) for perm in currentPerms for nextVal in allowableNextComplete(perm,nums))
        curLen+=1
    return currentPerms
def testMax(maxNum):
    sol = getSolution(maxNum,genMaker)
    if sol is None:
        print(maxNum,' has no solution')
    else:
        print(maxNum,' has a solution:\n',sol)
try:
    maxNum = int(sys.argv[1])
except IndexError:
    for i in range(2,50):
        testMax(i)
else:
    testMax(maxNum)
    
