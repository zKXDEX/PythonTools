import random
from colorama import Fore, Style

def main():
    MIN_NUMBER = 1
    MAX_NUMBER = 10

    random_number = random.randint(MIN_NUMBER, MAX_NUMBER)
    number = None

    print(f"{Fore.GREEN} Welcome to the Guessing Game! {Style.RESET_ALL}")

    while True:

        number = input("Guess a number between 1 and 10: ")

        try:
            number = int(number)
        except ValueError:
            print("Invalid input. Please enter a number.")

        if number < MIN_NUMBER or number > MAX_NUMBER:
            print(f"Invalid input. Please enter a number between {MIN_NUMBER} and {MAX_NUMBER}.")
            continue

        if number == random_number:
            print(f"{Fore.GREEN} You guessed it! {Style.RESET_ALL}")
            break
        if (number > random_number):
            print("Too high!")
        else:
            print("Too low!")

if __name__ == "__main__":
    main()

