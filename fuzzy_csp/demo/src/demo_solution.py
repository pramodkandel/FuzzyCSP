#solutions for demo
class DemoSolution:

	def __init__(self,availability_problem, desirability_problem, combined_problem, m=10):
		self.availability_solution = FuzzyCSSolution(availability_problem)
		self.desirability_solution = FuzzyCSSolution(desirability_problem)
		self.combined_solution = FuzzyCSSolution(combined_problem)
		self.m = m
		self.best_availability_sols = None
		self.best_desirability_sols = None
		self.best_combined_sols = None

	def get_m_best_availability_sols(self):
		if self.best_availability_sols == None:
			self.best_availability_sols = self.availability_solution.get_m_best_solutions(self.m)
		return self.best_availability_sols

	def get_m_best_desirability_sols(self):
		if self.best_desirability_sols == None:
			self.best_desirability_sols = self.desirability_solution.get_m_best_solutions(self.m)
		return self.best_availability_sols

	def get_m_best_combined_sols(self):
		if self.best_combined_sols == None:
			self.best_combined_sols = self.combined_solution.get_m_best_solutions(self.m)
		return self.best_availability_sols

	def get_nth_best_availability_solution(self,n):
		sols = self.get_m_best_availability_sols()
		if n<= len(sols):
			return sols[len(sols)-1 -n]
		else:
			return False

	def get_nth_best_desirability_solution(self,n):
		sols = self.get_m_best_desirability_sols()
		if n<= len(sols):
			return sols[len(sols)-1 -n]
		else:
			return False

	def get_nth_best_combined_solution(self,n):
		sols = self.get_m_best_combined_sols()
		if n<= len(sols):
			return sols[len(sols)-1 -n]
		else:
			return False