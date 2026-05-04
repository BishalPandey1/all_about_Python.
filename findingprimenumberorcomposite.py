num = int(input("Enter a number: "))

if num > 1:
    for i in range(2, num):
        if num % i == 0:
            print(num, "is a Composite number")
            break
    else:
        print(num, "is a Prime number")
else:
    print(num, "is neither Prime nor Composite")
