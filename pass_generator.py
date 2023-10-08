import pyperclip
import random
import string
from colorama import Fore, Back, Style

def generatorPassword(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

def main():
    try:
        password = generatorPassword()
        print(f"Your password is: {Fore.GREEN} {password} {Style.RESET_ALL}")
        pyperclip.copy(password)
        print(f"{Fore.GREEN} The password has been copied to the clipboard! {Style.RESET_ALL}")
        Wait = input("Press enter to continue...")
    except ValueError:
        print(f"{Fore.RED} Invalid input! {Style.RESET_ALL}")
        return
    
    
if __name__ == "__main__":
    main()