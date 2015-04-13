class FuzzyCSProblem:
	vars_and_domains = {}
	def __init__(self, variables,domains, constraints):
		self.variables = variables
		self.domains = domains
		self.constraints = constraints
		
		for i in range(len(variables)):
			var = variables[i]
			dom = domains[i]
			self.vars_and_domains[var] = dom

	def get_variables(self):
		return self.variables

	def get_domain(self, variable):
		return self.vars_and_domains[variable]

	def get_constraints(self):
		return self.constraints

