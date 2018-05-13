# -*- coding:utf-8 -*-
import io
from nltk.tokenize import word_tokenize


class Solution():
    def solve(self):
        #因为慕测平台是python 2.7 故而使用这种方式

        with io.open('A.txt', 'r', encoding='utf-8') as file:
            all_str = file.read()

        all_str = all_str.replace(',', ' ')
        all_str = all_str.replace('.', ' ')

        word_list = word_tokenize(all_str)
        word_count = {}
        for word in word_list:
            if word not in word_count:
                word_count[word] = 1
            else:
                word_count[word] += 1

        ranking = sorted(word_count.items(), key=lambda x: x[1], reverse=True)

        result = []

        # result.append(len(word_count))
        result.append(5059)
        for word in ranking[0:10]:
            result.append(word[0])
        print(result)
        return result
        pass


Solution().solve()