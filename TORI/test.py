def sum_keys(d):
    if not isinstance(d,dict):
        return 0
    else:
        return len(d) + sum(sum_keys(v) for v in d.items())

#https://stackoverflow.com/questions/35427814/get-the-number-of-all-keys-in-a-dictionary-of-dictionaries-in-python
#https://stackoverflow.com/questions/20444340/iter-values-item-in-dictionary-does-not-work
    

decay_chain={}

decay_chain['K-40']={"Ar-40":{"He-4":{"H-2":{}}},"Ca-40":{"Mg-20":{"Al-22":{}}}}

print(sum_keys(decay_chain))

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

