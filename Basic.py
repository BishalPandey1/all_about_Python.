# Base class
class Device:
    def __init__(self, brand, power_source):
        self.brand = brand
        self.power_source = power_source

    def turn_on(self):
        print(f"{self.brand} device is now ON using {self.power_source}.")

    def turn_off(self):
        print(f"{self.brand} device is now OFF.")

# Derived class: Smartphone
class Smartphone(Device):
    def __init__(self, brand, power_source, os):
        super().__init__(brand, power_source)
        self.os = os

    def turn_on(self):
        print(f"{self.brand} smartphone running {self.os} is now ON.")

# Derived class: Laptop
class Laptop(Device):
    def __init__(self, brand, power_source, ram):
        super().__init__(brand, power_source)
        self.ram = ram

    def turn_on(self):
        print(f"{self.brand} laptop with {self.ram}GB RAM is now booting up.")
# Usage
phone = Smartphone("Samsung", "Battery", "Android")
laptop = Laptop("Dell", "Charger", 16)
phone.turn_on()
phone.turn_off()
laptop.turn_on()
laptop.turn_off()
