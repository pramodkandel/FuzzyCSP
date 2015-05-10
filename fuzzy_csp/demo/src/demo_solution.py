#from fuzzy_csp.src.fuzzy_cs_problem import FuzzyCSProblem
from fuzzy_csp.src.fuzzy_cs_solution import FuzzyCSSolution

#solutions for demo
class DemoSolution:

	def __init__(self,availability_problem, desirability_problem, combined_problem, m=10):
		self.availability_problem = availability_problem
		self.desirability_problem = desirability_problem
		self.combined_problem = combined_problem

		self.availability_solution = FuzzyCSSolution(availability_problem)
		self.desirability_solution = FuzzyCSSolution(desirability_problem)
		self.combined_solution = FuzzyCSSolution(combined_problem)
		self.m = m

		self.best_availability_sols = []
		self.availability_sats = []
		self.best_desirability_sols = []
		self.desirability_sats = []
		self.best_combined_sols = []
		self.combined_sats = []

	def set_m(self,m):
		self.m=m



	def get_m_best_availability_sols(self):
		if self.best_availability_sols == []:
			m_best_sols = self.availability_solution.get_m_best_solutions_branch_n_bound(self.m)
			self.best_availability_sols = m_best_sols
			self.availability_sats = [self.availability_solution.get_joint_satisfaction_degree(sol) for sol in m_best_sols]
		return self.best_availability_sols

	def get_m_best_desirability_sols(self):
		if self.best_desirability_sols == []:
			m_best_sols = self.desirability_solution.get_m_best_solutions_branch_n_bound(self.m)
			self.best_desirability_sols = m_best_sols
			self.desirability_sats = [self.desirability_solution.get_joint_satisfaction_degree(sol) for sol in m_best_sols]
		return self.best_desirability_sols

	def get_m_best_combined_sols(self):
		if self.best_combined_sols == []:
			m_best_sols = self.combined_solution.get_m_best_solutions_branch_n_bound(self.m)
			self.best_combined_sols = m_best_sols
			self.combined_sats = [self.combined_solution.get_joint_satisfaction_degree(sol) for sol in m_best_sols]
		return self.best_combined_sols

	def get_mbest_fix_solutions(self,sol_type, want_items, no_want_items):
		final_want_items = []
		final_no_want_items = []
		sol_instance = None;
		if (sol_type == "availability"):
			all_domain_items = self.get_domains_as_list(self.availability_problem)
			sol_instance = self.availability_solution
		elif (sol_type == "desirability"):
			all_domain_items = self.get_domains_as_list(self.desirability_problem)
			sol_instance = self.desirability_solution
		elif (sol_type == "combined"):
			all_domain_items = self.get_domains_as_list(self.combined_problem)
			sol_instance = self.combined_solution
		else:
			raise Error("Wrong solution type asked.")

		for item in want_items:
			if item not in all_domain_items:
				final_want_items.append(item + "_c")
				final_want_items.append(item + "_m")
				final_want_items.append(item + "_d")
			else:
				final_want_items.append(item)

		for item in no_want_items:
			if item not in all_domain_items:
				final_no_want_items.append(item + "_c")
				final_no_want_items.append(item + "_m")
				final_no_want_items.append(item + "_d")
			else:
				final_no_want_items.append(item)

		print "final want items: ", final_want_items
		print "final no want items: ", final_no_want_items
		solutions = sol_instance.get_m_best_fixed_solutions_branch_n_bound(self.m, final_want_items, final_no_want_items)
		real_solutions = []
		for solution in solutions:
			real_solutions.append(self.get_real_sol(solution))

		return real_solutions


	def get_domains_as_list(self, problem):
		all_domain_values = []
		for domain in problem.get_domains():
			all_domain_values.extend(list(domain))
		return all_domain_values

	def get_nth_best_availability_solution(self,n):
		sols = self.get_m_best_availability_sols()
		if n<= len(sols):
			soln = sols[len(sols)-n]
			return self.get_real_sol(soln)
		else:
			return False

	def get_nth_best_desirability_solution(self,n):
		sols = self.get_m_best_desirability_sols()
		if n<= len(sols):
			soln = sols[len(sols)-n]
			return self.get_real_sol(soln)
		else:
			raise Error("exhausted total solutions..")

	def get_nth_best_combined_solution(self,n):
		sols = self.get_m_best_combined_sols()
		if n<= len(sols):
			soln = sols[len(sols)-n]
			return self.get_real_sol(soln)
		else:
			return Error("exhausted total solutions")


	def get_real_sol(self, solution):
		sol = []
		for item_value in solution:
			if item_value[-2:] == '_c' or item_value[-2:]=='_m':
				sol.append(item_value[:-2])
			else:
				sol.append(item_value)
		return tuple(sol)