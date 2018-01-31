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
class NoSolutionsException(BaseException):
    pass


@timeit
def getSolution(maxNum):
    def pairMeetsReqs(n1,n2):
        def isWholeNum(n):
            return n == int(n)
        return isWholeNum(math.sqrt(n1+n2))
        
    def allowableNextRepetition(permList,nums):
        return (num for num in nums if num not in permList)
    def getSquareList(maxNum):
        maxSquare = int(math.sqrt(maxNum*2 - 1))
        squares = tuple(n**2 for n in range(1,maxSquare+1))
        return squares
        
    def canBeNext(permList,nextVal):
        return pairMeetsReqs(permList[-1],nextVal)
    def allowableNextComplete(permList,nums):
        return (num for num in allowableNextRepetition(permList,nums) if canBeNext(permList,num))
    def asAppendedVal(permList,num):
        return list(permList)+[num]
    def removeVal(collection):
        return collection.get()[1]
    def addPerm(collection,newPerm,nums):
        newPerm = list(newPerm)
        allowableNexts = tuple(allowableNextComplete(newPerm,nums))
        #print(len(allowableNexts))
        priority = len(allowableNexts)
        if priority != 0:
            #print(priority)
            collection.put((len(allowableNexts),(newPerm,allowableNexts)))
        
    #currentPerms contains a tuple of: (actual perm, list possibleNexts)
    squares = getSquareList(maxNum)
    nums = tuple(range(1,maxNum+1))
    currentPerms = PriorityQueue()
    for perm in itertools.permutations(nums,2):
        if pairMeetsReqs(*perm):
            addPerm(currentPerms,perm,nums)
    
    while not currentPerms.empty():
        perm,allowableNexts = removeVal(currentPerms)
        for nextVal in allowableNexts:
            permChild = asAppendedVal(perm,nextVal)
            if len(permChild) == len(nums):
                return permChild
            else:
                addPerm(currentPerms,permChild,nums)
    return None

def testMax(maxNum):
    sol = getSolution(maxNum)
    if sol is None:
        print(maxNum,' has no solution')
    else:
        print(maxNum,' has a solution:\n',sol)
try:
    maxNum = int(sys.argv[1])
except IndexError:
    for i in range(3,50):
        testMax(i)
else:
    testMax(maxNum)
    
