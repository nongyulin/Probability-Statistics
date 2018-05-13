# -*- coding:utf-8 -*-
import requests
import pandas as pd
import time
import re
import itertools


def download(name, url):
    res = requests.get(url)
    with open(name, 'wb') as file:
        file.write(res.content)


def get_index_of(name):
    result = re.findall('[a-zA-z\?]*(.+?)$', name)[0]
    return int(result)


def contain_duplicate(item):
    item_set = set(item)
    return len(item) != len(item_set)


def union_tuple(ituple):
    iset_1 = set(ituple[0])
    iset_2 = set(ituple[1])
    return iset_1 | iset_2

def union_two_tuple(ituple1,ituple2):
    iset_1 = set(ituple1)
    iset_2 = set(ituple2)
    return iset_1 | iset_2

def to_index_list(index_set):
    index_list = []
    for item in index_set:
        index = get_index_of(item)
        if index not in index_list:
            index_list.append(index)
    return index_list


def remove_duplicate_in_dict(idict):
    pass


def search_data(vote_data, key):
    index_list = to_index_list(key)
    groupby = vote_data.groupby(index_list)
    size = groupby.size()
    size_dict = dict(size)
    new_size_dict = {}
    for k,v in size_dict.items():
        new_size_dict[tuple(sorted(k,key=lambda x:get_index_of(x)))] = v
    return new_size_dict.get(tuple(sorted(key,key=lambda x:get_index_of(x))), 0)


class Solution():
    def solve(self):
        start = time.clock()
        try:
            file = open('A.csv')
            file.close()
            del file
        except IOError:
            print('downloading...')
            print('the url is invalid')
            return
            # download('A.csv','https://archive.ics.uci.edu/ml/datasets/Congressional+Voting+Record')
        # download('name.txt','https://archive.ics.uci.edu/ml/machine-learning-databases/voting-records/house-votes-84.names')

        vote_data = pd.read_csv('A.csv', header=-1)

        num_of_man = len(vote_data)
        num_of_votes = len(vote_data.loc[0])

        minimum_support = 150

        # size = 1
        dict_1 = {}
        for j in range(0, num_of_votes):
            groups = vote_data.groupby([j]).count()
            for index, row in groups.iterrows():
                if j == 1:
                    t = 2
                else:
                    t = 1
                appear_times = row[t]
                if appear_times >= minimum_support:
                    index_set = set()
                    index_set.add(index)
                    index_tuple = tuple(index_set)
                    dict_1[index_tuple] = appear_times

        # 2　<= size <= num_of_votes
        result_list = []
        result_list.append(dict_1)
        for k in range(1, num_of_votes):

            k_dict = {}
            last_dict = result_list[k - 1]
            last_index_set = set(last_dict)
            k_dict = {}

            for item in itertools.product(last_index_set, last_index_set):
                new_index_set = union_tuple(item)
                # print(new_index_set)
                index_list_key = to_index_list(new_index_set)
                if len(index_list_key) != k+1:
                    continue
                groupby = vote_data.groupby(index_list_key)
                groupby_size = groupby.size()
                new_dict = dict(groupby_size)
                new_dict = dict(filter(lambda x: x[0] == tuple(new_index_set), new_dict.items()))
                k_dict.update(new_dict)
                # print(index_list_key)

            k_dict = dict(filter(lambda x: x[1] >= minimum_support, k_dict.items()))
            if len(k_dict) == 0:
                break
            result_list.append(k_dict)
            print('klist=', k_dict)

        # find relations
        count_list = []
        total_dict = {}
        for e_dict in result_list:
            total_dict.update(e_dict)

        new_total_dict = {}
        for key,value in total_dict.items():
            sort_key = tuple(sorted(key))
            new_total_dict[sort_key] = total_dict[key]

        print(new_total_dict)
        for product in itertools.product(new_total_dict.items(),new_total_dict.items()):
            item_1 = product[0]
            item_2 = product[1]
            if item_1 == item_2:
                continue
            key_left = item_1[0]
            value_left = item_1[1]
            key_right = item_2[0]
            value_right = item_2[1]

            condition_1 = (value_right / value_left) >= 0.9

            union_key = union_two_tuple(key_left,key_right)


            length = len(to_index_list(union_key))
            if length != (len(key_left) + len(key_right)):
                continue

            union_value = search_data(vote_data, tuple(sorted(union_key)))
            if union_value==0:
                continue
            condition_2 = (value_right / union_value) >=0.45


            if condition_1 and condition_2:
                relation_list = []
                relation_list.append(key_left)
                relation_list.append(key_right)
                count_list.append(relation_list)

        print('count list=',count_list)
        print('count list size=',count_list)
        print('take time = ', time.clock() - start)
        print('relation list',relation_list)
        return count_list
        pass


Solution().solve()
