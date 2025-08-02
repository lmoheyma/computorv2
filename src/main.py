from environment.Environment import Environment
from parsing.Parser import Parser

def main():
    """Fonction principale du programme"""
    environment = Environment()
    parser = Parser(environment)

    print("Computor v2")
    print("Enter 'exit' to quit, 'var' to show variables")

    while True:
        try:
            user_input = input("> ")

            # Commandes spéciales
            if user_input.lower() in ['exit', 'quit']:
                break
            elif user_input.lower() == 'var':
                environment.print_variables()
                continue
            elif not user_input.strip():
                continue

            # Préprocessing
            processed_input = parser.preprocess(user_input)
            if not processed_input:
                print("Syntax Error")
                continue

            # Identification du type et calcul
            assignment = parser.identify_type(processed_input)
            if assignment:
                assignment.compute()

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except EOFError:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()