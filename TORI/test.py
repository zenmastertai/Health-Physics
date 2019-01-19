from collections import *

def sum_keys(d):
    for k,v in d.items():
        print(k)
                   
        sum_keys(v)

def update(d, u):
    for k, v in u.items():
        if isinstance(v, collections.Mapping):
            d[k] = update(d.get(k, {}), v)
        else:
            d[k] = v
    return d

    

decay_chain={}

decay_chain['K-40']={"Ar-40":{"He-4":{"H-2":{}}},
                     "Ca-40":{"Mg-20":{"Al-22":{}}},
                    }






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

#sum_keys(decay_chain)

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

