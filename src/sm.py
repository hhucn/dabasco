from random import randrange
import itertools
import copy
import collections
from pos import Position

Inference = collections.namedtuple('Inference', ['id','origin','target'])

# statement map
class SM(object):
    """A statement map data structure.
    
    Consists of:
    n -- Number of statements (set of statements is [1,..,n] implicitly)
    inferences -- Set of arguments
    undercuts -- Set of undercuts
    """
    
    COHERENCE_DEDUCTIVE_INFERENCES = 0
    
    # -----------------------------------------------------------
    # CONSTRUCTION
    def __init__(self):
        self.n = 0
        self.inferences = {}
        self.undercuts = {}
    
    def addInference(self, origin, target, rid):
        '''Add an inference rule with a statement target.'''
        
        # Update statements.
        self.n = max(self.n,abs(target))
        for p in origin:
            self.n = max(self.n,abs(p))
        
        # check (or generate) inference id.
        if rid is None or (rid in self.inferences):
            i = 1
            while (i in self.inferences):
                i += 1
            rid = i
        
        # Add rule.
        self.inferences[rid] = Inference(rid, origin, target)
        return rid
    
    def addUndercut(self, origin, target, rid):
        '''Add an inference rule with a rule target.'''
        
        # Update statements.
        for p in origin:
            self.n = max(self.n,abs(p))
        
        # check (or generate) inference id.
        if rid is None or (rid in self.undercuts):
            i = 1
            while (i in self.undercuts):
                i += 1
            rid = i
            
        # Add rule.
        self.undercuts[rid] = Inference(rid, origin, target)
        return rid
    
    # -----------------------------------------------------------
    # I/O
    def prettyPrint(self):
        if self.n < 5:
            print('Statements: ',range(1,self.n+1))
        else:
            print('Statements: [ 1, ...,',self.n,']')
        for rid in self.inferences:
            self.printInference(rid)
        for rid in self.undercuts:
            self.printUndercut(rid)
    
    def printInference(self, rid):
        rule = self.inferences[rid]
        print(rule.id,': (',rule.origin,',',rule.target,')')
        
    def printUndercut(self, rid):
        rule = self.undercuts[rid]
        print(rule.id,': (',rule.origin,', rule',rule.target,')')
        
    # -----------------------------------------------------------
    # EVALUATION
    def inferenceIsViolated(self,pos,r):
        for p in r.origin:
            if not pos.isAccepted(p):
                return False
        return pos.isRejected(r.target)
    
    def getActiveInferences(self,pos):
        """Return all active and non-undercut inferences.
        
        An inference is active if it has a satisfied premise.
        An inference is undercut if there is an undercut with 
        satisfied premise against it.
        """
        
        # Fetch inferences with satisfied premises.
        active_inferences = []
        for rid in self.inferences:
            r = self.inferences[rid]
            active = True
            for p in r.origin:
                if not pos.isAccepted(p):
                    active = False
                    break
            if active:
                active_inferences.append(r)
        
        # Fetch undercuts with satisfied premises.
        active_undercuts = []
        for rid in self.undercuts:
            r = self.undercuts[rid]
            active = True
            for p in r.origin:
                if not pos.isAccepted(p):
                    active = False
                    break
            if active:
                active_undercuts.append(r)
        
        # Remove rules that are undercut by active undercuts.
        definite_undercuts = []
        changed = True
        while changed:
            changed = False
            
            # Find unattacked undercutting rules and remember them as definitely active.
            for r in active_undercuts:
                if r not in definite_undercuts:
                    is_undercut = False
                    for r2 in active_undercuts:
                        if r.id == abs(r2.target):
                            is_undercut = True
                            break
                    if not is_undercut:
                        definite_undercuts.append(r)
            
            # Remove all rules from active_undercuts that are undercut by some rule in definite_undercuts.
            for r in definite_undercuts:
                target_id = abs(r.target)
                nOld = len(active_undercuts)
                active_undercuts[:] = [r2 for r2 in active_undercuts if r2.id != target_id]
                active_inferences[:] = [r2 for r2 in active_inferences if r2.id != target_id]
                nNew = len(active_undercuts)
                if nNew < nOld:
                    changed = True
        
        return active_inferences
    
    def getViolatedRules(self,pos):
        """Return a list of Inference tuples, which are the rules in self that are violated by the given position."""
        ar = self.getActiveInferences(pos)
        vr = []
        for r in ar:
            if self.inferenceIsViolated(pos,r):
                vr.append(r)
        return vr
    
    def isDeductivelyValid(self, pos):
        return (len(self.getViolatedRules(pos)) == 0)
    
    # -----------------------------------------------------------
    # COHERENCE
    def getNumberOfCoherentCompletions(self,pos,coherence):
        if (coherence == SM.COHERENCE_DEDUCTIVE_INFERENCES):
            return self.getNumberOfDeductivelyValidCompletions(pos)
        return 0;
        
    def getNumberOfDeductivelyValidCompletions(self,pos):
        possibleStatements = list(pos.getFreeElements())
        pos2 = copy.deepcopy(pos)
        return self.getNumberOfDeductivelyValidCompletionsREC(pos2,possibleStatements,len(possibleStatements))
        
    def getNumberOfDeductivelyValidCompletionsREC(self,pos,possibleStatements,k):
        if k==0:
            if self.isDeductivelyValid(pos):
                return 1;
            else:
                return 0;
        k-=1
        possibleStatement = possibleStatements[k]
        pos.setAccepted(possibleStatement)
        n1 = self.getNumberOfDeductivelyValidCompletionsREC(pos,possibleStatements,k)
        pos.setRejected(possibleStatement)
        n2 = self.getNumberOfDeductivelyValidCompletionsREC(pos,possibleStatements,k)
        pos.setUndecided(possibleStatement)
        return n1+n2
    
    


