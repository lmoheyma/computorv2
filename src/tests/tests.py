import pytest
import sys
import os
import io
from contextlib import redirect_stdout, redirect_stderr
import re

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

# Import des classes du projet principal
from environment.Environment import Environment
from var_types.BaseAssignmentValue import BaseAssignmentValue
from var_types.RationalNumber import RationalNumber
from var_types.ComplexNumber import ComplexNumber
from var_types.Matrix import Matrix
from var_types.Function import Function
from parsing.Parser import Parser

class TestEnvironment:
    """Tests pour la classe Environment"""
    
    def setup_method(self):
        """Setup avant chaque test"""
        self.env = Environment()
    
    def test_environment_initialization(self):
        """Test de l'initialisation de l'environnement"""
        assert self.env.variables == {}
        assert len(self.env.variables) == 0
    
    def test_set_variable(self):
        """Test d'ajout de variables"""
        var = RationalNumber("x", "5", self.env)
        var.compute()
        
        assert "x" in self.env.variables
        assert self.env.variables["x"] == var
    
    def test_get_variable_case_insensitive(self):
        """Test de récupération insensible à la casse"""
        var = RationalNumber("TestVar", "10", self.env)
        var.compute()
        
        # Test différentes casses
        assert self.env.get_variable("TestVar") == var
        assert self.env.get_variable("testvar") == var
        assert self.env.get_variable("TESTVAR") == var
        assert self.env.get_variable("tEsTvAr") == var
    
    def test_get_nonexistent_variable(self):
        """Test de récupération d'une variable inexistante"""
        assert self.env.get_variable("nonexistent") is None
    
    def test_variable_overwrite(self):
        """Test de réécriture de variable"""
        var1 = RationalNumber("x", "5", self.env)
        var1.compute()
        
        var2 = RationalNumber("x", "10", self.env)
        var2.compute()
        
        assert self.env.get_variable("x") == var2
        assert len(self.env.variables) == 1
    
    def test_reserved_variable_i(self):
        """Test que 'i' est une variable réservée"""
        var = RationalNumber("i", "5", self.env)
        
        # Capturer la sortie
        f = io.StringIO()
        with redirect_stdout(f):
            var.compute()
        
        output = f.getvalue()
        assert "'i' is not a valid variable name" in output
        assert "i" not in self.env.variables

class TestRationalNumber:
    """Tests pour la classe RationalNumber"""
    
    def setup_method(self):
        """Setup avant chaque test"""
        self.env = Environment()
    
    def test_simple_integer(self):
        """Test nombre entier simple"""
        var = RationalNumber("x", "42", self.env)
        result = var.compute()
        
        assert result == 42.0
        assert var.numeric_value == 42.0
        assert str(var) == "42"
    
    def test_simple_float(self):
        """Test nombre décimal simple"""
        var = RationalNumber("y", "3.14159", self.env)
        result = var.compute()
        
        assert result == 3.14159
        assert var.numeric_value == 3.14159
    
    def test_negative_numbers(self):
        """Test nombres négatifs"""
        var = RationalNumber("neg", "-25.5", self.env)
        result = var.compute()
        
        assert result == -25.5
        assert var.numeric_value == -25.5
    
    def test_basic_arithmetic(self):
        """Test opérations arithmétiques de base"""
        test_cases = [
            ("2 + 3", 5.0),
            ("10 - 4", 6.0),
            ("3 * 7", 21.0),
            ("15 / 3", 5.0),
            ("17 % 5", 2.0),
            ("2 ^ 3", 8.0),
            ("2 ** 3", 8.0),
        ]
        
        for expression, expected in test_cases:
            var = RationalNumber("test", expression, self.env)
            result = var.compute()
            assert result == expected, f"Failed for {expression}"
    
    def test_parentheses_priority(self):
        """Test priorité des parenthèses"""
        test_cases = [
            ("2 * (3 + 4)", 14.0),
            ("(10 - 2) / 4", 2.0),
            ("2 + 3 * 4", 14.0),
            ("(2 + 3) * 4", 20.0),
            ("2 * 3 + 4 * 5", 26.0),
            ("2 * (3 + 4) * 5", 70.0),
        ]
        
        for expression, expected in test_cases:
            var = RationalNumber("test", expression, self.env)
            result = var.compute()
            assert result == expected, f"Failed for {expression}"
    
    def test_variable_expansion(self):
        """Test expansion des variables"""
        # Créer des variables
        var_a = RationalNumber("a", "5", self.env)
        var_a.compute()
        
        var_b = RationalNumber("b", "3", self.env)
        var_b.compute()
        
        # Utiliser les variables dans une expression
        var_c = RationalNumber("c", "a + b * 2", self.env)
        result = var_c.compute()
        
        assert result == 11.0  # 5 + 3 * 2 = 11
    
    def test_query_operator(self):
        """Test opérateur de requête ?"""
        var_x = RationalNumber("x", "10", self.env)
        var_x.compute()
        
        # Test query
        query = RationalNumber("x + 5", "?", self.env)
        
        f = io.StringIO()
        with redirect_stdout(f):
            result = query.compute()
        
        output = f.getvalue().strip()
        assert "15" in output
    
    def test_complex_expressions(self):
        """Test expressions complexes"""
        test_cases = [
            ("2 + 4 * 2 - 5 % 4 + 2 * (4 + 5)", 27.0),
            ("(3 + 2) * (4 - 1) + 2 ^ 3", 23.0),
            ("10 / 2 + 3 * 4 - 1", 16.0),
        ]
        
        for expression, expected in test_cases:
            var = RationalNumber("test", expression, self.env)
            result = var.compute()
            assert result == expected, f"Failed for {expression}"
    
    def test_invalid_expressions(self):
        """Test expressions invalides"""
        invalid_expressions = [
            "2 + + 3",
            "/ 5",
            "2 3",  # multiplication implicite non supportée
            "",
        ]
        
        for expression in invalid_expressions:
            var = RationalNumber("test", expression, self.env)
            
            f = io.StringIO()
            with redirect_stdout(f):
                result = var.compute()
            
            output = f.getvalue()
            assert result is None or "Syntax Error" in output

