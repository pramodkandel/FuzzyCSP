#for testing stuff
from habit_parser import HabitParser
from habit_to_fcsp import HabitToFCSP
from demo_solution import DemoSolution

def test_habit_to_fcsp():
	data_path = '/home/pramod/Documents/spring_2015/cog_rob-6834/FuzzyCSP/fuzzy_csp/demo/data/'
	brkfast_file = data_path + 'breakfast_log.txt'
	ttl_file = data_path + 'time_to_last.txt'
	pref_file = data_path + 'preferences.txt'

	#first test habit parser
	habit_parser = HabitParser(brkfast_file, ttl_file, pref_file)
	variables = habit_parser.get_variables()
	print "Habit vars are:", variables
	domains = habit_parser.get_domains()
	print "Habit domains are:", domains
	domain1 = domains[0]
	habit_list = habit_parser.get_breakfastList
	print "habit list is:", habit_list
	for item in domain1:
		print "Time to last is for item", item, "is:", habit_parser.time_to_last_item(item)
		print "Frequency of use was", habit_parser.get_frequency([item])


	habit_to_fcsp = HabitToFCSP(habit_parser)
	avail_problem = habit_to_fcsp.get_availability_fcsp()
	demo_sol = DemoSolution(avail_problem, None, None)
	print "m best sols: ",demo_sol.get_m_best_availability_sols()
	print "nth best sol: ", demo_sol.get_nth_best_availability_solution(2)


if __name__ == '__main__':
	test_habit_to_fcsp()