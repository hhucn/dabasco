import math
from pos import Position


class DoJ(object):
    DOJ_RECALL = 0
    DOJ_PRECISION = 1
#    DOJ_F1 = 2

    RELEVANCE_STANDARD = 0
    RELEVANCE_ADDED = 1

    REASON_RELATION_1 = 0
    REASON_RELATION_2 = 1
    REASON_RELATION_3 = 2
    REASON_RELATION_4 = 3

    # -----------------------------------------------------------
    # DEGREE OF JUSTIFICATION
    def doj(self, graph, pos, _doj, _coh):
        if _doj == DoJ.DOJ_RECALL:
            return self.recall(graph, pos, _coh)
        elif _doj == DoJ.DOJ_PRECISION:
            return self.precision(graph, pos, _coh)
#        elif _doj == DoJ.DOJ_F1:
#            return self.f1(graph,pos,_coh)
        return 0.0

    def doj_conditional(self, graph, pos, conditional_pos, _doj, _coh):
        if _doj == DoJ.DOJ_RECALL:
            return self.recall_conditional(graph, pos, conditional_pos, _coh)
        elif _doj == DoJ.DOJ_PRECISION:
            return self.precision_conditional(graph, pos, conditional_pos, _coh)
#        elif _doj == DoJ.DOJ_F1:
#            return self.f1_conditional(graph, pos, _coh)
        return 0.0

    # -----------------------------------------------------------
    # DEGREE OF JUSTIFICATION: implementations
    def recall(self, graph, pos, _coh):
        empty_pos = Position(pos.n)
        n1 = graph.getNumberOfCoherentCompletions(pos, _coh)
        n2 = graph.getNumberOfCoherentCompletions(empty_pos, _coh)
        return n1/float(n2)

    def recall_conditional(self, graph, pos, conditional_pos, _coh):
        pos_union = conditional_pos.unionWith(pos)
        if pos_union is None:
            return 0.0
        n1 = graph.getNumberOfCoherentCompletions(pos_union, _coh)
        if n1 == 0:
            return 0.0
        n2 = graph.getNumberOfCoherentCompletions(conditional_pos, _coh)
        return n1/float(n2)

    def precision(self, graph, pos, _coh):
        n1 = graph.getNumberOfCoherentCompletions(pos, _coh)
        n2 = pos.getNumberOfCompletions()
        return n1/float(n2)

    def precision_conditional(self, graph, pos, conditional_pos, _coh):
        pos_union = conditional_pos.unionWith(pos)
        if pos_union is None:
            return 0.0
        n1 = graph.getNumberOfCoherentCompletions(pos_union, _coh)
        if n1 == 0:
            return 0.0
        n2 = pos_union.getNumberOfCompletions()
        return n1/float(n2)

    # -----------------------------------------------------------
    # REASON RELATION:
    # Is q a reason to believe p?
    def reason(self, graph, p, q, _reason, _doj, _coh):
        if _reason == DoJ.REASON_RELATION_1:
            return self.reason1(graph, p, q, _doj, _coh)
        elif _reason == DoJ.REASON_RELATION_2:
            return self.reason2(graph, p, q, _doj, _coh)
        elif _reason == DoJ.REASON_RELATION_3:
            return self.reason3(graph, p, q, _doj, _coh)
        elif _reason == DoJ.REASON_RELATION_4:
            return self.reason4(graph, p, q, _doj, _coh)
        return 0.0

    # -----------------------------------------------------------
    # REASON RELATION: implementations

    # --------------------------
    # doj(p|q) - doj(p)
    def reason1(self, graph, p, q, _doj, _coh):
        """Calculate doj(p|q) - doj(p)."""
        pos = Position(graph.n)
        pos.setAcceptance(p, Position.ACCEPTED)
        cond_pos = Position(graph.n)
        cond_pos.setAcceptance(q, Position.ACCEPTED)
        doj1 = self.doj_conditional(graph, pos, cond_pos, _doj, _coh)
        doj2 = self.doj(graph, pos, _doj, _coh)
        return doj1 - doj2

    # --------------------------
    # doj(p|q) - doj(p|-q)
    def reason2(self, graph, p, q, _doj, _coh):
        """Calculate doj(p|q) - doj(p|-q)."""
        pos = Position(graph.n)
        pos.setAcceptance(p, Position.ACCEPTED)
        cond_pos1 = Position(graph.n)
        cond_pos1.setAcceptance(q, Position.ACCEPTED)
        cond_pos2 = Position(graph.n)
        cond_pos2.setAcceptance(q, Position.REJECTED)
        doj1 = self.doj_conditional(graph, pos, cond_pos1, _doj, _coh)
        doj2 = self.doj_conditional(graph, pos, cond_pos2, _doj, _coh)
        return doj1 - doj2

    # --------------------------
    # log_2( doj(p|q) / doj(p) )
    def reason3(self, graph, p, q, _doj, _coh):
        """Calculate log_2( doj(p|q) / doj(p) )."""
        pos = Position(graph.n)
        pos.setAcceptance(p, Position.ACCEPTED)
        cond_pos = Position(graph.n)
        cond_pos.setAcceptance(q, Position.ACCEPTED)
        doj1 = self.doj_conditional(graph, pos, cond_pos, _doj, _coh)
        doj2 = self.doj(graph, pos, _doj, _coh)
        if doj1 == 0:
            return -float("inf")  # log(0) = negative infinity
        if doj2 == 0:
            return 0.0  # log(inf) = 0
        quotient = doj1/float(doj2)
        return math.log(quotient, 2)

    # --------------------------
    # log_2( doj(p|q) / doj(p|-q) )
    def reason4(self, graph, p, q, _doj, _coh):
        """Calculate log_2( doj(p|q) / doj(p|-q) )."""
        pos = Position(graph.n)
        pos.setAcceptance(p, Position.ACCEPTED)
        cond_pos1 = Position(graph.n)
        cond_pos1.setAcceptance(q, Position.ACCEPTED)
        cond_pos2 = Position(graph.n)
        cond_pos2.setAcceptance(q, Position.REJECTED)
        doj1 = self.doj_conditional(graph, pos, cond_pos1, _doj, _coh)
        doj2 = self.doj_conditional(graph, pos, cond_pos2, _doj, _coh)
        if doj1 == 0:
            return -float("inf")  # log(0) = negative infinity
        if doj2 == 0:
            return 0.0  # log(inf) = 0
        quotient = doj1/float(doj2)
        return math.log(quotient, 2)
