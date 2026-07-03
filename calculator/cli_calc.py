import sys

def print_banner():
    banner = """
    ╔══════════════════════════════════════════════════════╗
    ║                     ⚡ CALCULATOR ⚡                 ║
    ║             Interactive Command Line Mode            ║
    ╚══════════════════════════════════════════════════════╝
    """
    print(banner)

def get_number_input(prompt_text):
    """Prompts the user for a valid number. Allows typing 'q' or 'exit' to quit."""
    while True:
        try:
            val = input(prompt_text).strip()
            if val.lower() in ['q', 'exit', 'quit']:
                print("\nExiting Calculator. Thank you for using TaskFlow!")
                sys.exit(0)
            return float(val)
        except ValueError:
            print("❌ Invalid input! Please enter a valid number (e.g. 10, -5.5) or type 'q' to quit.")

def get_operator_input():
    """Prompts the user to select an arithmetic operator."""
    valid_ops = {
        '+': "Addition",
        '-': "Subtraction",
        '*': "Multiplication",
        '/': "Division",
        '%': "Modulo",
        '^': "Power"
    }
    
    print("\nAvailable Operations:")
    for op, desc in valid_ops.items():
        print(f"  [{op}] {desc}")
        
    while True:
        op = input("\nEnter your operation choice: ").strip()
        if op.lower() in ['q', 'exit', 'quit']:
            print("\nExiting Calculator. Thank you for using TaskFlow!")
            sys.exit(0)
        if op in valid_ops:
            return op
        print(f"❌ Invalid choice! Please enter one of: {', '.join(valid_ops.keys())}")

def run_cli_calculator():
    print_banner()
    print("Type 'q' or 'exit' at any prompt to quit.\n")

    while True:
        num1 = get_number_input("Enter the first number: ")
        num2 = get_number_input("Enter the second number: ")
        operator = get_operator_input()

        result = None
        error_msg = None

        # Perform Calculation
        try:
            if operator == '+':
                result = num1 + num2
            elif operator == '-':
                result = num1 - num2
            elif operator == '*':
                result = num1 * num2
            elif operator == '/':
                if num2 == 0:
                    error_msg = "Division by zero is undefined!"
                else:
                    result = num1 / num2
            elif operator == '%':
                if num2 == 0:
                    error_msg = "Modulo by zero is undefined!"
                else:
                    result = num1 % num2
            elif operator == '^':
                # Avoid complex math domains (huge numbers)
                if num1 == 0 and num2 < 0:
                    error_msg = "Zero raised to a negative power is undefined!"
                elif abs(num2) > 1000:
                    error_msg = "Exponent too large to prevent overflow!"
                else:
                    result = num1 ** num2
        except OverflowError:
            error_msg = "Result is too large (Overflow error)!"
        except Exception as e:
            error_msg = f"Mathematical error: {str(e)}"

        # Display Result
        print("\n" + "═"*54)
        if error_msg:
            print(f"  ❌ ERROR: {error_msg}")
        else:
            # Format floating points cleanly (remove trailing .0 for integers)
            num1_str = f"{int(num1)}" if num1.is_integer() else f"{num1}"
            num2_str = f"{int(num2)}" if num2.is_integer() else f"{num2}"
            
            # Format result
            if isinstance(result, float) and result.is_integer():
                result_str = f"{int(result)}"
            elif isinstance(result, float):
                # Clean rendering up to 6 decimals
                result_str = f"{result:.6f}".rstrip('0').rstrip('.')
            else:
                result_str = f"{result}"
                
            print(f"  📝 RESULT:  {num1_str} {operator} {num2_str} = {result_str}")
        print("═"*54 + "\n")

        # Ask to continue
        again = input("Do you want to perform another calculation? (y/n): ").strip().lower()
        if again not in ['y', 'yes']:
            print("\nExiting Calculator. Thank you for using TaskFlow!")
            break

if __name__ == "__main__":
    try:
        run_cli_calculator()
    except KeyboardInterrupt:
        print("\n\nCalculator interrupted. Goodbye!")
        sys.exit(0)
