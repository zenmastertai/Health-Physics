from collections import abc

def sum_keys(d):
    for k,v in d.items():
        print(v)     
        sum_keys(v)

def set(d, key, value):
    dd = d
    keys = key.split('.')
    latest = keys.pop()
    for k in keys:
        dd = dd.setdefault(k, {})
    dd.setdefault(latest, value)

decay_chain={}

decay_chain['K-40']={"Ar-40":{"He-4":{"H-2":{}},"Ls-65":{"Kc-45":{}}},
                     "Ca-40":{"Mg-20":{"Al-22":{}}},
                    }

set(decay_chain,'K-40.Ar-40.He-4.H-2.As-40',{})
set(decay_chain,'K-40.Ca-40.Mg-20.Al-22.Pb-82',{})
print(decay_chain)
sum_keys(decay_chain)



##sum_keys(decay_chain)

{'K-40':
 {'Ar-40':
  {'He-4': {'H-2': {'As-40': {}}},
   'Ls-65': {'Kc-45': {}}},
  'Ca-40': {'Mg-20': {'Al-22': {'Pb-82': {}}}}}}

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

   # Function used to translate user input and search decay chain
    # ----------------------------------------------------
    # def decay_search(self ,event=None ,isotope_input=None):
    #     isotope, parent_A = self.search(self, isotope_input)
    #     parent_isotope = isotope+'-'+parent_A
    #     self.dc = {}
    #
    #     self.gen_list = [[parent_isotope]]
    #     self.dc_list = []
    #     self.decay_chain_get(1)
    #     for line in self.gen_list:
    #         print(line)

    # def decay_chain_get(self,gen_num):
    #     x = 1
    #     #cycle through each generation to determine which generation is the current one
    #     for g in self.gen_list:
    #         if x == gen_num:
    #             generation = g
    #         else:
    #             x+=1
    #
    #     tmp = []
    #
    #     #for every isotope in the current generation,
    #     #calculate each daughter product
    #     for iso in generation:
    #         #break down isotope into isotope and A components
    #         for i in range(len(iso)):
    #             if iso[i] == '-':
    #                 isotope = iso[0:i]
    #                 A = iso.replace(isotope+'-',"")
    #                 break
    #
    #         ref = self.translate_isotope(isotope,A) #get referenc id for isotope
    #
    #         branch_list = self.decay_mode_get(ref) #get all branching ratios in a list for that isotope
    #
    #         #if the isotope isn't stable, caclulate daughter
    #         if len(branch_list)>0:
    #             for branch in branch_list: #loop through all branching ratios
    #                 decay_modes = self.decay_mode_split(branch) #split all decay modes up into a list in order for single branch
    #                 new_i,new_A = self.decay_mode_translate(decay_modes,ref,A) #calculate daughter from parent for each branch
    #                 new_isotope = new_i+'-'+new_A
    #
    #                 tmp.append(new_isotope)
    #     #if the branch ends, stop recursion
    #     #if the branch keeps going, go deeper
    #     if len(tmp)>0:
    #         self.gen_list.append(tmp)
    #         self.decay_chain_get(x+1)
    #
    # def set(key, value):
    #     keys = key.split('.')
    #     latest = keys.pop()
    #     for k in keys:
    #         self.dc = self.dc.setdefault(k, {})
    #     self.dc.setdefault(latest, value)
    #
    # def decay_mode_get(self,ref=None):
    #     decay_mode_list=[]
    #     try:
    #         for i in range(int(len(self.parents2[ref])/2)):
    #             decay_mode_list.append(self.parents2[ref]['mode'+str(i+1)])
    #     except KeyError:
    #         pass
    #     return decay_mode_list
    #
    # def decay_mode_split(self,branch=None):
    #     tmp_list = []
    #     count = 1
    #     while len(branch) > 0:
    #         x = branch[:count]
    #         try:
    #             if branch[:count+1] == 'EC+':
    #                 x = branch[:count+3]
    #                 tmp_list.append(x)
    #                 branch = branch.replace(x,"")
    #                 count = 1
    #             elif x in decay_types:
    #                 tmp_list.append(x)
    #                 branch = branch.replace(x,"")
    #                 count = 1
    #             else:
    #                 count+=1
    #         except IndexError:
    #             pass
    #     return tmp_list
    #
    # def decay_mode_translate(self,modes=None,ref=None,A=None):
    #
    #     Z = int(ref.replace(ref[-4:],""))
    #     A = int(A)
    #
    #     for mode in modes:
    #         if mode == 'B-':
    #             Z = Z + 1
    #         elif mode == 'B+':
    #             Z = Z - 1
    #         elif mode == 'EC':
    #             Z = Z - 1
    #         elif mode == 'EC+':
    #             Z = Z - 1
    #         elif mode == 'EC+B+':
    #             Z = Z - 1
    #         elif mode == 'A' or mode == '2A':
    #             Z = Z - 2
    #             A = A - 4
    #         elif mode == '3A':
    #             Z = Z - 4
    #             Z = Z - 8
    #         elif mode == 'N':
    #             A = A - 1
    #         elif mode == '2N':
    #             A = A - 2
    #         elif mode == '3N':
    #             A = A - 3
    #         elif mode == 'P':
    #             Z = Z - 1
    #             A = A - 1
    #         elif mode == '2P':
    #             Z = Z - 2
    #             A = A - 2
    #         elif mode == 'IT':
    #             A = A - 300
    #         elif mode == 'D':
    #             Z = Z - 1
    #             A = A - 1
    #         elif mode == 'T':
    #             Z = Z - 1
    #             A = A - 3
    #
    #     isotope = nuclides_rev[Z]
    #     return isotope,str(A)
