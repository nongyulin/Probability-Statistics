# -*- coding:utf-8 -*-
import pandas as pd
import math


class Solution():
    def solve(self, R, Y, ratings, k):
        frame = pd.DataFrame(Y)
        counts_frame = pd.DataFrame(R)
        counts_list = []
        user_rating = pd.DataFrame(ratings)
        user_rating = user_rating[0]

        # 欧几里得距离
        # apply_result = frame.apply(lambda x:pow(user_rating - x, 2).sum())
        # 余弦相似度
        apply_result = frame.apply(lambda x:
                                   ((user_rating * x).sum())
                                   / math.sqrt(pow(user_rating, 2).sum()) * math.sqrt(pow(x, 2).sum()))
        counts_list = list(apply_result)

        index_list = []
        for i in range(0, len(counts_list)):
            cur_min_index = counts_list.index(min(counts_list))
            index_list.append(cur_min_index)
            counts_list[cur_min_index] = 2147483647

        nearest_index = -1
        for nearest in index_list:
            if frame[frame[nearest] > 0][nearest].count() >= k:
                print(frame[frame[nearest] > 0][nearest].count())
                nearest_index = nearest
                break

        if nearest_index == -1:
            print('error')
            return
        nearest_col = frame[nearest_index]

        result_set = set()
        for i in range(0, k + 1):
            idmax = nearest_col.idxmax()
            nearest_col.iloc[idmax] = -1
            result_set.add(idmax)
            print(result_set, idmax, nearest_col.iloc[idmax])

        # 似乎在webide里面不加iloc是复制一份，不是修改
        print(result_set)
        return result_set
        pass