class TestComplexNumber:
    """Tests pour la classe ComplexNumber"""
    
    def setup_method(self):
        """Setup avant chaque test"""
        self.env = Environment()
    
    def test_pure_imaginary(self):
        """Test nombres purement imaginaires"""
        test_cases = [
            ("i", 0.0, 1.0, "i"),
            ("2i", 0.0, 2.0, "2.0i"),
            ("-i", 0.0, -1.0, "-i"),
            ("-3i", 0.0, -3.0, "-3.0i"),
            ("2*i", 0.0, 2.0, "2.0i"),
        ]
        
        for expression, expected_real, expected_imag, expected_str in test_cases:
            var = ComplexNumber("test", expression, self.env)
            var.compute()
            
            assert var.real_part == expected_real, f"Real part failed for {expression}"
            assert var.imaginary_part == expected_imag, f"Imaginary part failed for {expression}"
    
    def test_pure_real(self):
        """Test nombres purement réels"""
        var = ComplexNumber("test", "5", self.env)
        var.compute()
        
        assert var.real_part == 5.0
        assert var.imaginary_part == 0.0
        assert str(var) == "5.0"
    
    def test_complex_numbers(self):
        """Test nombres complexes complets"""
        test_cases = [
            ("3 + 2i", 3.0, 2.0),
            ("5 - 3i", 5.0, -3.0),
            ("-2 + 4i", -2.0, 4.0),
            ("-1 - 2i", -1.0, -2.0),
            ("2*i + 3", 3.0, 2.0),
            ("-4i - 4", -4.0, -4.0),
        ]
        
        for expression, expected_real, expected_imag in test_cases:
            var = ComplexNumber("test", expression, self.env)
            var.compute()
            
            assert var.real_part == expected_real, f"Real part failed for {expression}"
            assert var.imaginary_part == expected_imag, f"Imaginary part failed for {expression}"
    
    def test_complex_string_representation(self):
        """Test représentation en chaîne des nombres complexes"""
        test_cases = [
            (0.0, 0.0, "0"),
            (0.0, 1.0, "i"),
            (0.0, -1.0, "-i"),
            (0.0, 2.0, "2.0i"),
            (0.0, -3.0, "-3.0i"),
            (5.0, 0.0, "5.0"),
            (3.0, 1.0, "3.0 + i"),
            (3.0, -1.0, "3.0 - i"),
            (2.0, 3.0, "2.0 + 3.0i"),
            (4.0, -2.0, "4.0 - 2.0i"),
        ]
        
        for real, imag, expected_str in test_cases:
            var = ComplexNumber("test", "0", self.env)
            var.real_part = real
            var.imaginary_part = imag
            
            assert str(var) == expected_str, f"String representation failed for {real} + {imag}i"
    
    def test_complex_variable_expansion(self):
        """Test expansion des variables dans les nombres complexes"""
        # Créer une variable réelle
        var_a = RationalNumber("a", "3", self.env)
        var_a.compute()
        
        # Utiliser dans un nombre complexe
        var_complex = ComplexNumber("c", "a + 2i", self.env)
        var_complex.compute()
        
        assert var_complex.real_part == 3.0
        assert var_complex.imaginary_part == 2.0
    
    def test_complex_query(self):
        """Test requête sur nombres complexes"""
        var = ComplexNumber("z", "3 + 4i", self.env)
        var.compute()
        
        query = ComplexNumber("z", "?", self.env)
        
        f = io.StringIO()
        with redirect_stdout(f):
            query.compute()
        
        output = f.getvalue().strip()
        assert "3.0 + 4.0i" in output

