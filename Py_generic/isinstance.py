""" isinstance(object, type) 
object	Required. An object.
type	A type or a class, or a tuple of types and/or classes
"""

array_list=[itr for itr in range(1,11,1)] # array [1 to 10]

print(type(array_list)) # get the type of the entity

print(isinstance(array_list,list)) # isinstance in action

array_str=str(array_list) # changing the type of the entity

print(f'Changed: {isinstance(array_str,str)}') # isinstance in action


def is_unicode(s):
  if isinstance(s, str):
    return True
  return False