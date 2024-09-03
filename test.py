import re

class ComplexParser:
    def __init__(self):
        self.real_part = 0
        self.imaginary_part = 0

    def parse(self, value):
        # Supprimer les espaces pour faciliter le parsing
        value = value.replace(" ", "")
        
        # Expression régulière pour capturer les parties réelles et imaginaires
        complex_regex = re.compile(r'([+-]?\d*\.?\d*\*?i?)')
        
        # Trouver toutes les parties de l'expression
        matches = complex_regex.findall(value)
        print("Matches:", matches)
        
        for term in matches:
            if term == '' or term == '+' or term == '-':
                continue  # Ignorer les termes vides ou simples signes sans chiffres

            if 'i' in term:
                # Si la partie contient 'i', c'est une partie imaginaire
                imag_term = term.replace('*', '').replace('i', '')
                if imag_term == '' or imag_term == '+':
                    imag_term = '1'
                elif imag_term == '-':
                    imag_term = '-1'
                self.imaginary_part += eval(imag_term)
            else:
                # Sinon, c'est une partie réelle
                self.real_part += eval(term)
        
        print("Imaginary part:", self.imaginary_part)
        print("Real part:", self.real_part)
        return complex(self.real_part, self.imaginary_part)

# Exemple d'utilisation
parser = ComplexParser()
expressions = [
    "-3 * i + 9",
    "5i + 6",
    "3i",
    "i",
    "-9i + (5 * 8)",
    "(5 + 3)i + 14/2"
]

for expr in expressions:
    result = parser.parse(expr)
    print(f"{expr} => {result}")
