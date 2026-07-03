import string
import secrets
import sys

def print_banner():
    banner = """
    ╔══════════════════════════════════════════════════════╗
    ║                ⚡ PASSWORD GENERATOR ⚡               ║
    ║             Interactive Command Line Mode            ║
    ╚══════════════════════════════════════════════════════╝
    """
    print(banner)

def get_boolean_input(prompt_text):
    """Prompt the user for y/n response. Returns bool."""
    while True:
        choice = input(prompt_text).strip().lower()
        if choice in ['y', 'yes', '']:
            return True
        if choice in ['n', 'no']:
            return False
        if choice in ['q', 'exit', 'quit']:
            print("\nExiting. Thank you for using Password Generator!")
            sys.exit(0)
        print("❌ Invalid input! Please enter 'y' for Yes or 'n' for No.")

def generate_secure_password(length, use_upper, use_lower, use_digits, use_symbols):
    """Generates a secure password based on specified criteria."""
    # Define character pools
    upper_chars = string.ascii_uppercase
    lower_chars = string.ascii_lowercase
    digit_chars = string.digits
    symbol_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"

    character_pool = ""
    guaranteed_chars = []

    # Build character pools and add guaranteed chars to ensure complexity is met
    if use_upper:
        character_pool += upper_chars
        guaranteed_chars.append(secrets.choice(upper_chars))
    if use_lower:
        character_pool += lower_chars
        guaranteed_chars.append(secrets.choice(lower_chars))
    if use_digits:
        character_pool += digit_chars
        guaranteed_chars.append(secrets.choice(digit_chars))
    if use_symbols:
        character_pool += symbol_chars
        guaranteed_chars.append(secrets.choice(symbol_chars))

    if not character_pool:
        raise ValueError("At least one character set must be selected!")

    # Calculate remaining length
    remaining_length = length - len(guaranteed_chars)
    
    if remaining_length < 0:
        # If length is smaller than number of selected categories, truncate guaranteed chars
        guaranteed_chars = guaranteed_chars[:length]
        remaining_length = 0

    # Fill remainder randomly from the combined pool
    random_chars = [secrets.choice(character_pool) for _ in range(remaining_length)]
    
    # Combine and shuffle securely
    final_list = guaranteed_chars + random_chars
    secrets.SystemRandom().shuffle(final_list)

    return "".join(final_list)

def run_cli_generator():
    print_banner()
    print("Type 'q' or 'exit' at any prompt to quit.\n")

    while True:
        # Prompt for length
        while True:
            len_input = input("Enter the desired password length (minimum 4): ").strip()
            if len_input.lower() in ['q', 'exit', 'quit']:
                print("\nExiting. Thank you for using Password Generator!")
                sys.exit(0)
            try:
                length = int(len_input)
                if length < 4:
                    print("❌ Length must be at least 4 for basic complexity!")
                    continue
                if length > 256:
                    print("❌ Length cannot exceed 256 characters!")
                    continue
                break
            except ValueError:
                print("❌ Invalid input! Please enter a valid integer.")

        # Prompt for complexity
        print("\nSpecify password complexity parameters:")
        use_upper = get_boolean_input("Include Uppercase letters (A-Z)? [Y/n]: ")
        use_lower = get_boolean_input("Include Lowercase letters (a-z)? [Y/n]: ")
        use_digits = get_boolean_input("Include Numbers (0-9)? [Y/n]: ")
        use_symbols = get_boolean_input("Include Special Symbols (!@#$ etc)? [Y/n]: ")

        # Validate that at least one is selected
        if not (use_upper or use_lower or use_digits or use_symbols):
            print("\n❌ Error: You must select at least one character set! Let's try again.\n")
            continue

        # Generate password
        try:
            password = generate_secure_password(length, use_upper, use_lower, use_digits, use_symbols)
            
            # Display password
            print("\n" + "═"*54)
            print("  🔑 GENERATED SECURE PASSWORD:")
            print(f"  {password}")
            print("═"*54 + "\n")
        except Exception as e:
            print(f"\n❌ Error generating password: {e}\n")

        # Ask to generate another
        again = input("Do you want to generate another password? (y/n): ").strip().lower()
        if again not in ['y', 'yes']:
            print("\nExiting. Thank you for using Password Generator!")
            break

if __name__ == "__main__":
    try:
        run_cli_generator()
    except KeyboardInterrupt:
        print("\n\nProgram interrupted. Goodbye!")
        sys.exit(0)
