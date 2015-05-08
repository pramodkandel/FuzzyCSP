#from fuzzy_csp.src.fuzzy_cs_problem import FuzzyCSProblem
from fuzzy_csp.src.fuzzy_cs_solution import FuzzyCSSolution

#solutions for demo
class DemoSolution:

	def __init__(self,availability_problem, desirability_problem, combined_problem, m=10):
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
			m_best_sols = self.availability_solution.get_m_best_solutions(self.m)
			self.best_availability_sols = m_best_sols
			self.availability_sats = [self.availability_solution.get_joint_satisfaction_degree(sol) for sol in m_best_sols]
		return self.best_availability_sols

	def get_m_best_desirability_sols(self):
		if self.best_desirability_sols == []:
			m_best_sols = self.desirability_solution.get_m_best_solutions(self.m)
			self.best_desirability_sols = m_best_sols
			self.desirability_sats = [self.desirability_solution.get_joint_satisfaction_degree(sol) for sol in m_best_sols]
		return self.best_desirability_sols

	def get_m_best_combined_sols(self):
		if self.best_combined_sols == []:
			m_best_sols = self.combined_solution.get_m_best_solutions(self.m)
			self.best_combined_sols = m_best_sols
			self.combined_sats = [self.combined_solution.get_joint_satisfaction_degree(sol) for sol in m_best_sols]
		return self.best_combined_sols



	def get_nth_best_availability_solution(self,n):
		sols = self.get_m_best_availability_sols()
		if n<= len(sols):
			return sols[len(sols)-n]
		else:
			return False

	def get_nth_best_desirability_solution(self,n):
		sols = self.get_m_best_desirability_sols()
		if n<= len(sols):
			return sols[len(sols)-n]
		else:
			raise Error("exhausted total solutions..")

	def get_nth_best_combined_solution(self,n):
		sols = self.get_m_best_combined_sols()
		if n<= len(sols):
			soln = sols[len(sols)-n]

		else:
			return Error("exhausted total solutions")


	def get_real_item(item_value):
		if item_value[-2:] == '_c' or item_value[-2:]=='_m':
			return item_value[:-2]
		return item_value