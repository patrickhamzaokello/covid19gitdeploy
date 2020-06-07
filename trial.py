from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


url = "file:///media/pkasemer/Pkase/COVID-19%20Uganda/Resources/Coronavirus%20Update%20(Live)_%20445,815%20Cases%20and%2019,768%20Deaths%20from%20COVID-19%20Virus%20Outbreak%20-%20Worldometer.html"
html = urlopen(url)

soup = BeautifulSoup(html)

title = soup.title

print(title)
print(title.text)

links = soup.find_all('a', href=True)

# for link in links:
#     print(link['href'])

data = []
allrows = soup.find_all("tr")
for row in allrows:
    row_list = row.find_all("td")
    dataRow = []

    for cell in row_list:
        dataRow.append(cell.text)
    data.append(dataRow)


data = data[1:]
# print(data[-2:])

df = pd.DataFrame(data)

print(df.head(2))
print(df.tail(2))

header_list = []
col_headers = soup.find_all("th")
for col in col_headers:
    header_list.append(col.text)

header_list = header_list[:10]
print(header_list)

df.columns = header_list

print(df.head())


#remove non-null values
df2 = df.dropna(axis=0, how='any')
df2.shape


plt.bar(df2['Country,Other'], df2['NewCases'])
plt.xlabel('Country')
plt.ylabel('NewCases')
plt.title('Commparison of New cases for each country')

plt.show()