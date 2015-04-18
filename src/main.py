import sys
import getopt

from fuzzy_cs_problem import FuzzyCSProblem
from fuzzy_cs_solution import FuzzyCSSolution
from fuzzy_example_problem import FuzzyExampleProblem

#####SOME PARAMETERS######
alpha = 0.7 #used for finding alpha solutions, i.e. solutions with joint satisfaction greater than 0.7
joint_sat_type = "average" #could be "average", "min", "productive"
upper_bound_type = "appropriateness" #could be "partial_joint_sat" or "appropriateness"

#Various implemented algorithms running on example problems
def main_wrapper(opts, args):
    example_problem = FuzzyExampleProblem();
    robot_problem = example_problem.get_robot_dressing_problem()
    print "Running solutions for robot dressing problem..."
    run_all_solution_algorithms(robot_problem)

    heuristic_backtrack_problem = example_problem.get_heuristic_backtracking_problem()
    print "Running solutions for variant of robot dressing problem in which heuristic solution needs to backtrack..."
    run_all_solution_algorithms(heuristic_backtrack_problem)
    
    temporal_problem = example_problem.get_temporal_constraint_problem()
    print "Running solutions for variant of temporal problem given in thought exercise #3..."
    run_all_solution_algorithms(temporal_problem)

    lunch_swim_problem = example_problem.get_lunch_swim_problem()
    print "Running solutions for Fuzzy SCSP of preference & temporal preference problem ..."
    run_all_solution_algorithms(lunch_swim_problem)
    
    #TODO:ADD some more problems: 1) crisp constraints, 2) Francesca's dinner problem 3) Our lunch problem 
                                #4)infeasible(some variables don't satisfy any constraints), this is only
                                #infeasible for the joint_sat_type of "productive" and "min"
                                #5) Problems that don't 



#This demonstrates all the api necessary
def run_all_solution_algorithms(problem):
    #print "problem variables:", problem.get_variables()
    #print "problem domains", problem.get_domains()
    #print "problem constraints:"
    #for constraint in problem.get_constraints():
        #print constraint
    solution = FuzzyCSSolution(problem, joint_sat_type, upper_bound_type)
    print "---------------------------------"
    print "RUNNING ALL ALGORITHMS..."
    print "----------------------------------"

    print "Finding a feasible solution with backtracking..."
    feasible_solution = solution.get_a_feasible_solution()
    if feasible_solution:
        print "a feasible solution is", feasible_solution
    else:
        print "Feasible solution doesn't exist."
    print "------------------------------"  

    print "Finding all feasible solutions with backtracking..."
    all_solutions = solution.get_all_feasible_solutions()
    print "all feasible solutions are", list(all_solutions)
    print "---------------------------------"

    print "Finding alpha solutions with alpha-backtracking..."
    alpha_solutions = solution.get_alpha_solutions(alpha)
    print "all alpha solutions with alpha:",alpha, "are", list(alpha_solutions)
    print "---------------------------"

    print "Finding a solution with heuristic approach..."
    heuristic_solution = solution.get_heuristic_solution()
    if heuristic_solution:
        print "Heuristic solution is", heuristic_solution
        print "Joint satisfaction degree is", solution.get_joint_satisfaction_degree(heuristic_solution)
    else:
        print "Feasible solution doesn't exist."
    print "---------------------------"

    print "Finding the best solution with branch and bound algorithm..."
    bnb_solution = solution.get_branch_and_bound_solution()
    if bnb_solution:
        print "branch_n_bound solution is", bnb_solution
        print "joint_sat of branch_n_bound is", solution.get_joint_satisfaction_degree(bnb_solution)
    else:
        print "Feasible solution doesn't exist."
    print "--------------------------------"



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


if __name__ == "__main__":
    sys.exit(main())
