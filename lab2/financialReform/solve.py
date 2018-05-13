# -*- coding:utf-8 -*-
import requests
import zipfile
import pandas


class Solution():
    def initial(self):
        response = requests.get("https://www.imf.org/external/pubs/ft/wp/2008/Data/wp08266.zip")
        # print('get if successful:' + str(response is not None))
        with open('data.zip', 'wb') as file:
            file.write(response.content)

        return

    def solve(self):
        countries = 0
        medianNumber = 0.00
        self.initial()
        dataZip = zipfile.ZipFile('data.zip', 'r')
        fileNameList = dataZip.namelist()
        type1 = str(fileNameList[0]).split('.')[1]
        type2 = str(fileNameList[1]).split('.')[1]
        if type1 == 'dta':
            dtaFileName = fileNameList[0]
            excelFileName = fileNameList[1]
        else:
            dtaFileName = fileNameList[1]
            excelFileName = fileNameList[0]

        dta = dataZip.open(dtaFileName)
        dtaDataFrame = pandas.read_stata(dta)
        country_set = set()
        for s in dtaDataFrame.get('country'):
            if s not in country_set:
                country_set.add(s)

        countries = len(country_set)

        # median number below
        country_years = {}

        for each in country_set:
                s = dtaDataFrame[dtaDataFrame.country == each]
                country_years[each] = len(s)

        print(country_years)
        valueList = sorted(country_years.values())
        size = len(valueList)
        if size % 2==0:
            medianNumber = (valueList[size//2-1] + valueList[size//2])/2
        else:
            medianNumber = valueList[size//2-1]


        print(countries)
        print(medianNumber)
        return [countries, medianNumber]
        pass


object = Solution()
object.solve()
