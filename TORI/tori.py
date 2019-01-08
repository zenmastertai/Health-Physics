from isoref import *

def import_data(filename):
    data = []
    file = open(filename)
    for line in file:
        tmp_data = []
        line = line.split(',')
        tmp_data.append(line[0])
        tmp_data.append(line[2])
        tmp_data.append(line[4])
        tmp_data.append(line[6].strip('\n'))
        data.append(tmp_data)
    file.close()
    return data

gamma_data = import_data('gammas.txt')
print(gamma_data[0])

