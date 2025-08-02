from typing import Dict, Optional
from var_types.BaseAssignmentValue import BaseAssignmentValue

class Environment:
    """Gère l'environnement des variables et fonctions"""
    def __init__(self) -> None:
        self.variables: Dict[str, BaseAssignmentValue] = {}
    
    def get_variable(self, name: str) -> Optional[BaseAssignmentValue]:
        """Récupère une variable par son nom (insensible à la casse)"""
        name_lower = name.lower()
        for var_name, var in self.variables.items():
            if var_name.lower() == name_lower:
                return var
        return None

    def set_variable(self, variable: BaseAssignmentValue) -> None:
        """Ajoute ou met à jour une variable"""
        if variable.name.lower() == 'i':
            print("'i' is not a valid variable name")
            return
        
        existing_key = None
        for key in self.variables.keys():
            if key.lower() == variable.name.lower():
                existing_key = key
                break
        
        if existing_key:
            self.variables[existing_key] = variable
        else:
            self.variables[variable.name] = variable
        
        print(f"{variable}")

    def print_variables(self) -> None:
        """Affiche toutes les variables"""
        if not self.variables:
            print("No variables defined")
            return
        
        for name, var in self.variables.items():
            print(f"Variable: {name} | Value: {var} | Type: {type(var).__name__}")