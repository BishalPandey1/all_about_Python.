class Addition:
    def __init__(self, num1, num2):
        self.num1 = num1
        self.num2 = num2

    def add_numbers(self):
        return self.num1 + self.num2

obj = Addition(10, 20)

result = obj.add_numbers()
print("The sum is:", result)



