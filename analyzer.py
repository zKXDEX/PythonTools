from collections import Counter
from colorama import Fore, Back, Style
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import fnmatch
import json
import time
import os
import random
import re

def main():
    print(f"{Fore.GREEN} Welcome to the text analyzer! {Style.RESET_ALL}")
    input_next = input("Press enter to continue... ")
    print(f"{Fore.GREEN} What would you like to do? {Style.RESET_ALL} \n 1. Analyze text \n 2. Analyze File  \n 3. Graph \n 4. Exit")
    options = input(f"{Fore.GREEN} Select an option: {Style.RESET_ALL}")
    if options.isdigit():
        options = int(options)
        if options == 1:
                analyze_text()
        elif options == 2:
            analyze_file()
        elif options == 3:
            analizer_graph()
        elif options == 4:
            exit()
        else:
            print(f"{Fore.RED} Invalid input! {Style.RESET_ALL}")
            return
    else:
        print(f"{Fore.RED} Please enter a number! {Style.RESET_ALL}")
   
def analyze_text(word_count=5):
    input_text = input("Enter the text to analyze: ")
    
    clean_text = re.sub(r'\W+', ' ', input_text).lower()
    words = clean_text.split()
    word_count = Counter(words)
    char_count = Counter(clean_text.replace(" ", ""))
    half_lenght = sum(len(word) for word in words) / len(words)
    longest_word = max(words, key=len)
    shortest_word = min(words, key=len)
    num_sentences = input_text.count('.') + input_text.count('!') + input_text.count('?')
    num_paragraphs = input_text.count('\n\n') + 1

    common_words = word_count.most_common(10)

    print(f"Total de palabras: {len(words)}")
    print(f"Recuento de palabras: {word_count}")
    print(f"Recuento de caracteres: {char_count}")
    print(f"Longitud promedio de palabra: {half_lenght}")
    print(f"Palabra más larga: {longest_word}")
    print(f"Palabra más corta: {shortest_word}")
    print(f"Número de oraciones: {num_sentences}")
    print(f"Número de párrafos: {num_paragraphs}")

    results = {
        "total_words": len(words),
        "word_count": word_count,
        "char_count": char_count,
        "half_lenght": half_lenght,
        "longest_word": longest_word,
        "shortest_word": shortest_word,
        "num_sentences": num_sentences,
        "num_paragraphs": num_paragraphs,
        "common_words": common_words
    }

    try:
        with open('analizer/result_text.json', 'r') as f:
            if f.read():
                f.seek(0)
                data = json.load(f)
            else:
                data = {}
    except FileNotFoundError:
        data = {}

    identifier = f'data_{str(int(time.time()))}{random.randint(1, 999)}{len(words)}'


    data[identifier] = results

    with open('analizer/result_text.json', 'w') as f:
        json.dump(data, f, indent=4)



def analyze_file():
    imput_file = input("Enter the path to the file to analyze: ")

    if not os.path.isfile(imput_file):
        print(f"{Fore.RED} The path is not valid! {Style.RESET_ALL}")
        return
    
    with open(imput_file, 'r') as f:
        imput_file = f.read()
    
    clean_text = re.sub(r'\W+', ' ', imput_file).lower()
    words = clean_text.split()
    word_count = Counter(words)
    char_count = Counter(clean_text.replace(" ", ""))
    half_lenght = sum(len(word) for word in words) / len(words)
    longest_word = max(words, key=len)
    shortest_word = min(words, key=len)
    num_sentences = imput_file.count('.') + imput_file.count('!') + imput_file.count('?')
    num_paragraphs = imput_file.count('\n\n') + 1

    common_words = word_count.most_common(10)

    print(f"Total de palabras: {len(words)}")
    print(f"Recuento de palabras: {word_count}")
    print(f"Recuento de caracteres: {char_count}")
    print(f"Longitud promedio de palabra: {half_lenght}")
    print(f"Palabra más larga: {longest_word}")
    print(f"Palabra más corta: {shortest_word}")
    print(f"Número de oraciones: {num_sentences}")
    print(f"Número de párrafos: {num_paragraphs}")

    results = {
        "total_words": len(words),
        "word_count": word_count,
        "char_count": char_count,
        "half_lenght": half_lenght,
        "longest_word": longest_word,
        "shortest_word": shortest_word,
        "num_sentences": num_sentences,
        "num_paragraphs": num_paragraphs,
        "common_words": common_words
    }

    try:
        with open('analizer/result_file.json', 'r') as f:
            if f.read():
                f.seek(0)
                data = json.load(f)
            else:
                data = {}
    except FileNotFoundError:
        data = {}

    identifier = f'data_{str(int(time.time()))}{random.randint(1, 999)}{len(words)}'


    data[identifier] = results

    with open('analizer/result_file.json', 'w') as f:
        json.dump(data, f, indent=4)

def analizer_graph():

    directory = r'D:\User\repos\python\tools\analizer'
    all_files = os.listdir(directory)
    json_files = [file for file in all_files if file.endswith('.json')]

    print("Files: ")
    for i, file in enumerate(json_files):
        print(f"{i + 1}. {file}")

    file_number = int(input("Seleccione el número del archivo que desea analizar: "))
    selected_file = json_files[file_number - 1]

    with open(os.path.join(directory, selected_file)) as f:
        data = json.load(f)

    for identifier, results in data.items():
        print(f"Analizer: {identifier}")
        common_words = results['common_words']
        words, counts = zip(*common_words)

        df = pd.DataFrame({'word': words, 'count': counts})
        df.sort_values('count', ascending=False, inplace=True)

        df.plot.bar(x='word', y='count', legend=False)
        plt.title(f'Top 10 most common words in {identifier}')
        plt.ylabel('Frequency')
        plt.show()

if __name__ == '__main__':
    main()