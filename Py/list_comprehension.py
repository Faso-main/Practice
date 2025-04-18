"""
List comprehension offers a shorter syntax when you want 
to create a new list based on the values of an existing list.
"""

array_num_original=[1,2,3,4,5] # original number array [1 to 5]
array_num_lc=[itr for itr in range(1,6,1)] # ls nu,ber array [1 to 5]

if array_num_lc == array_num_original: print(True) # array validation 

array_num_lc_rules=[itr for itr in range(1,6,1) if itr %2] # [1 to 5 if itr %2]

print(f'Updated with rules: {array_num_lc_rules}')
