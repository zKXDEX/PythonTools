from colorama import init, Fore, Back, Style

def main():
    print(f"{Fore.GREEN} Welcome to the calculator program! {Style.RESET_ALL}")

    first_number = input("Enter the first number: ")
    second_number = input("Enter the second number: ")

    print(f"{Fore.GREEN} What operation would you like to perform? {Style.RESET_ALL}")
    print(f"{Fore.GREEN} 1. Addition {Style.RESET_ALL}")
    print(f"{Fore.GREEN} 2. Subtraction {Style.RESET_ALL}")
    print(f"{Fore.GREEN} 3. Multiplication {Style.RESET_ALL}")
    print(f"{Fore.GREEN} 4. Division {Style.RESET_ALL}")

    operation = input("Select an operation: ")

    try:
        first_number = float(first_number)
        second_number = float(second_number)
        operation = int(operation)

        integer = None

        if is_integer(first_number) and is_integer(second_number):
            first_number = int(first_number)
            second_number = int(second_number)
            integer = True
        else:
            integer = False


        if operation == 1:
            calculate(first_number, second_number, "addition", integer_result=integer)
        elif operation == 2:
           calculate(first_number, second_number, "subtraction", integer_result=integer)
        elif operation == 3:
           calculate(first_number, second_number, "multiplication", integer_result=integer)
        elif operation == 4:
            if second_number == 0:
                print(f"{Fore.RED} Division by zero is not allowed! {Style.RESET_ALL}")
            else:
                calculate(first_number, second_number, "division", integer_result=integer)
        else:
            print(f"{Fore.RED} Invalid operation! {Style.RESET_ALL}")
    except ValueError:
        print(f"{Fore.RED} Invalid input! {Style.RESET_ALL}")

def calculate(first_number, second_number, operation, integer_result=False):
    if operation == "addition":
        result = first_number + second_number
    elif operation == "subtraction":
        result = first_number - second_number
    elif operation == "multiplication":
        result = first_number * second_number
    elif operation == "division":
        result = first_number / second_number
    else:
        print(f"{Fore.RED} Invalid input! {Style.RESET_ALL}")
        return
    
    print_result(first_number, second_number, result, operation, integer_result)
    
def is_integer(number):
    return int(number) == number

def print_result(first_number, second_number, result, operation, integer_result=False):

    operations = { "addition": "+", "subtraction": "-", "multiplication": "*", "division": "/"}

    if operation in operations:
        symbol = operations[operation]

    if integer_result:
        print(f"{Fore.GREEN} {first_number} {symbol} {second_number} = {result} {Style.RESET_ALL}")
    else:
        print(f"{Fore.GREEN} {first_number} {symbol} {second_number} = {result} {Style.RESET_ALL}")

if __name__ == "__main__":
    main()