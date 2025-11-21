from var_types.BaseAssignmentValue import BaseAssignmentValue
from environment.Environment import Environment
from typing import Tuple, List

class Matrix(BaseAssignmentValue):
    """Gère les matrices"""
    def __init__(self, name: str, value: str, environment: Environment) -> None:
        super().__init__(name, value, environment)
        self.matrix = []
        self.rows = 0
        self.columns = 0

    def parse_matrix(self, matrix_str: str) -> List[List[float]]:
        """Parse une chaîne de caractères représentant une matrice"""
        matrix_str = matrix_str.strip()
        # Retire les crochets extérieurs si présents
        if matrix_str.startswith('[') and matrix_str.endswith(']'):
            matrix_str = matrix_str[1:-1]

        rows = matrix_str.split(';')
        matrix = []

        for row_str in rows:
            row_str = row_str.strip()
            # Retire les crochets de la ligne si présents
            if row_str.startswith('[') and row_str.endswith(']'):
                row_str = row_str[1:-1]

            elements = [float(elem.strip()) for elem in row_str.split(',') if elem.strip()]
            matrix.append(elements)

        return matrix

    def compute(self):
        """Calcule et stocke la matrice"""
        if isinstance(self.value, str):
            if self.value == "?":
                var = self.environment.get_variable(self.name)
                if var and isinstance(var, Matrix):
                    print(f"{var}")
                else:
                    print("Variable not found")
                return None
            else:
                try:
                    self.matrix = self.parse_matrix(self.value)
                    self.rows = len(self.matrix)
                    self.columns = len(self.matrix[0]) if self.matrix else 0
                    self.environment.set_variable(self)
                    return self
                except Exception:
                    print("Syntax Error")
                    return None

    def __str__(self):
        if not self.matrix:
            return "[]"

        result = ""
        for row in self.matrix:
            row_str = " , ".join(str(elem) for elem in row)
            result += f"[ {row_str} ]\n"
        return result.rstrip()