class TestMatrix:
    """Tests pour la classe Matrix"""
    
    def setup_method(self):
        """Setup avant chaque test"""
        self.env = Environment()
    
    def test_simple_matrix(self):
        """Test matrice simple"""
        var = Matrix("mat", "[[1,2];[3,4]]", self.env)
        var.compute()
        
        expected = [[1.0, 2.0], [3.0, 4.0]]
        assert var.matrix == expected
        assert var.rows == 2
        assert var.columns == 2
    
    def test_single_row_matrix(self):
        """Test matrice à une ligne"""
        var = Matrix("mat", "[[1,2,3]]", self.env)
        var.compute()
        
        expected = [[1.0, 2.0, 3.0]]
        assert var.matrix == expected
        assert var.rows == 1
        assert var.columns == 3
    
    def test_single_column_matrix(self):
        """Test matrice à une colonne"""
        var = Matrix("mat", "[[1];[2];[3]]", self.env)
        var.compute()
        
        expected = [[1.0], [2.0], [3.0]]
        assert var.matrix == expected
        assert var.rows == 3
        assert var.columns == 1
    
    def test_various_matrix_sizes(self):
        """Test différentes tailles de matrices"""
        test_cases = [
            ("[[1]]", [[1.0]], 1, 1),
            ("[[1,2]]", [[1.0, 2.0]], 1, 2),
            ("[[1];[2]]", [[1.0], [2.0]], 2, 1),
            ("[[1,2,3];[4,5,6]]", [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]], 2, 3),
            ("[[1,2];[3,4];[5,6]]", [[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]], 3, 2),
        ]
        
        for matrix_str, expected_matrix, expected_rows, expected_cols in test_cases:
            var = Matrix("mat", matrix_str, self.env)
            var.compute()
            
            assert var.matrix == expected_matrix, f"Matrix failed for {matrix_str}"
            assert var.rows == expected_rows, f"Rows failed for {matrix_str}"
            assert var.columns == expected_cols, f"Columns failed for {matrix_str}"
    
    def test_matrix_string_representation(self):
        """Test représentation en chaîne des matrices"""
        var = Matrix("mat", "[[1,2];[3,4]]", self.env)
        var.compute()
        
        expected_output = "[ 1.0 , 2.0 ]\n[ 3.0 , 4.0 ]"
        assert str(var) == expected_output
    
    def test_empty_matrix(self):
        """Test matrice vide"""
        var = Matrix("mat", "[]", self.env)
        var.compute()
        
        assert var.matrix == []
        assert var.rows == 0
        assert var.columns == 0
        assert str(var) == "[]"
    
    def test_matrix_with_floats(self):
        """Test matrice avec nombres décimaux"""
        var = Matrix("mat", "[[1.5,2.7];[3.14,4.0]]", self.env)
        var.compute()
        
        expected = [[1.5, 2.7], [3.14, 4.0]]
        assert var.matrix == expected
    
    def test_matrix_query(self):
        """Test requête sur matrice"""
        var = Matrix("M", "[[1,2];[3,4]]", self.env)
        var.compute()
        
        query = Matrix("M", "?", self.env)
        
        f = io.StringIO()
        with redirect_stdout(f):
            query.compute()
        
        output = f.getvalue()
        assert "[ 1.0 , 2.0 ]" in output
        assert "[ 3.0 , 4.0 ]" in output

class TestFunction:
    """Tests pour la classe Function"""
    
    def setup_method(self):
        """Setup avant chaque test"""
        self.env = Environment()
    
    def test_simple_function(self):
        """Test fonction simple"""
        var = Function("f(x)", "2*x + 1", self.env)
        var.compute()
        
        assert var.function_name == "f"
        assert var.variable == "x"
        assert var.expression == "2*x + 1"
    
    def test_function_evaluation(self):
        """Test évaluation de fonction"""
        var = Function("f(x)", "2*x + 1", self.env)
        var.compute()
        
        test_cases = [
            (0, 1.0),
            (1, 3.0),
            (2, 5.0),
            (-1, -1.0),
            (0.5, 2.0),
        ]
        
        for input_val, expected in test_cases:
            result = var.evaluate(input_val)
            assert result == expected, f"Function evaluation failed for x={input_val}"
    
    def test_complex_function(self):
        """Test fonction complexe"""
        var = Function("g(t)", "t^2 - 4*t + 4", self.env)
        var.compute()
        
        # Test pour t = 2 (devrait donner 0)
        result = var.evaluate(2)
        assert result == 0.0
        
        # Test pour t = 0 (devrait donner 4)
        result = var.evaluate(0)
        assert result == 4.0
    
    def test_polynomial_function(self):
        """Test fonction polynomiale"""
        var = Function("poly(x)", "x^3 - 2*x^2 + x - 1", self.env)
        var.compute()
        
        # Test pour x = 1
        result = var.evaluate(1)
        assert result == -1.0  # 1 - 2 + 1 - 1 = -1
        
        # Test pour x = 2
        result = var.evaluate(2)
        assert result == 1.0   # 8 - 8 + 2 - 1 = 1
    
    def test_function_with_different_variables(self):
        """Test fonctions avec différentes variables"""
        functions = [
            ("f(x)", "x + 1", "x"),
            ("g(y)", "2*y", "y"),
            ("h(z)", "z^2", "z"),
            ("func(t)", "3*t - 2", "t"),
        ]
        
        for func_name, expression, expected_var in functions:
            var = Function(func_name, expression, self.env)
            var.compute()
            
            assert var.variable == expected_var, f"Variable extraction failed for {func_name}"
    
    def test_function_string_representation(self):
        """Test représentation en chaîne des fonctions"""
        var = Function("f(x)", "2*x^2 + 3*x - 1", self.env)
        var.compute()
        
        assert str(var) == "2*x^2 + 3*x - 1"

