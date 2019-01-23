import pickle
from operator import itemgetter, attrgetter
import sys

filename = 'x-rays.txt'

data = []
file = open(filename)
for line in file:
    tmp_data = []
    line = line.split(',')
    tmp_data.append(line[0])
    tmp_data.append(float(line[2]))
    x = line[3].split(" ")
    x[2] = x[2].strip('"')
    x[2] = x[2].replace('<sub>','')
    x[2] = x[2].replace('</sub>','')
    tmp_data.append(x[2])
    data.append(tmp_data)
file.close()

xray_db = {}

for line in data:
    xray_db[line[0]] = {}

for line in data:
        count = 1
        test = False
        while test == False:
            try:
                if 'xray'+str(count) in xray_db[line[0]]:
                    count+=1
                else:
                    xray_db[line[0]]['xray'+str(count)] = line[1]
                    xray_db[line[0]]['level'+str(count)] = line[2]
                    test = True
            except KeyError:
                pass  

with open('xray.pickle', 'wb') as handle:
    pickle.dump(xray_db, handle, protocol=pickle.HIGHEST_PROTOCOL)




