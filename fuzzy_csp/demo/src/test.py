#for testing stuff
from habit_parser import HabitParser
from habit_to_fcsp import HabitToFCSP
from demo_solution import DemoSolution
import itertools

def test_habit_to_fcsp():
	data_path = '/home/pramod/Documents/spring_2015/cog_rob-6834/FuzzyCSP/fuzzy_csp/demo/data/'
	brkfast_file = data_path + 'breakfast_log.txt'
	ttl_file = data_path + 'time_to_last.txt'
	pref_file = data_path + 'preferences.txt'
	m = 5

	#first test habit parser
	habit_parser = HabitParser(brkfast_file, ttl_file, pref_file)
	variables = habit_parser.get_variables()
	print "Habit vars are:", variables
	domains = habit_parser.get_domains()
	print "Habit domains are:", domains
	domain1 = domains[0]
	habit_list = habit_parser.get_breakfastList()
	print "habit list is:", habit_list
	for item in domain1:
		print "Time to last is for item", item, "is:", habit_parser.time_to_last_item(item)
		print "Frequency of use was", habit_parser.get_frequency([item])

	domain2 = domains[1]
	domain3 = domains[2]
	binary_values = itertools.product(domain2, domain3)
	for values in binary_values:
		triplet = ["", values[0], values[1]]
		pref = habit_parser.get_preference(triplet)
		print "Preference for ", triplet, "is", pref

	habit_to_fcsp = HabitToFCSP(habit_parser)
	avail_problem = habit_to_fcsp.get_availability_fcsp()
	desire_problem = habit_to_fcsp.get_desirability_fcsp()
	combine_problem = habit_to_fcsp.get_combined_fcsp()
	demo_sol = DemoSolution(avail_problem, desire_problem, combine_problem)
	demo_sol.set_m(m)
	m_sols = demo_sol.get_m_best_availability_sols()
	print "m best availability sols: ",m_sols
	print "satisf degrees:", demo_sol.availability_sats

	print "nth best sol: ", demo_sol.get_nth_best_availability_solution(2)

	m_sols = demo_sol.get_m_best_desirability_sols()
	print "m best desirability sols: ",m_sols
	print "satisf degrees:", demo_sol.desirability_sats

	print "nth best sol: ", demo_sol.get_nth_best_desirability_solution(2)

	m_sols = demo_sol.get_m_best_combined_sols()
	print "m best combined sols: ",m_sols
	print "satisf degrees:", demo_sol.combined_sats

	print "nth best sol: ", demo_sol.get_nth_best_combined_solution(2)

if __name__ == '__main__':
	test_habit_to_fcsp()