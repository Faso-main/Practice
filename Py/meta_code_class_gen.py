"""
Code snippet: dinamic class generation(Метапрограммирование)
"""

def make_class(**kwargs):
    return type("DynamicClass", (), kwargs)

MyClass = make_class(x=10, y=20, greet=lambda self: f"x={self.x}, y={self.y}")
obj = MyClass()
print(obj.greet())  