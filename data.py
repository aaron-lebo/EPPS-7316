import csv
from glob import glob

IGNORED = (
           'Arab World',
           'Caribbean small states',
           'East Asia & Pacific (all income levels)',
           'East Asia & Pacific (developing only)',
           'East Asia and the Pacific (IFC classification)',
           'Euro area',
           'Europe & Central Asia (all income levels)',
           'Europe & Central Asia (developing only)',
           'Europe and Central Asia (IFC classification)',
           'European Union',
           'Heavily indebted poor countries (HIPC)',
           'High income',
           'High income: OECD',
           'High income: nonOECD',
           'Latin America & Caribbean (all income levels)',
           'Latin America & Caribbean (developing only)',
           'Latin America and the Caribbean (IFC classification)',
           'Least developed countries: UN classification',
           'Low & middle income',
           'Low income',
           'Lower middle income',
           'Middle East & North Africa (all income levels)',
           'Middle East & North Africa (developing only)',
           'Middle East and North Africa (IFC classification)',
           'Middle income',
           'North America',
           'Not classified',
           'OECD members',
           'Other small states',
           'Pacific island small states',
           'Small states',
           'South Asia',
           'South Asia (IFC classification)',
           'Sub-Saharan Africa (IFC classification)',
           'Sub-Saharan Africa (all income levels)',
           'Sub-Saharan Africa (developing only)',
           'Upper middle income',
           'World'
           )
data = {}
header = ['id', 'country', 'year']
countries = []
for path in sorted(glob('*_Topic_en_csv_v2.csv')):
    file = open(path, 'rb')
    reader = csv.reader(file)
    reader.next()
    reader.next()
    head = reader.next()
    for row in reader:
        country = row[0]
        if country in IGNORED:
            continue

        if not country in countries:
            countries.append(country)

        index = countries.index(country)
        indicator = row[2]
        if not indicator in header:
            header.append(indicator)

        row = zip(head, row)
        for year in row[4:]:
          if not year[0]:
              continue

          key = (index, country, year[0])
          if not data.get(key):
              data[key] = {}

          data[key][indicator] = year[1]

    file.close()

file = open('out1.csv', 'wb')
writer = csv.writer(file)
writer.writerow(header)
file3 = open('out3.csv', 'wb')
writer3 = csv.writer(file3)
writer3.writerow(header)
for key, value in sorted(data.items()):
    key_1 = (key[0], key[1], str(int(key[2]) + 1))
    orig = value['GDP per capita (current US$)']
    if data.get(key_1):
        value['GDP per capita (current US$)'] = data[key_1]['GDP per capita (current US$)']
    else:
        value['GDP per capita (current US$)'] = ''

    writer.writerow(list(key) + [value[k] for k in header[3:]])
    value['GDP per capita (current US$)'] = orig

    key_3 = (key[0], key[1], str(int(key[2]) + 3))
    if data.get(key_3):
        value['GDP per capita (current US$)'] = data[key_3]['GDP per capita (current US$)']
    else:
        value['GDP per capita (current US$)'] = ''

    writer3.writerow(list(key) + [value[k] for k in header[3:]])
    value['GDP per capita (current US$)'] = orig

file.close()
file3.close()
