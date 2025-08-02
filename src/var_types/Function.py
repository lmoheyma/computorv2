from var_types.BaseAssignmentValue import BaseAssignmentValue
from environment.Environment import Environment
from typing import Tuple, List
import re

class Function(BaseAssignmentValue):
    """Gère les fonctions"""
    def __init__(self, name: str, value: str, environment: Environment) -> None:
        super().__init__(name, value, environment)
        self.function_name = ""
        self.variable = ""
        self.expression = ""
        self.parse_function_definition()

    def parse_function_definition(self):
        """Parse la définition de fonction"""
        match = re.match(r'([a-zA-Z_][a-zA-Z0-9_]*)\s*\(\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*\)', self.name)
        if match:
            self.function_name = match.group(1)
            self.variable = match.group(2)
            self.expression = self.value

    def evaluate(self, arg_value: float) -> float:
        """Évalue la fonction pour une valeur donnée"""
        try:
            expr = self.expression.replace(self.variable, str(arg_value))
            expr = expr.replace('^', '**')
            return eval(expr)
        except Exception:
            raise ValueError(f"Cannot evaluate function with argument {arg_value}")

    def compute(self):
        """Stocke la fonction"""
        if self.value == "?":
            var = self.environment.get_variable(self.function_name)
            if var and isinstance(var, Function):
                print(f"{var}")
            else:
                print("Function not found")
            return None
        else:
            self.environment.set_variable(self)
            return self

    def __str__(self):
        return f"{self.expression}"