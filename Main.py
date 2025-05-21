"""
" Welcome to the world of misery and anguish - Python practice dir!! " 
"""

hashmap_str = (lambda parts: (parts[0][:6], parts[1].strip('!')))(['Python!!!!Python!!!!', 'Python!!!!'])
print(f'Result: {" is ".join(map(str, hashmap_str))}')