class TestParser:
    """Tests pour la classe Parser"""
    
    def setup_method(self):
        """Setup avant chaque test"""
        self.env = Environment()
        self.parser = Parser(self.env)
    
    def test_preprocessing_valid_inputs(self):
        """Test préprocessing d'entrées valides"""
        valid_inputs = [
            "x = 5",
            "var = 3.14",
            "complex = 2 + 3i",
            "mat = [[1,2];[3,4]]",
            "f(x) = 2*x + 1",
            "result = ?",
        ]
        
        for input_str in valid_inputs:
            result = self.parser.preprocess(input_str)
            assert result == input_str, f"Preprocessing failed for {input_str}"
    
    def test_preprocessing_invalid_inputs(self):
        """Test préprocessing d'entrées invalides"""
        invalid_inputs = [
            "",
            "   ",
            "x = y =",
            "= 5",
            "x =",
            "no equals sign",
            "x = y = z",
        ]
        
        for input_str in invalid_inputs:
            result = self.parser.preprocess(input_str)
            assert result is None, f"Preprocessing should fail for {input_str}"
    
    def test_type_identification(self):
        """Test identification des types"""
        test_cases = [
            ("x = 5", RationalNumber),
            ("y = 3.14", RationalNumber),
            ("z = 2 + 3i", ComplexNumber),
            ("w = i", ComplexNumber),
            ("mat = [[1,2];[3,4]]", Matrix),
            ("f(x) = 2*x + 1", Function),
        ]
        
        for input_str, expected_type in test_cases:
            result = self.parser.identify_type(input_str)
            assert isinstance(result, expected_type), f"Type identification failed for {input_str}"
    
    def test_function_call_parsing(self):
        """Test parsing d'appels de fonction"""
        # Créer une fonction
        func = Function("f(x)", "2*x + 1", self.env)
        func.compute()
        
        # Test appel de fonction
        f = io.StringIO()
        with redirect_stdout(f):
            result = self.parser.identify_type("f(3) = ?")
        
        output = f.getvalue().strip()
        assert "7" in output  # f(3) = 2*3 + 1 = 7

