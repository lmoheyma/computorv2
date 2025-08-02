# Computor v2 🧮

> "Your homemade basic calculator"

Un interpréteur mathématique avancé qui gère les nombres rationnels, complexes, matrices et fonctions avec un système de variables dynamique.

## 📋 Table des matières

- [Description](#description)
- [Fonctionnalités](#fonctionnalités)
- [Installation](#installation)
- [Utilisation](#utilisation)
- [Types supportés](#types-supportés)
- [Opérateurs](#opérateurs)
- [Exemples](#exemples)
- [Commandes spéciales](#commandes-spéciales)
- [Architecture](#architecture)
- [Auteur](#auteur)

## 📖 Description

Computor v2 est un calculateur interactif similaire à `bc` qui permet de :
- Assigner des variables de différents types mathématiques
- Effectuer des calculs complexes avec gestion des priorités
- Définir et utiliser des fonctions mathématiques
- Manipuler des matrices et nombres complexes
- Résoudre des équations polynomiales de degré ≤ 2

## ✨ Fonctionnalités

### Types de données supportés
- **Nombres rationnels** (ℚ) : `2`, `4.242`, `-4.3`
- **Nombres complexes** (ℂ) : `2*i + 3`, `-4i - 4`, `i`
- **Matrices** (Mn,p(ℚ)) : `[[2,3];[4,3]]`, `[[1,2,3]]`
- **Fonctions** : `f(x) = 2*x^2 + 3*x - 1`

### Opérations avancées
- Assignation et réassignation de variables
- Calcul d'expressions avec variables
- Évaluation de fonctions
- Gestion des priorités opératoires
- Variables insensibles à la casse

## 🚀 Installation

```bash
# Cloner le repository
git clone git@github.com:lmoheyma/computorv2.git
cd computorv2

# Exécuter le programme
python3 src/main.py
```

### Prérequis :

- Python 3.6+
- Aucune dépendance externe

## 💻 Utilisation

### Lancement

```bash
$ python3 src/main.py
Computor v2
Enter 'exit' to quit, 'var' to show variables
>
```

### Syntaxe générale

```
variable = expression
expression = ?
function(variable) = expression
```

## 🔢 Types supportés

### 1. Nombres rationnels

```bash
> varA = 2
2
> varB = 4.242
4.242
> varC = -4.3
-4.3
> result = varA + varB * 2 - 5
5.484
```

### 2. Nombres complexes

```bash
> complexA = 2*i + 3
3 + 2i
> complexB = -4i - 4
-4 - 4i
> complexC = i
i
> sum = complexA + complexB
-1 - 2i
```

### 3. Matrices

```bash
> matA = [[2,3];[4,3]]
[ 2 , 3 ]
[ 4 , 3 ]
> matB = [[1,2,3]]
[ 1 , 2 , 3 ]
> matC = [[1];[2];[3]]
[ 1 ]
[ 2 ]
[ 3 ]
```

### 4. Fonctions

```bash
> funA(x) = 2*x^5 + 4*x^2 - 5*x + 4
2*x^5 + 4*x^2 - 5*x + 4
> funB(y) = 43 * y / (4 % 2 * y)
43 * y / (4 % 2 * y)
> funC(z) = -2 * z - 5
-2 * z - 5
```

## ⚡ Opérateurs

### Opérateurs arithmétiques

- ```+``` : Addition
- ```-``` : Soustraction
- ```*``` : Multiplication
- ```/``` : Division
- ```%``` : Modulo
- ```^``` : Puissance
- ```**``` : Multiplication matricielle (bonus)

### Opérateurs spéciaux

- ```=``` : Assignation
- ```?``` : Calcul/Évaluation
- ```()``` : Parenthèses (priorités)

## 📝 Exemples

### Assignation et calcul

```bash
> x = 5
5
> y = x * 2 + 3
13
> result = x + y
18
> result = ?
18
```

### Réassignation avec changement de type

```bash
> x = 2
2
> y = x
2
> y = 7
7
> y = 2 * i - 4
-4 + 2i
```

### Calculs avec fonctions

```bash
> funA(x) = 2 * x + 1
2 * x + 1
> funA(5) = ?
11
> funB(x) = x^2 - 4*x + 4
x^2 - 4*x + 4
> funB(2) = ?
0
```

### Expressions complexes

```bash
> varA = 2 + 4 * 2 - 5 % 4 + 2 * (4 + 5)
27
> varB = 2 * varA - 5 % 4
53
> funA(x) = varA + varB * 4 - 1 / 2 + x
238.5 + x
> varC = 2 * varA - varB
1
> varD = funA(varC)
239.5
```

## 🛠️ Commandes spéciales

- ```var``` : Affiche toutes les variables stockées
- ```exit``` ou ```quit``` : Quitte le programme
- ```Ctrl+C``` : Interruption gracieuse

```bash
> var
Variable: x | Value: 5 | Type: RationalNumber
Variable: complexA | Value: 3 + 2i | Type: ComplexNumber
Variable: matA | Value: [ 2 , 3 ]
[ 4 , 3 ] | Type: Matrix
Variable: funA | Value: 2*x + 1 | Type: Function

> exit
Goodbye!
```

## 🏗️ Architecture

### Structure du projet

```
computor-v2/
├── src
|   ├── environment
|   │   └── Environment.py             # Environnement (variables)
|   ├── parsing
|   │   └── Parser.py                  # Parsing de l'input
|   ├── var_types
|   |   ├── BaseAssignmentValue.py     # Classe abstraite pour tous les types
|   |   ├── ComplexNumber.py           # Nombres complexes
|   |   ├── Function.py                # Fonctions
|   |   ├── Matrix.py                  # Matrices
|   |   └── RationalNumber.py          # Nombre rationel
|   └── main.py                        # Point d'entrée principal
└── README.md                          # Documentation

```

### Classes principales

- ``BaseAssignmentValue`` : Classe abstraite de base
- ``RationalNumber`` : Gestion des nombres rationnels
- ``ComplexNumber`` : Gestion des nombres complexes
- ``Matrix`` : Gestion des matrices
- ``Function`` : Gestion des fonctions
- ``Environment`` : Environnement des variables
- ``Parser`` : Analyseur syntaxique

### Fonctionnalités techniques

- **Parsing intelligent** : Identification automatique des types
- **Expansion des variables** : Substitution automatique dans les expressions
- **Gestion d'erreurs** : Messages d'erreur appropriés
- **Interface interactive** : REPL (Read-Eval-Print Loop)
- **Insensibilité à la casse** : ``varA`` équivaut à ``vara``

## 🔧 Spécifications techniques

### Contraintes respectées

- ✅ Pas de types natifs pour les nombres complexes
- ✅ Pas de bibliothèques externes pour matrices/complexes
- ✅ Variables insensibles à la casse
- ✅ Variable ``i`` réservée pour les nombres complexes
- ✅ Simplification des expressions quand possible
- ✅ Affichage cohérent et formaté

### Priorités opératoires

1. Parenthèses ``()``
2. Puissances ``^``
3. Multiplication/Division ``*``, ``/``, ``%``
4. Addition/Soustraction ``+``, ``-``

## 🐛 Gestion d'erreurs

Le programme gère élégamment les erreurs courantes :
- Syntaxe invalide
- Variables non définies
- Expressions mal formées
- Divisions par zéro
- Types incompatibles

```bash
> invalid syntax here
Syntax Error

> undefinedVar = ?
Variable not found

> 5 / 0 = ?
Syntax Error
```

## 🧪 Tests

```bash
# Test nombres rationnels
> a = 2 * 4 + 4
12
> a + 2 = ?
14

# Test nombres complexes
> c = 3 + 4i
3 + 4i
> c2 = -2i + 1
1 - 2i

# Test matrices
> m = [[1,2];[3,4]]
[ 1 , 2 ]
[ 3 , 4 ]

# Test fonctions
> f(x) = x^2 + 1
x^2 + 1
> f(3) = ?
10
```
