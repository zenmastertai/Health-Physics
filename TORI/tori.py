from isoref import *
import pickle
from operator import itemgetter, attrgetter
import sys

def import_radiation_data(filename):
    data = []
    file = open(filename)
    for line in file:
        tmp_data = []
        line = line.split(',')
        tmp_data.append(line[0])
        tmp_data.append(float(line[2]))
        tmp_data.append(line[4])
        tmp_data.append(line[6].strip('\n'))
        data.append(tmp_data)
    file.close()
    return data

with open('parents.pickle', 'rb') as handle:
    isotope_data = pickle.load(handle)

gamma_db = {"data":[]}
for i in range(len(isotope_data["data"])):
    gdb = {}
    gdb[isotope_data["data"][i]["ref"]]=[{}]
    gamma_db["data"].append(gdb)

gamma_data = import_radiation_data('gammas.txt')
gamma_data.sort(key=lambda gamma: gamma[1], reverse=False)

for i in range(len(gamma_data)):
    count = 1
    for j in range(len(gamma_db["data"])):
        try:
            if 'gamma'+str(count) in gamma_db["data"][j][gamma_data[i][0]][0]:
                count+=1
            else:
                gamma_db["data"][j][gamma_data[i][0]][0]['gamma'+str(count)] = gamma_data[i][1]
                gamma_db["data"][j][gamma_data[i][0]][0]['I'+str(count)] = gamma_data[i][2]
        except KeyError:
            pass

with open('gamma.pickle', 'wb') as handle:
    pickle.dump(gamma_db, handle, protocol=pickle.HIGHEST_PROTOCOL)




