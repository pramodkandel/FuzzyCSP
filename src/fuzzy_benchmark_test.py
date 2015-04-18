from fuzzy_example_problem import FuzzyExampleProblem
from fuzzy_cs_solution import FuzzyCSSolution
from fuzzy_cs_solution import FuzzyBenchmarkMetrics
import time

class FuzzyBenchmarkTest():
	alpha = 0.7
	joint_sat_type = "productive"
	upper_bound_type = "appropriateness"

	def __init__(self, alpha = alpha, joint_sat_type = joint_sat_type, upper_bound_type = upper_bound_type):
		self.alpha = alpha
		self.joint_sat_type = joint_sat_type
		self.upper_bound_type = upper_bound_type
	


	#benchmarking a problem with several solutions
	def benchmark_problem(self, problem):
		solution = FuzzyCSSolution(problem, self.joint_sat_type, self.upper_bound_type)
		#We benchmark for finding a feasible solution with backtracking, finding best solution with
		#branch and bound, and finding a good solution with heuristic search
		solution.set_do_benchmark(True)

		#first backtracking
		print "Benchmarking backtracking..."
		start_time = time.time()
		found_solution = solution.get_a_feasible_solution()
		runtime = time.time() - start_time
		num_var_assignments = FuzzyBenchmarkMetrics.num_var_assignments
		num_constraints_check = FuzzyBenchmarkMetrics.num_constraint_checks
		print "solution was", found_solution
		if found_solution:
			print "Joint satisfaction was", solution.get_joint_satisfaction_degree(found_solution)
		print "Runtime was", runtime
		print "num_var_assignments was", num_var_assignments
		print "num_constraints_check was", num_constraints_check
		self.cleanup_benchmark_metrics()

		#then heuristic search
		print "Benchmarking heuristic search..."
		start_time = time.time()
		found_solution = solution.get_heuristic_solution()
		runtime = time.time() - start_time
		num_var_assignments = FuzzyBenchmarkMetrics.num_var_assignments
		num_constraints_check = FuzzyBenchmarkMetrics.num_constraint_checks
		print "solution was", found_solution
		if found_solution:
			print "Joint satisfaction was", solution.get_joint_satisfaction_degree(found_solution)
		print "Runtime was", runtime
		print "num_var_assignments was", num_var_assignments
		print "num_constraints_check was", num_constraints_check
		self.cleanup_benchmark_metrics()

		#then branch_and_bound
		print "Benchmarking branch_and_bound search..."
		start_time = time.time()
		found_solution = solution.get_branch_and_bound_solution()
		runtime = time.time() - start_time
		num_var_assignments = FuzzyBenchmarkMetrics.num_var_assignments
		num_constraints_check = FuzzyBenchmarkMetrics.num_constraint_checks
		print "solution was", found_solution
		if found_solution:
			print "Joint satisfaction was", solution.get_joint_satisfaction_degree(found_solution)
		print "Runtime was", runtime
		print "num_var_assignments was", num_var_assignments
		print "num_constraints_check was", num_constraints_check
		self.cleanup_benchmark_metrics()

	def cleanup_benchmark_metrics(self):
		FuzzyBenchmarkMetrics.num_constraint_checks = 0
		FuzzyBenchmarkMetrics.num_var_assignments = 0

	def benchmark_heuristic_algorithm(self):
		#TODO:run problems to show strengths and weaknesses of this algorithm
		pass

	def benchmark_branch_and_bound_algorithm(self):
		#TODO:run problems to show strengths and weaknesses of this algorithm
		pass


	def benchmark_backtracking(self):
		#TODO:run problems to show strengths and weaknesses of this algorithm
		pass

	def benchmark_robot_dressing(self):
		print "Benchmarking on robot dressing problem..."
		robot_problem = FuzzyExampleProblem().get_robot_dressing_problem()
		self.benchmark_problem(robot_problem)

if __name__ == '__main__':
    test = FuzzyBenchmarkTest()
    test.benchmark_robot_dressing()
   
