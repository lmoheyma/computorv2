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

        # Expand variables in right_part
        def expand_variables(expr):
            def repl(match):
                var_name = match.group(0)
                var = self.environment.get_variable(var_name)
                if var:
                    return str(var.value)
                return var_name
            return re.sub(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', repl, expr)

        expanded_right = expand_variables(right_part)

        # Ajoute le signe * entre les nombres et les variables dans right_part uniquement pour les fonctions
        def add_stars(expr):
            expr = re.sub(r'(\d)([a-zA-Z_])', r'\1*\2', expr)
            expr = re.sub(r'([a-zA-Z_])(\d)', r'\1*\2', expr)
            return expr

        # Évalue les sous-expressions numériques dans une expression
        def eval_numeric_subexpressions(expr):
            # Fonction utilitaire pour savoir si une sous-expression contient des lettres
            def has_letters(s):
                return re.search(r'[a-zA-Z_]', s) is not None

            # Évalue les parenthèses les plus profondes d'abord
            pattern_paren = re.compile(r'\(([^()]+)\)')
            while True:
                match = pattern_paren.search(expr)
                if not match:
                    break
                subexpr = match.group(1)
                if not has_letters(subexpr):
                    try:
                        val = str(eval(subexpr.replace('^', '**')))
                        expr = expr[:match.start()] + val + expr[match.end():]
                    except Exception:
                        expr = expr[:match.start()] + '(' + subexpr + ')' + expr[match.end():]
                else:
                    expr = expr[:match.start()] + '(' + subexpr + ')' + expr[match.end():]

            # Évalue les opérations simples hors parenthèses
            # Ex: 4 -5 + 2^2 - 4
            # On cherche les séquences de chiffres et opérateurs sans lettres
            pattern_simple = re.compile(r'(?<![a-zA-Z_\d])([+-]?\d+(?:\s*[-+*/%^]\s*\d+)+)(?![a-zA-Z_\d])')
            def repl_simple(m):
                subexpr = m.group(1)
                if not has_letters(subexpr):
                    try:
                        return str(eval(subexpr.replace('^', '**')))
                    except Exception:
                        return subexpr
                return subexpr
            expr = pattern_simple.sub(repl_simple, expr)
            return expr

        # Si right_part est une variable déjà définie
        if re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', right_part):
            var = self.environment.get_variable(right_part)
            if var:
                # Retourne une nouvelle instance du même type
                if isinstance(var, ComplexNumber):
                    return ComplexNumber(left_part, str(var.value), self.environment)
                if isinstance(var, Matrix):
                    return Matrix(left_part, str(var.value), self.environment)
                if isinstance(var, Function):
                    return Function(left_part, str(var.value), self.environment)
                if isinstance(var, RationalNumber):
                    return RationalNumber(left_part, str(var.value), self.environment)

        if re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*\s*\([^)]*\)$', left_part):
            # Ajoute les * sur l'expression brute, puis expand
            right_with_stars = add_stars(right_part)
            expanded_right_func = expand_variables(right_with_stars)
            # Évalue les sous-expressions numériques
            final_expr = eval_numeric_subexpressions(expanded_right_func)
            return Function(left_part, final_expr, self.environment)

        # Les autres cas utilisent expanded_right
        if re.match(r'^\[.*\]$', right_part):
            return Matrix(left_part, expanded_right, self.environment)

        # Si c'est un nombre complexe
        if 'i' in right_part or right_part == "?":
            temp_right = expanded_right.replace('i', '')
            if re.search(r'[a-zA-Z]', temp_right):
                if 'i' in expanded_right:
                    return ComplexNumber(left_part, expanded_right, self.environment)
            else:
                if 'i' in expanded_right:
                    return ComplexNumber(left_part, expanded_right, self.environment)

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

        # Appel de fonction dans l'assignation d'une variable
        func_call_match = re.match(r'^([a-zA-Z_][a-zA-Z0-9_]*)\s*\(\s*([^)]*)\s*\)$', right_part)
        if func_call_match:
            func_name = func_call_match.group(1)
            arg_expr = func_call_match.group(2)
            func = self.environment.get_variable(func_name)
            if func and isinstance(func, Function):
                # Expand variables in arg_expr
                expanded_arg = expand_variables(arg_expr)
                try:
                    arg_value = eval(expanded_arg.replace('^', '**'))
                    result = func.evaluate(arg_value)
                    return RationalNumber(left_part, str(result), self.environment)
                except Exception:
                    return None

        # Si c'est un nombre rationnel, on évalue l'expression
        try:
            value = eval(expanded_right.replace('^', '**'))
        except Exception:
            value = expanded_right
        return RationalNumber(left_part, str(value), self.environment)

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
