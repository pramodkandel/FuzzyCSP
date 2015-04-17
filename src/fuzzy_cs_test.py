import unittest
import time
import inspect

from fuzzy_cs_problem import FuzzyCSProblem
from fuzzy_cs_solution import FuzzyCSSolution


#not inheriting unittest because of various limitations
class FuzzyCSTest():
    problem = None
    solution = None

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

        

    def testOne(self):
        print "Running test ", inspect.stack()[0][3]
        self.setup_default_problem()
        startTime = time.time()

        #main algorithm to test
        time.sleep(1)
        
        t = time.time() - startTime
        print "Time to run is", t

    def testTwo(self):
        print "Running test ", inspect.stack()[0][3]
        startTime = time.time()

        #main algorithm to test
        time.sleep(2)

        t = time.time() -startTime
        print "Time to run is", t

if __name__ == '__main__':
    test = FuzzyCSTest()
    test.testOne()
    test.testTwo()