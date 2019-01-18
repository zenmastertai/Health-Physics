from collections import defaultdict

def sum_keys(d):
    for k,v in d.items():
        print(k)
                   
        sum_keys(v)

    
##        return len(d) + sum(sum_keys(v) for v in d.items())

    

decay_chain={}

decay_chain['K-40']={"Ar-40":{"He-4":{"H-2":{}}},
                     "Ca-40":{"Mg-20":{"Al-22":{}}},
                    }

#https://stackoverflow.com/questions/27118687/updating-nested-dictionaries-when-data-has-existing-key/27118776

print(my_dict)
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

