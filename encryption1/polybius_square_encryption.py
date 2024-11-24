from abc import ABC, abstractmethod
import random
import math

class Cipher(ABC):
    @abstractmethod
    def encrypt(self, text):
        pass

    @abstractmethod
    def decrypt(self, text):
        pass

    def process_file(self, input_file, output_file, mode='encrypt'):
        with open(input_file, 'r') as f:
            content = f.read()

        if mode == 'encrypt':
            processed_content = self.encrypt(content)
        elif mode == 'decrypt':
            processed_content = self.decrypt(content)
        else:
            raise ValueError("Mode should be either 'encrypt' or 'decrypt'.")

        with open(output_file, 'w') as f:
            f.write(processed_content)

class PolybiusSquareCipher(Cipher):
    def __init__(self, alphabet):
        self.alphabet = alphabet.upper()
        self.square_size = math.ceil(math.sqrt(len(self.alphabet)))
        self._validate_alphabet()
        self.square = self._generate_random_square()

    def _validate_alphabet(self):
        if len(set(self.alphabet)) != len(self.alphabet):
            raise ValueError("Alphabet must contain unique characters.")

    def _generate_random_square(self):
        shuffled_alphabet = list(self.alphabet)
        random.shuffle(shuffled_alphabet)
        square = []
        index = 0
        for i in range(self.square_size):
            row = []
            for j in range(self.square_size):
                if index < len(shuffled_alphabet):
                    row.append(shuffled_alphabet[index])
                    index += 1
                else:
                    row.append('')
            square.append(row)
        return square

    def encrypt(self, text):
        text = text.upper()
        encrypted_text = ''
        for char in text:
            if char in self.alphabet:
                for i, row in enumerate(self.square):
                    if char in row:
                        j = row.index(char)
                        encrypted_text += str(i + 1) + str(j + 1)
        return encrypted_text

    def decrypt(self, code):
        decrypted_text = ''
        if len(code) % 2 != 0:
            raise ValueError("The code length must be even.")

        for i in range(0, len(code), 2):
            row, col = int(code[i]) - 1, int(code[i + 1]) - 1
            if 0 <= row < self.square_size and 0 <= col < self.square_size:
                decrypted_text += self.square[row][col]
        return decrypted_text

en_alph = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
rus_alph = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЪЫЭЮЯ'
rus_alph_extended = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЪЫЭЮЯ— :;\n'
cipher = PolybiusSquareCipher(alphabet=rus_alph_extended)

cipher.process_file('input.txt', 'encrypted.txt', mode='encrypt')

cipher.process_file('encrypted.txt', 'decrypted.txt', mode='decrypt')