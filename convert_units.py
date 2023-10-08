from colorama import Fore, Style


conversion = {
    'm': {'km': 0.001, 'cm': 100, 'mm': 1000},
    'g': {'kg': 0.001, 'mg': 1000}
}

def calculate_units():
    user_input = input("Enter the value and unit (e.g., 1.5g): ")

    number = ''
    unit = ''
    is_decimal = False
    try:
        for char in user_input:
            if char.isdigit():
                
                number += char
            elif char == ".":
                if is_decimal:
                   
                    break
                number += char
                is_decimal = True
            else:
                unit += char

        if is_decimal:
            number = float(number)
        else:
            number = int(number)

        output_unit = input("Ingresa la unidad a la que deseas convertir: ")

        unity_value = None
       

        if unit in conversion:
            unity_value = unit
        else:
            for key in conversion:
                if unit in conversion[key]:
                    unity_value = key
                    number /= conversion[key][unit] 
                    break

        if unity_value is None:
            print(f"{Fore.RED} Invalid unit! {Style.RESET_ALL}")
            return

        if output_unit in conversion[unity_value]:
            number *= conversion[unity_value][output_unit]
            print(f"{Fore.GREEN} {number} {output_unit} {Style.RESET_ALL}")
        else:
            print(f"{Fore.RED} Invalid unit! {Style.RESET_ALL}")
            return

    except ValueError:
        print(f"{Fore.RED} Invalid input! {Style.RESET_ALL}")
        return
    
if __name__ == '__main__':
    calculate_units()
    