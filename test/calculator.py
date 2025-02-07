def a(x, y):
    return x + y


def s(x, y):
    return x - y


def m(x, y):
    return x * y


def d(x, y):
    return x / y


def calc():
    while True:
        try:
            n1 = float(input("Enter first number: "))
            n2 = float(input("Enter second number: "))
            op = input("Enter operation (+,-,*,/): ")
            if op == "+":
                r = a(n1, n2)
            elif op == "-":
                r = s(n1, n2)
            elif op == "*":
                r = m(n1, n2)
            elif op == "/":
                r = d(n1, n2)
            else:
                print("Invalid operation")
                continue
            print("Result:", r)
        except Exception as e:
            print(f"Error occurred: {e}")


if __name__ == "__main__":
    calc()
