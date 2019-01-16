import pickle

#import parents data
data = []
file = open('parents2.txt')
for line in file:
    tmp_data = []
    line = line.split(',')
    tmp_data.append(line[0]) #ref
    tmp_data.append(line[1]) #num decay modes
    tmp_data.append(line[4].strip('"')) #decay mode
    tmp_data.append(line[5]) #branching ratio
    data.append(tmp_data)
file.close()

#sort the array by isotope reference
data.sort(key=lambda isotope: isotope[0], reverse=False)


#put all isotope data into dictionary associated with isotope reference
isotope_data = {}
for i in range(len(data)):
    test = False
    while test == False:
        try:
            if data[i][0] in isotope_data:
                test = True
            else:
                isotope_data[data[i][0]]={}
        except KeyError:
            pass

##associate every gamma-ray radiation and it's intesnity with it's isotope
for line in data:
    test = False
    if 'mode'+line[1] not in isotope_data[line[0]]:
        isotope_data[line[0]]['mode'+line[1]] = line[2]
        isotope_data[line[0]]['branch'+line[1]] = line[3]
        
#export dictionary to pickle file
with open('parents2.pickle', 'wb') as handle:
    pickle.dump(isotope_data, handle, protocol=pickle.HIGHEST_PROTOCOL)





    
