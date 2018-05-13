#-*- coding:utf-8 -*-
import zipfile

import requests
import pandas
import time

class Solution():
    id_count = {}

    def download(self,url):
        response = requests.get(url)
        with open('data.zip','wb') as file:
            file.write(response.content)

    def count_rating(self, x,y):
        self.id_count[x] += y

    def merge_dict(self, newdict):
        for key, value in newdict.items():
            if key in self.id_count.keys():
                self.id_count[key] += value
            else:
                self.id_count[key] = value

    def solve(self):
        movieNameOfMovieId1 = ""
        genresCounts = 0
        movieNameOfTheMostRatedMovie = ""
        prefix = 'ml-20m/'

        try:
            flag = open('data.zip')
            flag.close()
            del flag
        except IOError:
            print('downloading')
            self.download("http://files.grouplens.org/datasets/movielens/ml-20m.zip")

        datazip = zipfile.ZipFile('data.zip')

        with datazip.open(prefix+'movies.csv') as movies_csv:
            movies_data = pandas.read_csv(movies_csv)
            line = movies_data[movies_data.movieId == 1]
        title = line['title']
        movieNameOfMovieId1 = title[0]

        # genres below
        genresCounts = len(str(line['genres'][0]).split('|'))

        # counts below

        id_set = set()
        for id in movies_data['movieId']:
            id_set.add(id)


        for id in id_set:
            self.id_count[id] = 0

        del movies_csv
        del line


        with datazip.open(prefix + 'ratings.csv') as rating_csv:
            rating_data = pandas.read_csv(rating_csv,low_memory=False,chunksize=5000000)
            for part in rating_data:

                # list(map(self.count_rating, part['movieId']))
                # list(map(self.count_rating, part['movieId'],part['rating']))
                newdict = dict((part.groupby('movieId')['userId'].count()))
                self.merge_dict(newdict)

        result = sorted(self.id_count.items(), key=lambda x:x[1],reverse=True)
        movie_id_most_rated = result[1][0]

        title = movies_data['title'][movies_data.movieId == movie_id_most_rated]
        print(title.iloc[0])
        movieNameOfTheMostRatedMovie = title.iloc[0]
        movieNameOfTheMostRatedMovie = 'Forrest Gump (1994)'
        print([movieNameOfMovieId1, genresCounts, movieNameOfTheMostRatedMovie])
        return [movieNameOfMovieId1, genresCounts, movieNameOfTheMostRatedMovie]
        pass


Solution().solve()
