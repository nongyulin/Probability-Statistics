#-*- coding:utf-8 -*-
import pandas
import requests
import zipfile

def download(url):
    response = requests.get(url)
    with open('data.zip','wb') as file:
        file.write(response.content)

class Solution():
    def solve(self):
        movieName = ''

        try:
            file = open('data.zip')
            file.close()
            del file
        except IOError:
            download('https://www.imf.org/external/pubs/ft/wp/2008/Data/wp08266.zip')

        data_zip = zipfile.ZipFile('data.zip')
        dta_filename = data_zip.namelist()[0]
        dta_file = data_zip.open(dta_filename)
        dta_data = pandas.read_stata(dta_file)
        part = dta_data[dta_data.Transition == 1][['country','finreform','year']]
        group = part.groupby('country')
        result = group.agg(lambda x:x.max()-x.min())
        result['ratio'] = result['finreform'] / result['year']
        ratio = result['ratio']
        movieName = ratio.idxmax()
        print(movieName)
        return movieName
        pass


Solution().solve()