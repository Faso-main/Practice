"""
Code snippet: dictionary basics
"""

dict_snippet={itr:f'str{itr}' for itr in range(1,6,1)}
print(f'Target_dict: {dict_snippet}')

# GET 
print(dict_snippet[1]) # обычный доступ

# безопасный доступ : выдаст None, если не найдено, без ошибки
print(dict_snippet.get(111)) 
print(dict_snippet.get(111,'Сообщение об ошибке')) 

if 1 in dict_snippet: print(dict_snippet[1]) # проверка на ключ

# получение значений 
print(f'Keys: {dict_snippet.keys()}\nValues: {dict_snippet.values()}\nItems: {dict_snippet.items()}')

# UPDATE
dict_snippet[7]='str7'
dict_snippet[2]='str2222'
print(f'Target_dict: {dict_snippet}')

# Групповое изменение
dict_snippet.update({1:'str11111',2:'str22222'})
print(f'Target_dict: {dict_snippet}')

del dict_snippet[1]
print(f'Target_dict: {dict_snippet}')

dict_snippet.popitem() # удаление последенего
print(f'Target_dict: {dict_snippet}')

dict_snippet.clear() # очистка
print(f'Target_dict: {dict_snippet}')




