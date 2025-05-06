"""
Code snippet example of cash, same task called decorator
"""

integers_array=[itr for itr in range(1,6,1)]
str_array=[str(itr) for itr in range(1,6,1)]
#print(integers_array,str_array)

hashmap_dict={k:v for (k,v) in zip(integers_array,str_array)}
#print(hashmap_dict)

hashmap_dict=dict(zip(integers_array,str_array))
#print(hashmap_dict)

made_by_comprehension_dict={itr: itr**3 for itr in[1,2,3,4,5]}
print(f'Made_by_comprehension_dict: {made_by_comprehension_dict}')

