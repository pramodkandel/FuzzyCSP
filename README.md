# 6834_pset3

Fuzzy Constraint Satisfaction Problem tutorial and implementation for Cognitive Robotics (6.834) MIT

Group members: Manushaqe Muco, Pallavi Mishra, Pramod Kandel

Instructions to configure the project:
1. Download or clone this project.
1. From the root directory(where setup.py file is), run this in terminal: sudo python setup.py install . This makes sure the package installs correctly in your system. 
2. To see an example of all the public API use, see test/fuzzy_cs_api_test.py. You can run it with this command: python fuzzy_cs_api_test.py
3. Unit tests for internal functions are placed in test/fuzzy_cs_unittest.py, which you can run as well.
4. Benchmark tests are under benchmark/fuzzy_benchmark_test.py. If you run it, the results appear in a txt file in the same folder. The results compare various algorithms according to various problem metrics. For problem metrics, see the class variables of FuzzyExampleProblem in src/fuzzy_example_problem.py.


