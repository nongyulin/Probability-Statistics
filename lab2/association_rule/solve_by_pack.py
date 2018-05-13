import pyfpgrowth
import pandas as pd

class Solution():
    def solve(self):
        vote_data = pd.read_csv('A.csv')
        transaction = vote_data.values
        patterns = pyfpgrowth.find_frequent_patterns(transaction, 150)
        print(patterns)
        rules = pyfpgrowth.generate_association_rules(patterns, 0.9)
        result_list = []
        for key,value in rules.items():
            i_list = []
            i_list.append(list(key))
            i_list.append(list(value[0]))
            result_list.append(i_list)

        print(result_list)
        string = ''
        for item in result_list:
            string += str(item) + '\n'
        with open('result.txt','w') as file:
            file.write(string)
        return result_list


Solution().solve()