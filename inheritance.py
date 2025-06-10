# Parent class
class Animal:
    def __init__(self, name):
        self.name = name
    
    def make_sound(self):
        return "Some generic sound"

# Child class inheriting from Animal
class Dog(Animal):
    def make_sound(self):
        return "Bark!"

# Creating objects
generic_animal = Animal("Unknown Animal")
dog = Dog("Buddy")

print(generic_animal.name, "says:", generic_animal.make_sound())
print(dog.name, "says:", dog.make_sound())
