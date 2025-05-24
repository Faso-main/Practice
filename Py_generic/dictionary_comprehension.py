"""
Code snippet: dictionary comprehension
"""

integers_array=[itr for itr in range(1,6,1)]
str_array=[str(itr) for itr in range(1,6,1)]
#print(integers_array,str_array)

dict_snippet1={k:v for (k,v) in zip(integers_array,str_array)}
#print(dict_snippet1)

dict_snippet2=dict(zip(integers_array,str_array))
#print(dict_snippet2)

made_by_comprehension_dict={itr: itr**3 for itr in[1,2,3,4,5]}
#print(f'Made_by_comprehension_dict: {made_by_comprehension_dict}')

conditional_statements_dict={itr:str(itr) for itr in range(1,6,1) if itr**3 % 4 == 0}
#print(f'conditional_statements_dict: {conditional_statements_dict}')

hashmap='str1'
nested_dict_snippet={
    itr:{x: itr+x for x in hashmap} for itr in hashmap
}
print(f'nested_dict_snippet: {nested_dict_snippet}')
