"""
Проверить, является ли число палиндромом (читается одинаково слева направо и справа налево).
"""

def isPalindrome(x):
    if x < 0:
        return False
    return str(x) == str(x)[::-1]


print(isPalindrome(121))  # True
print(isPalindrome(-121)) # False