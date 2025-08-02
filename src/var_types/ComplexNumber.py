from var_types.BaseAssignmentValue import BaseAssignmentValue
from environment.Environment import Environment
from typing import Tuple, List
import var_types.RationalNumber as RationalNumber
import re

class ComplexNumber(BaseAssignmentValue):
    """Gère les nombres complexes"""
    def __init__(self, name: str, value: str, environment: Environment) -> None:
        super().__init__(name, value, environment)
        self.real_part = 0.0
        self.imaginary_part = 0.0

    def expand_variables(self, expression: str) -> str:
        """Remplace les variables par leurs valeurs dans l'expression"""
        result = ""
        i = 0
        while i < len(expression):
            if expression[i].isalpha() and expression[i] != 'i':
                var_name = ""
                while i < len(expression) and (expression[i].isalnum() or expression[i] == '_'):
                    var_name += expression[i]
                    i += 1

                var = self.environment.get_variable(var_name)
                if var:
                    if isinstance(var, RationalNumber):
                        result += str(var.numeric_value)
                    elif isinstance(var, ComplexNumber):
                        if var.real_part != 0 or var.imaginary_part == 0:
                            result += str(var.real_part)
                        if var.imaginary_part != 0:
                            if var.real_part != 0 and var.imaginary_part > 0:
                                result += "+"
                            result += str(var.imaginary_part) + "i"
                    else:
                        result += str(var.value)
                else:
                    result += var_name
                i -= 1
            else:
                result += expression[i]
            i += 1
        return result

    def parse_complex(self, expression: str) -> Tuple[float, float]:
        """Parse une expression complexe et retourne (partie_réelle, partie_imaginaire)"""
        expression = expression.replace(" ", "")

        real_part = 0.0
        imaginary_part = 0.0

        expression = expression.replace('^', '**')

        terms = re.findall(r'[+-]?[^+-]+', expression)
        if not terms and expression:
            terms = [expression]

        for term in terms:
            term = term.strip()
            if not term:
                continue

            if 'i' in term:
                coeff = term.replace('i', '').replace('*', '')
                if coeff == '' or coeff == '+':
                    coeff = '1'
                elif coeff == '-':
                    coeff = '-1'

                try:
                    imaginary_part += eval(coeff)
                except:
                    imaginary_part += float(coeff) if coeff else 1.0
            else:
                try:
                    real_part += eval(term)
                except:
                    real_part += float(term)

        return real_part, imaginary_part

    def compute(self):
        """Calcule la valeur du nombre complexe"""
        if isinstance(self.value, str):
            if self.value == "?":
                try:
                    expanded = self.expand_variables(self.name)
                    self.real_part, self.imaginary_part = self.parse_complex(expanded)
                    print(f"{self}")
                    return self
                except Exception:
                    print("Syntax Error")
                    return None
            else:
                try:
                    expanded = self.expand_variables(self.value)
                    self.real_part, self.imaginary_part = self.parse_complex(expanded)
                    self.environment.set_variable(self)
                    return self
                except Exception:
                    print("Syntax Error")
                    return None

    def __str__(self):
        if self.real_part == 0 and self.imaginary_part == 0:
            return "0"
        elif self.real_part == 0:
            if self.imaginary_part == 1:
                return "i"
            elif self.imaginary_part == -1:
                return "-i"
            else:
                return f"{self.imaginary_part}i"
        elif self.imaginary_part == 0:
            return str(self.real_part)
        else:
            real_str = str(self.real_part)
            if self.imaginary_part == 1:
                return f"{real_str} + i"
            elif self.imaginary_part == -1:
                return f"{real_str} - i"
            elif self.imaginary_part > 0:
                return f"{real_str} + {self.imaginary_part}i"
            else:
                return f"{real_str} - {abs(self.imaginary_part)}i"
