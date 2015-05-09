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
	attempt_num = 2

	#first test habit parser
	habit_parser = HabitParser(brkfast_file, ttl_file, pref_file)
	variables = habit_parser.get_variables()
	print "Habit vars are:", variables
	domains = habit_parser.get_domains()
	print "Habit domains are:", domains

	#test for bread_c and bread_m
	print "time to last for bread_c is", habit_parser.time_to_last_item("bread_c")
	print "ttl for bread_m is", habit_parser.time_to_last_item("bread_m")
	print "freq for bread_m is", habit_parser.get_frequency(["bread_m"])
	print "freq for bread_c is", habit_parser.get_frequency(["bread_c"])
	print "freq for bread is", habit_parser.get_frequency(["bread"])
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

	print "------------FINISHED HABIT PARSER TEST-------------"
	habit_to_fcsp = HabitToFCSP(habit_parser)
	print "Availability Problem.."
	avail_problem = habit_to_fcsp.get_availability_fcsp()
	print "Desirability Problem.."
	desire_problem = habit_to_fcsp.get_desirability_fcsp()
	print "Combined Problem.."
	combine_problem = habit_to_fcsp.get_combined_fcsp()
	demo_sol = DemoSolution(avail_problem, desire_problem, combine_problem)
	demo_sol.set_m(m)
	m_sols = demo_sol.get_m_best_availability_sols()
	print "--------availability sols -----------"
	print "m best availability sols: ",m_sols
	print "satisf degrees:", demo_sol.availability_sats

	nth_best = demo_sol.get_nth_best_availability_solution(attempt_num)
	print "nth best sol: ", nth_best
	stock = []
	for item in nth_best:
		stock.append(habit_to_fcsp.get_availability_score(item))
	print "stock is:", stock

	print "--------desirability sols -----------"
	m_sols = demo_sol.get_m_best_desirability_sols()
	print "m best desirability sols: ",m_sols
	print "satisf degrees:", demo_sol.desirability_sats

	nth_best = demo_sol.get_nth_best_desirability_solution(attempt_num)
	print "nth best sol: ", nth_best
	stock = []
	for item in nth_best:
		stock.append(habit_to_fcsp.get_availability_score(item))
	print "stock is:", stock
	print "--------combined sols -----------"
	m_sols = demo_sol.get_m_best_combined_sols()
	print "m best combined sols: ",m_sols
	print "satisf degrees:", demo_sol.combined_sats

	nth_best = demo_sol.get_nth_best_combined_solution(attempt_num)
	print "nth best sol: ", nth_best
	stock = []
	for item in nth_best:
		stock.append(habit_to_fcsp.get_availability_score(item))
	print "stock is:", stock


if __name__ == '__main__':
	test_habit_to_fcsp()