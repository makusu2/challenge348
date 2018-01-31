import sys
import math
import itertools
import time
from collections import deque

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
class NoSolutionsException(BaseException):
    pass


@timeit
def getSolution(maxNum,searchType='bfs'):
    def allowableNextRepetition(permList,nums):
        return (num for num in nums if num not in permList)
    def canBeNext(permList,nextVal):
        return pairMeetsReqs(permList[-1],nextVal)
    def allowableNextComplete(permList,nums):
        return (num for num in allowableNextRepetition(permList,nums) if canBeNext(permList,num))
    def asAppendedVal(permList,num):
        return permList+[num]
    def removeVal(collection,bfs):
        return collection.popleft() if bfs else collection.pop()
        
    assert(searchType in ['bfs','dfs'])
    bfs = searchType == 'bfs'
    nums = tuple(range(1,maxNum+1))
    currentPerms = deque([list(perm) for perm in itertools.permutations(nums,2) if meetsReqs(perm)])
    
    while(currentPerms):
        perm = removeVal(currentPerms,bfs)
        for nextVal in allowableNextComplete(perm,nums):
            addVal = asAppendedVal(perm,nextVal)
            if len(addVal) == len(nums):
                return addVal
            else:
                currentPerms.append(addVal)
    return None

def testMax(maxNum):
    sol = getSolution(maxNum,searchType='dfs')
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
    
