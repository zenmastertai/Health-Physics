#initialize lists
data_array = []
energy = []
attenuation = []

#open file and extract data
fin = open('PbMassAttenData.txt')
for line in fin:
    data_array.append(line)
fin.close()

#extract data to lists
for i in range(len(data_array)):
    e, a = list(map(str, data_array[i].split(",")))
    energy.append(e)
    attenuation.append(a)
