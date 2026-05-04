# 1. Create a list
tech_stack = ["Python", "C#", "Flutter"]

# 2. Add items to the list
tech_stack.append("JavaScript")  # Adds to the end
tech_stack.insert(1, "SQL")      # Adds at a specific index (1)

# 3. Remove an element from the list
tech_stack.remove("C#")          # Removes by value
# tech_stack.pop(0)              # Alternative: Removes by index (0)

# 4. Display list items
print("Current list items:")
for item in tech_stack:
    print(f"- {item}")