from isoref import *
import pickle
from operator import itemgetter, attrgetter
import sys

#import radiation data from text file into list
def import_radiation_data(radiation,filename):

    if radiation == "gamma":
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
    elif radiation == "beta":
        data = []
        file = open(filename)
        for line in file:
            tmp_data = []
            line = line.split(',')
            tmp_data.append(line[0])
            tmp_data.append(float(line[2]))
            tmp_data.append(line[3])
            tmp_data.append(line[1].strip('"'))
            data.append(tmp_data)
        file.close()
        return data
    elif radiation == "alpha":
        data = []
        file = open(filename)
        for line in file:
            tmp_data = []
            line = line.split(',')
            tmp_data.append(line[0])
            tmp_data.append(float(line[2]))
            tmp_data.append(line[4])
            data.append(tmp_data)
        file.close()
        return data

def export_db(radiation,filename):
    #import isotope data from dictionary file
    with open('parents.pickle', 'rb') as handle:
        isotope_data = pickle.load(handle)

    #put only isotope reference #'s into a dictionary
    radiation_db = {}
    for isotope in isotope_data:
        radiation_db[isotope]={}

    #import gamma radiation data and sort
    radiation_data = import_radiation_data(radiation,filename)
    radiation_data.sort(key=lambda radiation: radiation[1], reverse=False)

    #associate every gamma-ray radiation and it's intesnity with it's isotope
    for line in radiation_data:
        count = 1
        test = False
        while test == False:
            try:
                if radiation+str(count) in radiation_db[line[0]]:
                    count+=1
                else:
                    radiation_db[line[0]]['gamma'+str(count)] = line[1]
                    radiation_db[line[0]]['I'+str(count)] = line[2]
                    test = True
            except KeyError:
                pass        
    #export to
    with open(radiation+".pickle", 'wb') as handle:
        pickle.dump(radiation_db, handle, protocol=pickle.HIGHEST_PROTOCOL)

export_db("gamma","gammas.txt")
export_db("beta","betas.txt")
export_db("alpha","alphas.txt")