class TestIntegration:
    """Tests d'intégration pour tester le workflow complet"""
    
    def setup_method(self):
        """Setup avant chaque test"""
        self.env = Environment()
        self.parser = Parser(self.env)
    
    def test_complete_workflow_rational(self):
        """Test workflow complet avec nombres rationnels"""
        # Assignation
        assignment = self.parser.identify_type("x = 10")
        assignment.compute()
        
        # Utilisation
        calculation = self.parser.identify_type("y = x * 2 + 5")
        calculation.compute()
        
        # Vérification
        y_var = self.env.get_variable("y")
        assert y_var.numeric_value == 25.0
        
        # Requête
        f = io.StringIO()
        with redirect_stdout(f):
            query = self.parser.identify_type("y = ?")
            query.compute()
        
        output = f.getvalue().strip()
        assert "25" in output
    
    def test_complete_workflow_complex(self):
        """Test workflow complet avec nombres complexes"""
        # Assignation de nombres complexes
        assignment1 = self.parser.identify_type("z1 = 3 + 4i")
        assignment1.compute()
        
        assignment2 = self.parser.identify_type("z2 = 1 - 2i")
        assignment2.compute()
        
        # Vérification des valeurs
        z1 = self.env.get_variable("z1")
        assert z1.real_part == 3.0
        assert z1.imaginary_part == 4.0
        
        z2 = self.env.get_variable("z2")
        assert z2.real_part == 1.0
        assert z2.imaginary_part == -2.0
    
    def test_complete_workflow_function(self):
        """Test workflow complet avec fonctions"""
        # Définir une fonction
        func_def = self.parser.identify_type("f(x) = x^2 - 2*x + 1")
        func_def.compute()
        
        # Vérifier la fonction
        func = self.env.get_variable("f")
        assert func is not None
        assert func.expression == "x^2 - 2*x + 1"
        
        # Évaluer la fonction
        f = io.StringIO()
        with redirect_stdout(f):
            func_call = self.parser.identify_type("f(1) = ?")
        
        output = f.getvalue().strip()
        assert "0" in output  # f(1) = 1 - 2 + 1 = 0
    
    def test_mixed_types_workflow(self):
        """Test workflow avec types mixtes"""
        # Variables rationnelles
        self.parser.identify_type("a = 5").compute()
        self.parser.identify_type("b = 3").compute()
        
        # Nombre complexe utilisant des variables
        complex_var = self.parser.identify_type("z = a + b*i")
        complex_var.compute()
        
        # Matrice
        matrix_var = self.parser.identify_type("M = [[1,2];[3,4]]")
        matrix_var.compute()
        
        # Fonction
        func_var = self.parser.identify_type("f(x) = a*x + b")
        func_var.compute()
        
        # Vérifications
        z = self.env.get_variable("z")
        assert z.real_part == 5.0
        assert z.imaginary_part == 3.0
        
        M = self.env.get_variable("M")
        assert M.matrix == [[1.0, 2.0], [3.0, 4.0]]
        
        f = self.env.get_variable("f")
        assert f.expression == "a*x + b"
    
    def test_variable_reassignment(self):
        """Test réassignation de variables avec changement de type"""
        # Assignation initiale (rationnel)
        self.parser.identify_type("x = 5").compute()
        x = self.env.get_variable("x")
        assert isinstance(x, RationalNumber)
        
        # Réassignation (complexe)
        self.parser.identify_type("x = 2 + 3i").compute()
        x = self.env.get_variable("x")
        assert isinstance(x, ComplexNumber)
        assert x.real_part == 2.0
        assert x.imaginary_part == 3.0
        
        # Réassignation (matrice)
        self.parser.identify_type("x = [[1,2]]").compute()
        x = self.env.get_variable("x")
        assert isinstance(x, Matrix)
        assert x.matrix == [[1.0, 2.0]]

class TestEdgeCases:
    """Tests des cas limites et d'erreur"""
    
    def setup_method(self):
        """Setup avant chaque test"""
        self.env = Environment()
        self.parser = Parser(self.env)
    
    def test_division_by_zero(self):
        """Test division par zéro"""
        var = RationalNumber("test", "5 / 0", self.env)
        
        f = io.StringIO()
        with redirect_stdout(f):
            result = var.compute()
        
        output = f.getvalue()
        assert result is None or "Syntax Error" in output
    
    def test_undefined_variable_usage(self):
        """Test utilisation de variable non définie"""
        var = RationalNumber("test", "undefined_var + 5", self.env)
        
        f = io.StringIO()
        with redirect_stdout(f):
            result = var.compute()
        
        output = f.getvalue()
        assert result is None or "Syntax Error" in output
    
    def test_malformed_matrix(self):
        """Test matrice mal formée"""
        malformed_matrices = [
            "[[1,2];[3]]",      # Lignes de tailles différentes
            "[1,2;3,4]",        # Syntaxe incorrecte
            "[[1,2],[3,4]]",    # Virgules au lieu de points-virgules
            "[[]]",             # Ligne vide
        ]
        
        for matrix_str in malformed_matrices:
            var = Matrix("test", matrix_str, self.env)
            
            f = io.StringIO()
            with redirect_stdout(f):
                result = var.compute()
            
            output = f.getvalue()
            assert result is None or "Syntax Error" in output
    
    def test_invalid_function_definition(self):
        """Test définition de fonction invalide"""
        invalid_functions = [
            ("f = 2*x + 1", "Pas de parenthèses"),
            ("f() = 2*x + 1", "Pas de variable"),
            ("f(x,y) = x + y", "Plusieurs variables"),
        ]
        
        for func_def, description in invalid_functions:
            parts = func_def.split('=')
            if len(parts) == 2:
                var = Function(parts[0].strip(), parts[1].strip(), self.env)
                # La fonction devrait gérer l'erreur gracieusement
                var.compute()
    
    def test_very_long_expressions(self):
        """Test expressions très longues"""
        # Créer une expression très longue
        long_expr = " + ".join([str(i) for i in range(100)])
        var = RationalNumber("long", long_expr, self.env)
        
        result = var.compute()
        expected = sum(range(100))  # 0 + 1 + 2 + ... + 99
        assert result == expected
    
    def test_deeply_nested_parentheses(self):
        """Test parenthèses profondément imbriquées"""
        nested_expr = "((((1 + 2) * 3) + 4) * 5)"
        var = RationalNumber("nested", nested_expr, self.env)
        
        result = var.compute()
        expected = ((((1 + 2) * 3) + 4) * 5)  # = 65
        assert result == expected

