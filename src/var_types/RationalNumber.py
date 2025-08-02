from var_types.BaseAssignmentValue import BaseAssignmentValue
from environment.Environment import Environment
from typing import Union, Tuple, List

class RationalNumber(BaseAssignmentValue):
    """Gère les nombres rationnels"""
    def __init__(self, name: str, value: Union[str, float], environment: Environment) -> None:
        super().__init__(name, value, environment)
        self.numeric_value = 0.0

    def expand_variables(self, expression: str) -> str:
        """Remplace les variables par leurs valeurs dans l'expression"""
        result = ""
        i = 0
        while i < len(expression):
            if expression[i].isalpha():
                var_name = ""
                while i < len(expression) and (expression[i].isalnum() or expression[i] == '_'):
                    var_name += expression[i]
                    i += 1

                if var_name.lower() != 'i':  # 'i' est réservé pour les nombres complexes
                    var = self.environment.get_variable(var_name)
                    if var:
                        if isinstance(var, RationalNumber):
                            result += str(var.numeric_value)
                        else:
                            result += str(var.value)
                    else:
                        result += var_name
                else:
                    result += var_name
                i -= 1
            else:
                result += expression[i]
            i += 1
        return result

    def evaluate_expression(self, expression: str) -> float:
        """Évalue une expression mathématique"""
        try:
            expanded = self.expand_variables(expression)
            expanded = expanded.replace('^', '**')  # Puissance
            expanded = expanded.replace('%', ' % ')  # Modulo

            return eval(expanded)
        except Exception as e:
            raise ValueError(f"Cannot evaluate expression: {expression}")

    def compute(self):
        """Calcule la valeur du nombre rationnel"""
        if isinstance(self.value, str):
            if self.value == "?":
                try:
                    result = self.evaluate_expression(self.name)
                    print(f"{result}")
                    return result
                except Exception:
                    print("Syntax Error")
                    return None
            else:
                try:
                    self.numeric_value = self.evaluate_expression(self.value)
                    self.environment.set_variable(self)
                    return self.numeric_value
                except Exception:
                    print("Syntax Error")
                    return None
        else:
            self.numeric_value = float(self.value)
            return self.numeric_value

    def __str__(self):
        if self.numeric_value == int(self.numeric_value):
            return str(int(self.numeric_value))
        return str(self.numeric_value)