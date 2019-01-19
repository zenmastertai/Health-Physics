from collections import abc

def sum_keys(d):
    for k,v in d.items():
        print(v)     
        sum_keys(v)

def get_nested(data, k):
    if k and data:
        element  = k[0]
        if element:
            value = data.get(element)
            return value if len(k) == 1 else get_nested(value, k[1:])

decay_chain={}

decay_chain['K-40']={"Ar-40":{"He-4":{"H-2":{}}},
                     "Ca-40":{"Mg-20":{"Al-22":{}}},
                    }
k = ["K-40","Ar-40"]
print(get_nested(decay_chain,k))
print(decay_chain[k])

##sum_keys(decay_chain)



##decay_chain = lambda: defaultdict(decay_chain)
##mydict = decay_chain()
##mydict = mydict['K-40'] = {"Ar-40":{"He-4":{"H-2":{}}},
##                     "Ca-40":{"Mg-20":{"Al-22":{}}},
##                    }
##print(mydict)
##for line in mydict:
##    path = line.split('/')
##    print(line)
##    for i in range(len(path)-1):
##        print(mydict[path[i]])
##        print(i)


##    if path[-1] != '':
##        d = mydict
##
##        for i in range(len(path) -1):
##            d = d[path[i]]
##        d[path[-1]] = 'file'





#https://stackoverflow.com/questions/37357976/best-practice-to-recursively-update-a-nested-dictionary



##for k,v in decay_chain.items():
##    print(k)
##    for i,j in v.items():
##        print(i)
##        print(j)


##for p_id, p_info in decay_chain.items():
##    print("\nPerson ID:", p_id)
##    
##    for key in p_info:
##        print(key + ':', p_info[key])

##for k1,v1 in decay_chain.items():
##    print(v1)
##
##i= len(decay_chain)+ sum(len(v) for v in decay_chain.items())
##print(i)

