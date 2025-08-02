import re
from typing import Optional
from environment.Environment import Environment
from var_types.BaseAssignmentValue import BaseAssignmentValue
from var_types.Function import Function
from var_types.Matrix import Matrix
from var_types.ComplexNumber import ComplexNumber
from var_types.RationalNumber import RationalNumber

class Parser:
    """Parse les entrées utilisateur et détermine le type"""
    def __init__(self, environment: Environment):
        self.environment = environment

    def identify_type(self, input_str: str) -> Optional[BaseAssignmentValue]:
        """Identifie le type de l'expression et crée l'objet approprié"""
        parts = input_str.split('=', 1)
        if len(parts) != 2:
            return None
        
        left_part = parts[0].strip()
        right_part = parts[1].strip()

        if re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*\s*\([^)]*\)$', left_part):
            return Function(left_part, right_part, self.environment)
        
        if re.match(r'^\[.*\]$', right_part):
            return Matrix(left_part, right_part, self.environment)
        
        if 'i' in right_part or right_part == "?":
            temp_right = right_part.replace('i', '')
            if re.search(r'[a-zA-Z]', temp_right):
                if 'i' in right_part:
                    return ComplexNumber(left_part, right_part, self.environment)
            else:
                if 'i' in right_part:
                    return ComplexNumber(left_part, right_part, self.environment)
        
        func_call_match = re.match(r'^([a-zA-Z_][a-zA-Z0-9_]*)\s*\(\s*([^)]*)\s*\)$', left_part)
        if func_call_match and right_part == "?":
            func_name = func_call_match.group(1)
            arg_expr = func_call_match.group(2)
            
            func = self.environment.get_variable(func_name)
            if func and isinstance(func, Function):
                try:
                    arg_value = eval(arg_expr.replace('^', '**'))
                    result = func.evaluate(arg_value)
                    print(f"{result}")
                    return None
                except Exception:
                    print("Syntax Error")
                    return None
        
        return RationalNumber(left_part, right_part, self.environment)

    def preprocess(self, input_str: str) -> Optional[str]:
        """Préprocesse l'entrée utilisateur"""
        input_str = input_str.strip()
        
        if not input_str:
            return None
        
        if input_str.count('=') != 1:
            return None
        
        parts = input_str.split('=')
        if not parts[0].strip() or not parts[1].strip():
            return None
        
        return input_str
