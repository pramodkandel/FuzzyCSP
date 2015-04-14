class FuzzyCSProblem:
	vars_and_domains = {}
	num_vars_per_constraint = 0
	def __init__(self, variables,domains, constraints):
		self.variables = variables
		self.domains = domains
		self.constraints = constraints
		self.set_num_vars_per_constraint()
		self.set_vars_and_domains()



	def get_variables(self):
		return self.variables

	def get_domain(self, variable):
		return self.vars_and_domains[variable]

	def get_constraints(self):
		return self.constraints

	def get_num_constraints(self):
		return len(self.constraints)

	def set_num_vars_per_constraint(self):
		#constraint = self.constraints.keys()[0]
		constraint = self.constraints[0].keys()[0]
		num_vars = 0
		for value in constraint:
			if value != None:
				num_vars += 1
		self.num_vars_per_constraint = num_vars

	def get_num_vars_per_constraint(self):
		return self.num_vars_per_constraint

	def set_vars_and_domains(self):
		vars_n_domains = {}
		for i in range(len(self.variables)):
			var = self.variables[i]
			value = self.domains[i]
			vars_n_domains[var] = value
		self.vars_and_domains = vars_n_domains

	def get_vars_and_domains(self):
		return self.vars_and_domains