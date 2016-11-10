import sys

class Position(object):
    """Map elements in a set [1,..n] to {REJECTED, UNDECIDED, ACCEPTED}."""
    
    REJECTED = -1
    UNDECIDED = 0
    ACCEPTED = 1
    
    def __init__(self,n):
        self.n = n
        self.nUndecided = n # Cache the number of undecided elements to improve performance.
        self.A = [Position.UNDECIDED for x in range(n+1)]

    def setAcceptance(self,i,a):
        change = abs(self.A[i]) - abs(a)
        self.nUndecided += change
        self.A[i] = a
    
    def setAccepted(self,i):
        change = abs(self.A[i]) - 1
        self.nUndecided += change
        self.A[i] = Position.ACCEPTED
    
    def setRejected(self,i):
        change = abs(self.A[i]) - 1
        self.nUndecided += change
        self.A[i] = Position.REJECTED
    
    def setUndecided(self,i):
        change = abs(self.A[i])
        self.nUndecided += change
        self.A[i] = Position.UNDECIDED
    
    def isAccepted(self,i):
        if i<0:
            return (self.A[-i] == Position.REJECTED)
        return (self.A[i] == Position.ACCEPTED)
    
    def isRejected(self,i):
        if i<0:
            return (self.A[-i] == Position.ACCEPTED)
        return (self.A[i] == Position.REJECTED)
    
    def isUndecided(self,i):
        return (self.A[abs(i)] == Position.UNDECIDED)
    
    def getAcceptance(self,i):
        return self.A[abs(i)];
        
    def acceptedElements(self):
        S = set()
        for element in range(1,self.n+1):
            if (self.A[element] == Position.ACCEPTED):
                S.add(element)
        return S
    
    def getFreeElements(self):
        freeElements = set()
        for element in range(1,self.n+1):
            myChoice = self.A[element]
            if myChoice == Position.UNDECIDED:
                freeElements.add(element)
        return freeElements
    
    def isComplete(self):
        return (self.nUndecided == 0)
    
    def unionWith(self,otherPos):
        """Create a new position from self and otherPos.
        
        Creates a new position of same size as self. For each
        undecided element in self, use the acceptance value from
        otherPos, else use acceptance from self.
        Return None if the two positions are conflicting."""
        
        newPos = Position(self.n)
        for element in range(1,self.n+1):
            myChoice = self.A[element]
            theirChoice = otherPos.A[element]
            if myChoice == Position.UNDECIDED:
                newPos.setAcceptance(element,theirChoice)
            elif theirChoice == Position.UNDECIDED:
                newPos.setAcceptance(element,myChoice)
            elif myChoice != theirChoice:
                return None
            else:
                newPos.setAcceptance(element,theirChoice)
        return newPos
    
    def getNumberOfCompletions(self):
        return 2**self.nUndecided
    
    def prettyPrint(self,prefix,suffix):
        if prefix:
            sys.stdout.write(prefix)
        sys.stdout.write('[')
        for arg in range(1,self.n+1):
            if self.A[arg] == Position.ACCEPTED:
                sys.stdout.write('+')
            elif self.A[arg] == Position.REJECTED:
                sys.stdout.write('-')
            else:
                sys.stdout.write('?')
        sys.stdout.write(']')
        if suffix:
            sys.stdout.write(suffix)
        sys.stdout.write('\n')
        
    