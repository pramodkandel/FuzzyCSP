class HabitParser:

    domains = [ [], [], []]
    
    breakfast_file_toList = [] #reads breakfast file as a list
    
    
    time_to_last_dict = {}#stores lasting times/servings for each item

    preferences_dict={} #store preferences for master (x1, x2, x3) : float
    
    def __init__(self, breakfast_file, time_to_last_file, master_preferences_file):
        self.breakfast = breakfast_file
        self.time_to_last = time_to_last_file
        self.master_preferences = master_preferences_file
        self.variables = ['main', 'complement', 'drinks']
        
        #populate breakfastlist
        with open(self.breakfast, 'r') as f:
            lines = f.read().splitlines()
        for i in lines[2:]:
            hello = i.split('|')
            hello = [k.strip(' \t+\n+') for k in hello]
            if hello!=['']:
                self.breakfast_file_toList.append(hello)
        f.close()
        
       
        
        #populate domains
        for i in self.breakfast_file_toList:
            if i[0] not in self.domains[0]:
                self.domains[0].append(i[0])
            if i[1] not in self.domains[1]:
                self.domains[1].append(i[1])
            if i[2] not in self.domains[2]:
                self.domains[2].append(i[2]) #drinks, no repetition

        for i in self.domains[0]: #take care of similar values for main and complement
            if i in self.domains[1]:
                index_0 = self.domains[0].index(i)
                index_1 = self.domains[1].index(i)
                self.domains[0][index_0] +='_m'
                self.domains[1][index_1] +='_c'

        #populate time_to_last_dict
        with open(self.time_to_last, 'r') as f:
            lines = f.read().splitlines()
            for i in lines[2:]:
                hello = i.split(':')
                hello = [k.strip(' \t+\n+') for k in hello]
                if hello != ['']:
                    self.time_to_last_dict[hello[0]] = int(hello[1])
        f.close()
        
        #populate preferences_dict
        with open(self.master_preferences, 'r') as f:
              lines = f.read().splitlines()
              for i in lines[2:]:
                hello = i.split('|')
                hello = [k.strip(' \n+\t+') for k in hello]
                if hello != ['']:
                    self.preferences_dict[(hello[0],hello[1], hello[2])] = float(hello[3])
        f.close()
        
    
    def get_variables(self):
        "return variables"
        return self.variables

    def get_domain(self, variable):
        "returns the domain for given variable"
        if variable == 'main':
            return self.domains[0]
        elif variable == 'complement':
            return self.domains[1]
        else:
            return self.domains[2]

    def get_domains(self):
        "return domains"
        return self.domains

    def get_all_items(self):
        "return all domains as a list"
        all_items = []
        for domain in self.domains:
            all_items.extend(domain)
        return all_items

    def get_breakfastList(self):
        "returns every breakfast master had in the file as a list"
        return self.breakfast_file_toList

    def get_breakfast_day(self, day_number):
        "returns the breakfast master had on Day day_number"
        index = day_number - 1
        return self.breakfast_file_toList[index]

    def time_to_last_item(self, item):
        "returns how long the item lasts: i.e number of servings"
        item_new = self.actual_item(item)
        
        if item_new in self.time_to_last_dict:
            return self.time_to_last_dict[item_new]
        else: 
            return 0
        
    def isSublist(self, list_, sublist):
        "help function for get_frequency(item_list)"
        if not isinstance(list_, list):
            list_ = list(list_)
        sublen = len(sublist)
        for i in range(len(list_)-sublen+1):
            if list_[i:i+sublen] == sublist:
                return True
        return False
    
    def actual_item(self, item):
        "help function. Given an item bread_c --> bread,item is string"
        if item[-2:] == '_c' or item[-2:]=='_m':
            return item[:-2]
        else:
            return item
        
    def get_frequency(self,item_list):
        "item_list can be [item], [item1, item2], [item1,item2,item3]"
        l = []
        for il in item_list:
            l.append(self.actual_item(il))
        #print l
            
        count = 0
        for i in  self.breakfast_file_toList:
            if self.isSublist(i, l):
                count +=1
        return count

    def get_preference(self, items):
        main = items[0]
        complement = items[1]
        drinks = items[2]
        "return preference for triplet of items ex: ('eggs', 'bread', '')"

        main_c = self.actual_item(main)
        complement_c = self.actual_item(complement)
        drinks_c = self.actual_item(drinks)
        
        if (main_c, complement_c, drinks_c) in self.preferences_dict:
            return self.preferences_dict[(main_c, complement_c, drinks_c)]
        else:
            return None


        
