class FuzzyBenchmark():
	def __init__(self):
		self.runtime = 0
		self.num_constraint_checks = 0
		self.num_var_assignments = 0

	def set_runtime(self, runtime):
		self.runtime = runtime

	def set_num_constraint_checks(self, num_constraint_checks):
		self.num_constraint_checks = num_constraint_checks

	def set_num_var_assignments(self, num_var_assignments):
		self.num_var_assignments = num_var_assignments

	def get_runtime(self):
		return self.runtime

	def get_num_constraint_checks(self):
		return self.num_constraint_checks

	def get_num_var_assignments(self):
		return self.num_var_assignments