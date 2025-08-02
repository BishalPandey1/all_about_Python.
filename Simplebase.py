# Variables and Data Types
name = "Alice"
age = 25
height = 5.6
is_student = True

print("Name:", name)
print("Age:", age)
print("Height:", height)
print("Is Student?", is_student)

# Conditional Statements
if age >= 18:
    print("You are an adult.")
else:
    print("You are a minor.")

# Loops
for i in range(5):
    print("Iteration:", i)

num = 0
while num < 3:
    print("Number:", num)
    num += 1

# Functions
def greet(person):
    return f"Hello, {person}!"

print(greet(name))

# File Handling
with open("sample.txt", "w") as file:
    file.write("Hello, this is a sample file.\n")
    file.write("Python makes file handling easy!")

# Reading the file
with open("sample.txt", "r") as file:
    content = file.read()
    print("File Content:\n", content)
