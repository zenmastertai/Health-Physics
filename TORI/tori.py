from isoref import *
import pickle
from operator import itemgetter, attrgetter

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

##for i in range(len(isotope_data["data"])):
##    if isotope_data["data"][i]["name"] == "Li":
##        print(isotope_data["data"][i]["ref"])

gamma_db = {"data":[]}
for i in range(len(isotope_data["data"])):
    gdb = {}
    gdb[isotope_data["data"][i]["ref"]]=[{}]
    gamma_db["data"].append(gdb)

print(len(gamma_db["data"]))

##gamma_db['30011'][0]['gamma1']=123
##print(gamma_db['30011'][0]['gamma1'])

gamma_data = import_radiation_data('gammas.txt')

testdata = gamma_data[0:20]
testdata.sort(key=lambda gamma: gamma[1], reverse=False)

for i in range(len(testdata)):
    count = 1
    #print(testdata[i][0])
    #print(gamma_db['30011'][0])
    if 'gamma'+str(count) in gamma_db[testdata[i][0]][0]:
        count+=1
    else:
        gamma_db[testdata[i]][0]['gamma'+str(count)]=testdata[i][1]

#print(gamma_db['120031'])


##print(gamma_db['120031'][0])

##for i in range(len(testdata)):
##    print(testdata[i])
    

#print(isotope_data['data'][0])

