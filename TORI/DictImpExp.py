import pickle

data = []
file = open('parents.txt')
for line in file:
    tmp_data = []
    line = line.split(',')
    tmp_data.append(line[0])
    tmp_data.append(line[1])
    tmp_data.append(line[2].strip('"'))
    tmp_data.append(line[3])
    line[7] = line[7].strip('"')
    line[7] = line[7].replace('&nbsp;','')
    t = ''
    for i in range(len(line[7])):
        if line[7][i] != '<':
            t = t + line[7][i]
        else:
            break
    tmp_data.append(t)
    tmp_data.append(line[9])
    data.append(tmp_data)
file.close()

isotope_data = { "data":[]}
for i in range(len(data)):
    isotope = {}
    isotope["A"] = data[i][0]
    isotope["Z"] = data[i][1]
    isotope["name"] = data[i][2]
    isotope["ref"] = data[i][3]
    isotope["halflife"] = data[i][4]
    isotope["abund"] = data[i][5]
    isotope_data["data"].append(isotope)