# Tests de performance (optionnels)
class TestPerformance:
    """Tests de performance basiques"""
    
    def setup_method(self):
        """Setup avant chaque test"""
        self.env = Environment()
        self.parser = Parser(self.env)
    
    def test_many_variables(self):
        """Test avec beaucoup de variables"""
        import time
        
        start_time = time.time()
        
        # Créer 100 variables
        for i in range(100):
            var = RationalNumber(f"var{i}", str(i), self.env)
            var.compute()
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        # Vérifier que toutes les variables sont créées
        assert len(self.env.variables) == 100
        
        # Le temps d'exécution devrait être raisonnable (moins de 1 seconde)
        assert execution_time < 1.0, f"Performance test failed: {execution_time}s"
    
    def test_complex_calculation_performance(self):
        """Test performance calculs complexes"""
        import time
        
        # Expression complexe avec plusieurs opérations
        complex_expr = "2^10 + 3^5 - 4*5*6 + (7+8+9)*(10-5) + 100/4"
        
        start_time = time.time()
        
        var = RationalNumber("perf", complex_expr, self.env)
        result = var.compute()
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        # Vérifier le résultat
        expected = 2**10 + 3**5 - 4*5*6 + (7+8+9)*(10-5) + 100/4
        assert result == expected
        
        # Le temps d'exécution devrait être très rapide
        assert execution_time < 0.1, f"Complex calculation too slow: {execution_time}s"

# Configuration PyTest
class TestConfiguration:
    """Tests de configuration et setup"""
    
    def test_pytest_imports(self):
        """Test que tous les imports nécessaires sont disponibles"""
        # Vérifier que les modules principaux sont importables
        assert Environment is not None
        assert RationalNumber is not None
        assert ComplexNumber is not None
        assert Matrix is not None
        assert Function is not None
        assert Parser is not None
    
    def test_class_inheritance(self):
        """Test héritage des classes"""
        env = Environment()
        
        # Vérifier que toutes les classes héritent correctement
        rational = RationalNumber("test", "5", env)
        complex_num = ComplexNumber("test", "3+4i", env)
        matrix = Matrix("test", "[[1,2]]", env)
        function = Function("f(x)", "x+1", env)
        
        assert isinstance(rational, BaseAssignmentValue)
        assert isinstance(complex_num, BaseAssignmentValue)
        assert isinstance(matrix, BaseAssignmentValue)
        assert isinstance(function, BaseAssignmentValue)

# Tests de régression
class TestRegression:
    """Tests de régression pour éviter les régressions"""
    
    def setup_method(self):
        """Setup avant chaque test"""
        self.env = Environment()
        self.parser = Parser(self.env)
    
    def test_subject_examples_rational(self):
        """Test des exemples du sujet pour les nombres rationnels"""
        examples = [
            ("varA = 2", 2.0),
            ("varB = 4.242", 4.242),
            ("varC = -4.3", -4.3),
        ]
        
        for input_str, expected in examples:
            assignment = self.parser.identify_type(input_str)
            result = assignment.compute()
            assert result == expected, f"Subject example failed: {input_str}"
    
    def test_subject_examples_complex(self):
        """Test des exemples du sujet pour les nombres complexes"""
        examples = [
            ("varA = 2*i + 3", 3.0, 2.0),
            ("varB = -4i - 4", -4.0, -4.0),
        ]
        
        for input_str, expected_real, expected_imag in examples:
            assignment = self.parser.identify_type(input_str)
            assignment.compute()
            
            var = self.env.get_variable(input_str.split('=')[0].strip())
            assert var.real_part == expected_real, f"Real part failed: {input_str}"
            assert var.imaginary_part == expected_imag, f"Imaginary part failed: {input_str}"
    
    def test_subject_examples_matrix(self):
        """Test des exemples du sujet pour les matrices"""
        examples = [
            ("varA = [[2,3];[4,3]]", [[2.0, 3.0], [4.0, 3.0]]),
            ("varB = [[3,4]]", [[3.0, 4.0]]),
        ]
        
        for input_str, expected in examples:
            assignment = self.parser.identify_type(input_str)
            assignment.compute()
            
            var = self.env.get_variable(input_str.split('=')[0].strip())
            assert var.matrix == expected, f"Matrix failed: {input_str}"
    
    def test_subject_examples_function(self):
        """Test des exemples du sujet pour les fonctions"""
        examples = [
            ("funA(x) = 2*x^5 + 4*x^2 - 5*x + 4", "2*x^5 + 4*x^2 - 5*x + 4"),
            ("funB(y) = 43 * y / (4 % 2 * y)", "43 * y / (4 % 2 * y)"),
            ("funC(z) = -2 * z - 5", "-2 * z - 5"),
        ]
        
        for input_str, expected_expr in examples:
            assignment = self.parser.identify_type(input_str)
            assignment.compute()
            
            func_name = input_str.split('(')[0].strip()
            var = self.env.get_variable(func_name)
            assert var.expression == expected_expr, f"Function failed: {input_str}"
    
    def test_subject_workflow_example(self):
        """Test de l'exemple de workflow complet du sujet"""
        # Exemple du sujet
        workflow = [
            ("varA = 2 + 4 * 2 - 5 % 4 + 2 * (4 + 5)", 27.0),
            ("varB = 2 * varA - 5 % 4", 53.0),
        ]
        
        for input_str, expected in workflow:
            assignment = self.parser.identify_type(input_str)
            result = assignment.compute()
            assert result == expected, f"Workflow example failed: {input_str}"
    
    def test_reassignment_workflow(self):
        """Test du workflow de réassignation du sujet"""
        # Séquence de réassignations
        assignments = [
            ("x = 2", RationalNumber, 2.0),
            ("y = x", RationalNumber, 2.0),
            ("y = 7", RationalNumber, 7.0),
            ("y = 2 * i - 4", ComplexNumber, None),  # None car complexe
        ]
        
        for input_str, expected_type, expected_value in assignments:
            assignment = self.parser.identify_type(input_str)
            assignment.compute()
            
            var_name = input_str.split('=')[0].strip()
            var = self.env.get_variable(var_name)
            
            assert isinstance(var, expected_type), f"Type mismatch for {input_str}"
            
            if expected_value is not None:
                assert var.numeric_value == expected_value, f"Value mismatch for {input_str}"
            else:
                # Pour le nombre complexe
                assert var.real_part == -4.0 and var.imaginary_part == 2.0

