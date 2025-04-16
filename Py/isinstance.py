""" isinstance(object, type) """

array_list=[itr for itr in range(1,11,1)] # array [1 to 10]

print(type(array_list)) # get the type of the entity

print(isinstance(array_list,list)) # isinstance in action

array_str=str(array_list) # changing the type of the entity

print(f'Changed: {isinstance(array_str,str)}') # isinstance in action