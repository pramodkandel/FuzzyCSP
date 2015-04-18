from fuzzy_example_problem import FuzzyExampleProblem
from fuzzy_cs_solution import FuzzyCSSolution
from fuzzy_cs_solution import FuzzyBenchmarkMetrics
import time

class FuzzyBenchmarkTest():
	alpha = 0.7
	joint_sat_type = "productive"
	upper_bound_type = "appropriateness"

	file_to_write = None

	def __init__(self, alpha = alpha, joint_sat_type = joint_sat_type, 
		upper_bound_type = upper_bound_type, file_to_write = file_to_write):
		self.alpha = alpha
		self.joint_sat_type = joint_sat_type
		self.upper_bound_type = upper_bound_type
		self.file_to_write = file_to_write


	#benchmarking a problem with several solutions
	def benchmark_problem(self, problem, f=None, sol_param=None, open_new_file=True):
		solution = FuzzyCSSolution(problem, self.joint_sat_type, self.upper_bound_type)
		#We benchmark for finding a feasible solution with backtracking, finding best solution with
		#branch and bound, and finding a good solution with heuristic search
		solution.set_do_benchmark(True)
		solution.get_search_tree() #it makes the search tree

		if not self.file_to_write:
			file_to_write = "benchmark_problem.txt"
		else:
			file_to_write = self.file_to_write
	
                if open_new_file == True:	
		    f = open(file_to_write, 'w+')
		    #f.write("###"+str(time.time())+"###\n")
		    f.write("BLANK, num_constraint_checks, num_var_assignments, runtime, sol_param\n")

		#heuristic search
		print "Benchmarking heuristic search..."
		start_time = time.time()
		found_solution = solution.get_heuristic_solution()
		runtime = time.time() - start_time
		num_var_assignments = FuzzyBenchmarkMetrics.num_var_assignments
		num_constraints_check = FuzzyBenchmarkMetrics.num_constraint_checks
		print "solution was", found_solution
		if found_solution:
			print "Joint satisfaction was", solution.get_joint_satisfaction_degree(found_solution)
			heuristics_joint_sat_value = solution.get_joint_satisfaction_degree(found_solution)
		print "Runtime was", runtime
		print "num_var_assignments was", num_var_assignments
		print "num_constraints_check was", num_constraints_check
		#write info to file
		f.write("heuristic_search, "+str(num_constraints_check)+", "+str(num_var_assignments)+", "+str(runtime)+", "+str(sol_param)+"\n")
		self.cleanup_benchmark_metrics()

		#branch_and_bound
		print "Benchmarking branch_and_bound search..."
		start_time = time.time()
		found_solution = solution.get_branch_and_bound_solution()
		runtime = time.time() - start_time
		num_var_assignments = FuzzyBenchmarkMetrics.num_var_assignments
		num_constraints_check = FuzzyBenchmarkMetrics.num_constraint_checks
		print "solution was", found_solution
		if found_solution:
			print "Joint satisfaction was", solution.get_joint_satisfaction_degree(found_solution)
			bnb_joint_sat_value = solution.get_joint_satisfaction_degree(found_solution)
		print "Runtime was", runtime
		print "num_var_assignments was", num_var_assignments
		print "num_constraints_check was", num_constraints_check
		#write info to file
		f.write("branch_and_bound, "+str(num_constraints_check)+", "+str(num_var_assignments)+", "+str(runtime)+", "+str(sol_param)+"\n")

		self.cleanup_benchmark_metrics()


		#backtracking
		print "Benchmarking backtracking..."
		start_time = time.time()

		#found_solution = solution.get_a_feasible_solution()
		print "alpha solution = ",min(heuristics_joint_sat_value,bnb_joint_sat_value)
		found_solution = solution.get_an_alpha_solution(min(heuristics_joint_sat_value,bnb_joint_sat_value))
		
		runtime = time.time() - start_time
		num_var_assignments = FuzzyBenchmarkMetrics.num_var_assignments
		num_constraints_check = FuzzyBenchmarkMetrics.num_constraint_checks
		print "solution was", found_solution
		if found_solution:
			print "Joint satisfaction was", solution.get_joint_satisfaction_degree(found_solution)
		print "Runtime was", runtime
		print "num_var_assignments was", num_var_assignments
		print "num_constraints_check was", num_constraints_check

		#write info to file
		f.write("backtracking, "+str(num_constraints_check)+", "+str(num_var_assignments)+", "+str(runtime)+", "+str(sol_param)+"\n")
		self.cleanup_benchmark_metrics()
		#close the file in the end
                if open_new_file == True:	
		    f.close()

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

    #test.benchmark_robot_dressing()

    f = open("BM_Tightness.txt", 'w+')
    #f.write("###"+str(time.time())+"###\n")
    f.write("BLANK, num_constraint_checks, num_var_assignments, runtime, sol_param\n")

    for i in [float(j)/100 for j in range(0,100,5)]:
       print "Tightness = ", i
       sample_problem = FuzzyExampleProblem(3,6,2,i).generate_example_problem()
       test.benchmark_problem(sample_problem,f,i,False)
    
    f.close() 
