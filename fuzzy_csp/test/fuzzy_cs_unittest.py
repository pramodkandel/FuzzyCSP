import unittest
import time

from fuzzy_csp.src.fuzzy_cs_problem import FuzzyCSProblem
from fuzzy_csp.src.fuzzy_cs_solution import FuzzyCSSolution

from fuzzy_csp.src.fuzzy_example_problem import FuzzyExampleProblem


class FuzzyCSUnitTest(unittest.TestCase):
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



    def testExampleProblemGeneration(self):
        example_problem = FuzzyExampleProblem()
        generated_problem = example_problem.generate_example_problem()
        self.assertEquals(example_problem.num_variables, len(generated_problem.get_variables()))
        self.assertEquals(example_problem.num_vars_per_constraint, generated_problem.num_vars_per_constraint)



    def testPartialJointSatisfaction(self):
        partial_vars = ['f']
        partial_values = ['S']
        partial_joint_sat = self.solution.get_partial_joint_satisfaction(partial_vars, partial_values)
        self.assertEquals(partial_joint_sat, 1.0)



    def testAppropriateness(self):
        appr_vars = ['f','t']
        appr_vals = ['S','D']

        appr = self.solution.get_appropriateness(appr_vars, appr_vals)
        self.assertEquals(appr,1.0)

    def testDifficulty(self):
        diff_var = 's'
        diff_fixed = {'f':'S', 't':'D'}
        difficulty_and_appr = self.solution.get_difficulty_and_appr(diff_var, diff_fixed, [])
        difficulty = difficulty_and_appr[0]
        appr = difficulty_and_appr[1]
        self.assertEquals(difficulty, 1.4)
        self.assertEquals(appr['L'], 0.7)
        self.assertEquals(appr['W'], 0.7)


    def testJointSatisfaction(self):
        instant = ('C','D','L')
        joint_sat = self.solution.get_joint_satisfaction_degree(instant)
        self.assertEquals(joint_sat, 0.0)
        

    def testGetPossibleInstances(self):
        fixed_vars = ['t']
        fixed_vals = ['D']
        expected_instances = [('S', 'D', 'L'), ('S', 'D', 'W'), ('C', 'D', 'L'), ('C', 'D', 'W')]
        length = 0
        for instance in self.solution.get_all_possible_instantiations(fixed_vars, fixed_vals):
            self.assertTrue(instance in expected_instances)
            length += 1

        self.assertEquals(length ,len(expected_instances))        

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(FuzzyCSUnitTest)
    unittest.TextTestRunner(verbosity=0).run(suite)