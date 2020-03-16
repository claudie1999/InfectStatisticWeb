import csv
import pandas as pd

province_distribution = {}
with open('data/province.csv', 'r', encoding="UTF-8") as f:
        next(f)
        dataLine = f.readline().strip("")
        while dataLine != "":
            tmpList = dataLine.split(",")
            province_distribution[tmpList[1]] = int(tmpList[2])
            dataLine = f.readline().strip("\n")
        f.close()
        print(province_distribution)


province = list(province_distribution.keys())
values = list(province_distribution.values())

print(province)
print(values)

