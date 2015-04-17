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

    heuristic_backtrack_constraints =[
               {('S','D', None):0.5, 
                ('S','G',None):1.0,
                ('C','B',None):0.1},
               {('S', None, 'W'):1.0,
                ('C', None, 'W'):1.0,
                ('C', None, 'L'):1.0},
               {(None, 'B', 'W'):1.0,
                (None, 'B', 'L'):1.0,
                (None, 'G', 'L'):1.0,
                (None, 'D', 'L'):1.0}                 
                ]

    problem = FuzzyCSProblem(variables,domains, constraints)
    solution = FuzzyCSSolution(problem)

    problem2 = FuzzyCSProblem(variables, domains, heuristic_backtrack_constraints)
    solution2 = FuzzyCSSolution(problem2)

    partial_vars = ['f','t','s']
    partial_values = ['S','D','W']
    partial_joint_sat = solution.get_partial_joint_satisfaction(partial_vars, partial_values)
    print "Partial joint sat is", partial_joint_sat

    print "----------------------------"
    heuristic_solution = solution.get_heuristic_solution()
    print "Heuristic solution is", heuristic_solution
    print "Joint satisfaction degree is", solution.get_joint_satisfaction_degree(heuristic_solution)
    print "---------------------------"

    bnb_solution = solution.get_branch_and_bound_solution()
    print "branch_n_bound solution is", bnb_solution
    print "joint_sat of branch_n_bound is", solution.get_joint_satisfaction_degree(bnb_solution)
    print "--------------------------------"

    alpha = 0.7
    alpha_solutions = solution.get_alpha_solutions(alpha)
    print "all alpha solutions with alpha:",alpha, "are", list(alpha_solutions)
    print "---------------------------"

    feasible_solution = solution.get_a_feasible_solution()
    print "a feasible solution is", feasible_solution
    print "------------------------------"

    all_solutions = solution.get_all_feasible_solutions()
    print "all feasible solutions are", list(all_solutions)
    print "---------------------------------"
    print "---------------------------------"

    all_solutions = solution2.get_all_feasible_solutions()
    print "all feasible solutions 2 are", list(all_solutions)
    print "---------------------------------"


    feasible_solution = solution2.get_a_feasible_solution()
    print "a feasible solution 2 is", feasible_solution
    print "---------------------------------"

    heuristic_solution = solution2.get_heuristic_solution()  
    if not heuristic_solution:
        print "Feasible solutions don't exist"
    else:
        print "Heuristic solution is", heuristic_solution
        print "Joint satisfaction degree is", solution2.get_joint_satisfaction_degree(heuristic_solution)
    print "---------------------------"

    bnb_solution = solution2.get_branch_and_bound_solution()
    if bnb_solution: #if exists
        print "branch_n_bound solution is", bnb_solution
        print "joint_sat of branch_n_bound is", solution2.get_joint_satisfaction_degree(bnb_solution)
    else:
        print "Feasible solution doesn't exist."
    print "--------------------------------"

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