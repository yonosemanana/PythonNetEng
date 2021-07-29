
a = input("Enter the first number (a): ")
b = input("Enter the second number (b): ")

class MyCustomException(Exception): pass

# a = 100
# b = 0

#c = a / b
try:
    try:
        a = float(a)
        b = float(b)
        c = a / b
        print(c)
    except ZeroDivisionError:
        print("You can't divide by 0!")
        raise MyCustomException('Something happened! ')
    except ValueError:
        print("Enter numbers only!")
    else:
        print("This line is printed only when no exception raised!")
    finally:
        print("This line is printed anyway!")
except MyCustomException:
    print("Catch MyCustomException.")