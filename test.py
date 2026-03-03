def add_instance_count(cls):
    counter = 0
    
    def get_count(self):
        return counter  # Could access self.__class__.__dict__['counter']
    
    def increment_count(self):
        nonlocal counter
        counter += 1
        return counter
    
    cls.instance_count = property(get_count)
    cls.increment = increment_count  # Add increment method
    cls._counter = counter           # Store counter in class
    return cls

@add_instance_count
class MyClass:
    def __init__(self, name):
        self.name = name
        MyClass.increment()  # Increment on create

obj1 = MyClass("first")
obj2 = MyClass("second")

print(f"{obj1.instance_count=}")  # 2
print(f"{obj2.instance_count=}")  # 2  
print(f"{MyClass.instance_count=}") # 2
