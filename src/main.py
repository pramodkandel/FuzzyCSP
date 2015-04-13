import sys
import getopt

from fuzzy_cs_problem import FuzzyCSProblem
from fuzzy_cs_solution import FuzzyCSSolution


class FCSPException(Exception):
    def __init__(self, msg):
        self.msg = msg

def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "h", ["help"])
            return main_wrapper(opts, args)
        except getopt.error, msg:
             raise FCSPException(msg)
        # more code, unchanged
    except FCSPException, err:
        print >>sys.stderr, err.msg
        print >>sys.stderr, "for help use --help"
        return 2


def main_wrapper(opts, args):
    #create a problem right now
    vars_and_domains = {};
    variables = ['f', 't', 's']

    domains = [('S', 'C'),('D', 'B', 'G'),('L', 'W')]

    constraints = {
                    ('S','D', None):1.0, 
                    ('S','B',None):0.4,
                    ('S','G',None):0.2,
                    ('C','G',None):0.8,
                    ('C','B',None):0.5,
                    ('S', None, 'L'):1.0,
                    ('S', None, 'W'):0.7,
                    ('C', None, 'W'):1.0,
                    ('C', None, 'L'):0.1,
                    (None, 'D', 'W'):1.0,
                    (None, 'D', 'L'):0.7,
                    (None, 'B', 'W'):1.0,
                    (None, 'B', 'L'):0.4,
                    (None, 'G', 'L'):1.0,
                    (None, 'G', 'W'):0.6
                  }

    problem = FuzzyCSProblem(variables,domains, constraints)

    print "Variables are", problem.get_vars()

    solution = FuzzyCSSolution(problem)
    print "Pruning is", solution.get_pruning()

if __name__ == "__main__":
    sys.exit(main())