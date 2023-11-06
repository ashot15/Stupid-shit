import time as t


try:
    Number1 = int(input("First Number: "))
    Number2 = int(input("Second Number: "))
    char = input("Character: ")

    if char == "+":
        Result = Number1 + Number2
    elif char == "*":
        Result = Number1 * Number2
    elif char == "/":
        Result = Number1 / Number2
    elif char == "-":
        Result = Number1 - Number2
    else:
        Result = "Invalid operator"

    print (Result)
except ValueError:
    print("Please write numbers")

t.sleep(1.5)
exit()
