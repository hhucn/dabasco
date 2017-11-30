import unittest
from dabasco.doj.pos import Position
from dabasco.doj.sm import SM
from dabasco.doj.doj import DoJ


class TestStatementMapDoJ(unittest.TestCase):
    def generate(self, sm, dojs):
        doj = DoJ()
        n = sm.n
        for i in range(n):
            s = i + 1
            pos = Position(n)
            pos.set_accepted(s)
            doj_s = doj.doj(sm, pos, DoJ.DOJ_RECALL, SM.COHERENCE_DEDUCTIVE_INFERENCES)
            print(doj_s)
            self.assertEqual(doj_s, dojs[i])

    # -----------------------------------------------------
    def test_1statement_test1(self):
        sm = SM()
        sm.n = 1
        dojs = [0.5]
        self.generate(sm, dojs)

    # -----------------------------------------------------
    def test_2statements_test1(self):
        sm = SM()
        sm.n = 2
        dojs = [1.0/2.0, 1.0/2.0]
        self.generate(sm, dojs)

    def test_2statements_test2(self):
        sm = SM()
        sm.add_inference([1], 2, None)
        dojs = [1.0/3.0, 2.0/3.0]
        self.generate(sm, dojs)

    def test_2statements_test3(self):
        sm = SM()
        sm.add_inference([1], -2, None)
        dojs = [1.0/3.0, 1.0/3.0]
        self.generate(sm, dojs)

    def test_2statements_test4(self):
        sm = SM()
        sm.add_inference([-1], 2, None)
        dojs = [2.0/3.0, 2.0/3.0]
        self.generate(sm, dojs)

    def test_2statements_test5(self):
        sm = SM()
        sm.add_inference([-1], -2, None)
        dojs = [2.0/3.0, 1.0/3.0]
        self.generate(sm, dojs)

    # -----------------------------------------------------
    def test_3statements_test1(self):
        sm = SM()
        sm.add_inference([2], 1, None)
        sm.add_inference([3], 2, None)
        dojs = [3.0/4.0, 2.0/4.0, 1.0/4.0]
        self.generate(sm, dojs)

    # -----------------------------------------------------
    def test_4statements_test1(self):
        sm = SM()
        sm.add_inference([2], 1, None)
        sm.add_inference([3], 2, None)
        sm.add_inference([4], 3, None)
        dojs = [4.0/5.0, 3.0/5.0, 2.0/5.0, 1.0/5.0]
        self.generate(sm, dojs)


if __name__ == '__main__':
    unittest.main()
