def simple_interest(p, r, t):
  si = (p * r * t) / 100
  return si

p = float(input("Enter the principal amount: "))
r = float(input("Enter the rate of interest: "))
t = float(input("Enter the time period: "))

si = simple_interest(p, r, t)

print("The simple interest is:", si)