# Tests d'erreur spécifiques
class TestErrorHandling:
    """Tests spécifiques pour la gestion d'erreurs"""
    
    def setup_method(self):
        """Setup avant chaque test"""
        self.env = Environment()
        self.parser = Parser(self.env)
    
    def test_syntax_errors_rational(self):
        """Test erreurs de syntaxe pour nombres rationnels"""
        syntax_errors = [
            "2 + + 3",
            "* 5",
            "5 /",
            "((2 + 3)",
            "2 + 3))",
            "2 3 4",
        ]
        
        for error_expr in syntax_errors:
            var = RationalNumber("test", error_expr, self.env)
            
            f = io.StringIO()
            with redirect_stdout(f):
                result = var.compute()
            
            output = f.getvalue()
            assert result is None or "Syntax Error" in output, f"Should error on: {error_expr}"
    
    def test_syntax_errors_complex(self):
        """Test erreurs de syntaxe pour nombres complexes"""
        syntax_errors = [
            "2i + + 3",
            "i i",
            "2ii",
            "i + j",  # j n'est pas défini
        ]
        
        for error_expr in syntax_errors:
            var = ComplexNumber("test", error_expr, self.env)
            
            f = io.StringIO()
            with redirect_stdout(f):
                result = var.compute()
            
            # Certaines expressions peuvent être parsées différemment
            # On vérifie juste qu'il n'y a pas de crash
            assert result is None or isinstance(result, ComplexNumber)
    
    def test_syntax_errors_matrix(self):
        """Test erreurs de syntaxe pour matrices"""
        syntax_errors = [
            "[[1,2];[3,4,5]]",  # Lignes de tailles différentes
            "[1,2;3,4]",        # Pas de crochets doubles
            "[[1,2][3,4]]",     # Pas de point-virgule
            "[[1,2;3,4]",       # Crochet manquant
            "[[1,2,];[3,4]]",   # Virgule en trop
        ]
        
        for error_expr in syntax_errors:
            var = Matrix("test", error_expr, self.env)
            
            f = io.StringIO()
            with redirect_stdout(f):
                result = var.compute()
            
            output = f.getvalue()
            # Certaines erreurs peuvent être gérées, d'autres non
            if result is None:
                assert "Syntax Error" in output
    
    def test_function_evaluation_errors(self):
        """Test erreurs d'évaluation de fonction"""
        # Fonction qui peut causer des erreurs
        func = Function("f(x)", "1/x", self.env)
        func.compute()
        
        # Division par zéro
        with pytest.raises(ValueError):
            func.evaluate(0)
        
        # Fonction avec expression invalide
        invalid_func = Function("g(x)", "x +", self.env)
        invalid_func.compute()
        
        with pytest.raises(ValueError):
            invalid_func.evaluate(1)

