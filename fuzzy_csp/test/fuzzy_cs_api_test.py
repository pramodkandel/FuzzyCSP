import sys
import getopt
import inspect

from fuzzy_csp.src.fuzzy_cs_problem import FuzzyCSProblem
from fuzzy_csp.src.fuzzy_cs_solution import FuzzyCSSolution
from fuzzy_csp.src.fuzzy_example_problem import FuzzyExampleProblem

#####SOME PARAMETERS######
alpha = 0.7 #used for finding alpha solutions, i.e. solutions with joint satisfaction greater than 0.7
joint_sat_type = "productive" #could be "average", "min", "productive"
upper_bound_type = "appropriateness" #could be "partial_joint_sat" or "appropriateness"
#not inheriting unittest because of various limitations
m = 5 #for m-best solutions

#demonstration of how to instantiate a fuzzy problem
def get_robot_dressing_problem():
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
    return problem 

    

#This demonstrates the public api for solutions/algorithms 
def run_all_solution_algorithms(problem):
    solution = FuzzyCSSolution(problem, joint_sat_type, upper_bound_type)
    print "---------------------------------"
    print "RUNNING ALL ALGORITHMS..."
    print "----------------------------------"

    print "Finding a feasible solution with backtracking..."
    feasible_solution = solution.get_a_feasible_solution_backtracking()
    if feasible_solution:
        print "a feasible solution is", feasible_solution
    else:
        print "Feasible solution doesn't exist."
    print "------------------------------"  

    print "Finding all feasible solutions with backtracking..."
    all_solutions = solution.get_all_feasible_solutions_backtracking()
    print "all feasible solutions are", list(all_solutions)
    print "---------------------------------"

    print "Finding alpha solutions with backtracking..."
    alpha_solutions = solution.get_alpha_solutions_backtracking(alpha)
    print "all alpha solutions with alpha:",alpha, "are", list(alpha_solutions)
    print "---------------------------"

    print "Finding alpha solutions with branch and bound..."
    alpha_bnb_solutions = solution.get_alpha_solutions_branch_n_bound(alpha)
    print "all alpha solutions with alpha:",alpha, "are", list(alpha_bnb_solutions)
    print "---------------------------"

    print "Finding m-best solutions with backtracking..."
    mbest_solutions = solution.get_m_best_solutions(m)
    print "m best solutions with m:",m, "are", mbest_solutions
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


#Various implemented algorithms running on example problems
def run_solutions_on_various_fuzzy_problems():
    robot_problem = get_robot_dressing_problem()
    print "Running solutions for robot dressing problem..."
    run_all_solution_algorithms(robot_problem)

    #There are other example problems, including the robot dressing problem, in FuzzyExampleProblem class
    #which we will use for the following problems
    example_problem = FuzzyExampleProblem()
    heuristic_backtrack_problem = example_problem.get_heuristic_backtracking_problem()
    print "Running solutions for variant of robot dressing problem in which heuristic solution needs to backtrack..."
    run_all_solution_algorithms(heuristic_backtrack_problem)
    
    temporal_problem = example_problem.get_temporal_constraint_problem()
    print "Running solutions for variant of temporal problem given in thought exercise #3..."
    run_all_solution_algorithms(temporal_problem)

    lunch_swim_problem = example_problem.get_lunch_swim_problem()
    print "Running solutions for Fuzzy SCSP of preference & temporal preference problem ..."
    run_all_solution_algorithms(lunch_swim_problem)


if __name__ == '__main__':
    run_solutions_on_various_fuzzy_problems()