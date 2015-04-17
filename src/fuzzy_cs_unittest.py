import unittest
import time

from fuzzy_cs_problem import FuzzyCSProblem
from fuzzy_cs_solution import FuzzyCSSolution


    
'''
    problem2 = get_heuristic_backtracking_problem
    solution2 = FuzzyCSSolution(problem2)

    partial_vars = ['f','t','s']
    partial_values = ['S','D','W']
    partial_joint_sat = solution.get_partial_joint_satisfaction(partial_vars, partial_values)
    print "Partial joint sat is", partial_joint_sat



    print "Variables are", problem.get_variables()
    print "Vars per constraint are", problem.get_num_vars_per_constraint()

    print "best solution is", best_solution



    appr_vars = ['f','t', 's']
    appr_vals = ['S','D', 'W']

    appr = solution.get_appropriateness(appr_vars, appr_vals)
    print "Appr value is", appr

    diff_var = 's'
    diff_fixed = {'f':'S', 't':'D'}
    difficulty_and_appr = solution.get_difficulty_and_appr(diff_var, diff_fixed)
    print "Difficulty is", difficulty_and_appr[0]
    print "Appr is", difficulty_and_appr[1]


    instant = ('S','D','L')
    joint_sat = solution.get_joint_satisfaction_degree(instant)
    print "joint_sat is", joint_sat

    fixed_vars = ['t']
    fixed_vals = ['D']
    instances = solution.get_all_possible_instantiations(fixed_vars, fixed_vals)
    print "Possible instances are", instances
'''




class SomeTest(unittest.TestCase):
    problem = None
    solution = None
    def setUp(self):
        if self.problem == None:
            self.setup_default_problem()
        self.startTime = time.time()

    def setup_default_problem(self):
        #define a default problem
        variables = ['f', 't', 's']

        domains = [('S', 'C'),('D', 'B', 'G'),('L', 'W')]

        constraints = [
                   {('S','D', None):1.0, 
                    ('S','B',None):0.4,
                    ('S','G',None):0.2,
                    ('C','G',None):0.8,
                    ('C','B',None):0.5},
                   {('S', None, 'L'):1.0,
                    ('S', None, 'W'):0.7,
                    ('C', None, 'W'):1.0,
                    ('C', None, 'L'):0.1},
                   {(None, 'D', 'W'):1.0,
                    (None, 'D', 'L'):0.7,
                    (None, 'B', 'W'):1.0,
                    (None, 'B', 'L'):0.4,
                    (None, 'G', 'L'):1.0,
                    (None, 'G', 'W'):0.6}
                    ]

        self.problem = FuzzyCSProblem(variables,domains, constraints)
        self.solution = FuzzyCSSolution(self.problem)

    def tearDown(self):
        t = time.time() - self.startTime
        print "%s: %.3f" % (self.id(), t)

    def testOne(self):
        time.sleep(1)
        self.assertEquals(int('42'), 42)

    def testTwo(self):
        time.sleep(2)
        self.assertEquals(str(42), '42')

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(SomeTest)
    unittest.TextTestRunner(verbosity=0).run(suite)