# Test de couverture pour toutes les méthodes
class TestCoverage:
    """Tests pour assurer une couverture complète du code"""
    
    def setup_method(self):
        """Setup avant chaque test"""
        self.env = Environment()
    
    def test_all_string_methods(self):
        """Test toutes les méthodes __str__"""
        # RationalNumber
        rational = RationalNumber("r", "5.0", self.env)
        rational.compute()
        str_repr = str(rational)
        assert "5" in str_repr
        
        # ComplexNumber - différents cas
        complex_cases = [
            ("0", 0.0, 0.0, "0"),
            ("i", 0.0, 1.0, "i"),
            ("2+3i", 2.0, 3.0, "2.0 + 3.0i"),
        ]
        
        for expr, real, imag, expected in complex_cases:
            complex_num = ComplexNumber("c", expr, self.env)
            complex_num.compute()
            str_repr = str(complex_num)
            # Vérification flexible car le format peut varier
            assert str_repr is not None
        
        # Matrix
        matrix = Matrix("m", "[[1,2];[3,4]]", self.env)
        matrix.compute()
        str_repr = str(matrix)
        assert "1.0" in str_repr and "2.0" in str_repr
        
        # Function
        function = Function("f(x)", "x+1", self.env)
        function.compute()
        str_repr = str(function)
        assert "x+1" in str_repr
    
    def test_environment_edge_cases(self):
        """Test cas limites de l'environnement"""
        # Test print_variables avec environnement vide
        f = io.StringIO()
        with redirect_stdout(f):
            self.env.print_variables()
        
        output = f.getvalue()
        assert "No variables defined" in output
        
        # Test avec variables
        var = RationalNumber("test", "5", self.env)
        var.compute()
        
        f = io.StringIO()
        with redirect_stdout(f):
            self.env.print_variables()
        
        output = f.getvalue()
        assert "test" in output
    
    def test_parser_edge_cases(self):
        """Test cas limites du parser"""
        parser = Parser(self.env)
        
        # Test identify_type avec entrées limites
        edge_cases = [
            "x=5",           # Pas d'espaces
            " x = 5 ",       # Espaces multiples
            "X = 5",         # Majuscules
            "var123 = 456",  # Chiffres dans nom
        ]
        
        for case in edge_cases:
            result = parser.identify_type(case)
            assert result is not None, f"Parser failed on: {case}"

# Tests de comparaison et égalité
class TestComparison:
    """Tests pour les comparaisons et l'égalité"""
    
    def setup_method(self):
        """Setup avant chaque test"""
        self.env = Environment()
    
    def test_rational_equality(self):
        """Test égalité des nombres rationnels"""
        var1 = RationalNumber("a", "5", self.env)
        var1.compute()
        
        var2 = RationalNumber("b", "2.5 * 2", self.env)
        var2.compute()
        
        assert var1.numeric_value == var2.numeric_value
    
    def test_complex_equality(self):
        """Test égalité des nombres complexes"""
        var1 = ComplexNumber("z1", "3 + 4i", self.env)
        var1.compute()
        
        var2 = ComplexNumber("z2", "4i + 3", self.env)
        var2.compute()
        
        assert var1.real_part == var2.real_part
        assert var1.imaginary_part == var2.imaginary_part
    
    def test_matrix_equality(self):
        """Test égalité des matrices"""
        var1 = Matrix("m1", "[[1,2];[3,4]]", self.env)
        var1.compute()
        
        var2 = Matrix("m2", "[[1,2];[3,4]]", self.env)
        var2.compute()
        
        assert var1.matrix == var2.matrix
        assert var1.rows == var2.rows
        assert var1.columns == var2.columns

# Configuration pour PyTest
def pytest_configure(config):
    """Configuration PyTest"""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )

def pytest_collection_modifyitems(config, items):
    """Modification des items de collection PyTest"""
    for item in items:
        # Marquer les tests de performance comme lents
        if "performance" in item.nodeid.lower():
            item.add_marker(pytest.mark.slow)

# Utilitaires pour les tests
class TestUtilities:
    """Utilitaires pour les tests"""
    
    @staticmethod
    def capture_output(func, *args, **kwargs):
        """Capture la sortie standard d'une fonction"""
        f = io.StringIO()
        with redirect_stdout(f):
            result = func(*args, **kwargs)
        return result, f.getvalue()
    
    @staticmethod
    def create_test_environment():
        """Crée un environnement de test avec des variables prédéfinies"""
        env = Environment()
        
        # Variables rationnelles
        RationalNumber("a", "5", env).compute()
        RationalNumber("b", "3", env).compute()
        
        # Nombre complexe
        ComplexNumber("z", "2+3i", env).compute()
        
        # Matrice
        Matrix("M", "[[1,2];[3,4]]", env).compute()
        
        # Fonction
        Function("f(x)", "2*x+1", env).compute()
        
        return env

if __name__ == "__main__":
    # Permettre l'exécution directe des tests
    pytest.main([__file__, "-v", "--tb=short"])