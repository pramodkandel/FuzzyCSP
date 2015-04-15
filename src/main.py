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

    problem = FuzzyCSProblem(variables,domains, constraints)
    solution = FuzzyCSSolution(problem)
    best_solution, joint_sat = solution.get_best_heuristic_solution_and_joint_sat()

    print "Best solution is", best_solution
    print "Joint satisfaction degree is", joint_sat

    backtrack_solution = solution.get_feasible_solution_with_backtracking()
    print "backtrack_solution is", backtrack_solution
'''
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

if __name__ == "__main__":
    sys.exit(main())