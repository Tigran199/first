from typing import List
import string
from collections import Counter
import os

def get_longest_diverse_words(file_path: str) -> List[str]:
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    
    words = text.split()
    words = [word.strip(string.punctuation) for word in words]
    
    sorted_words = sorted(words, key=lambda x: (-len(set(x)), -len(x)))
    
    return sorted_words[:10]

def get_rarest_char(file_path: str) -> str:
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    
    char_counter = Counter(text)
    
    rarest_char = min(char_counter, key=char_counter.get)
    
    return rarest_char

def count_punctuation_chars(file_path: str) -> int:
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    
    punctuation_count = sum(1 for char in text if char in string.punctuation)
    
    return punctuation_count

def count_non_ascii_chars(file_path: str) -> int:
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    
    non_ascii_count = sum(1 for char in text if ord(char) > 127)
    
    return non_ascii_count

def get_most_common_non_ascii_char(file_path: str) -> str:
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    
    non_ascii_chars = [char for char in text if ord(char) > 127]
    
    if not non_ascii_chars:
        return None  # или return "Нет не-ASCII символов"
    
    most_common_non_ascii_char = Counter(non_ascii_chars).most_common(1)[0][0]
    
    return most_common_non_ascii_char

file_path = '1/data.txt'
print("10 самых длинных слов с наибольшим количеством уникальных символов:", get_longest_diverse_words(file_path))
print("Самый редкий символ:", get_rarest_char(file_path))
print("Количество знаков препинания:", count_punctuation_chars(file_path))
print("Количество не-ASCII символов:", count_non_ascii_chars(file_path))
print("Самый распространенный не-ASCII символ:", get_most_common_non_ascii_char(file_path))
