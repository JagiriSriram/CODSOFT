import random
import sys

def print_banner():
    banner = """
    ╔══════════════════════════════════════════════════════╗
    ║             ✊ ROCK - ✋ PAPER - ✌️ SCISSORS          ║
    ║             Interactive Command Line Mode            ║
    ╚══════════════════════════════════════════════════════╝
    """
    print(banner)

def get_user_choice():
    """Prompts the user to make a valid game choice."""
    weapons = {
        '1': 'rock',
        '2': 'paper',
        '3': 'scissors'
    }
    
    print("\nSelect your weapon:")
    print("  [1] Rock (✊)")
    print("  [2] Paper (✋)")
    print("  [3] Scissors (✌️)")
    print("  [Q] Quit Game")
    
    while True:
        choice = input("\nEnter your choice (1, 2, 3 or Q): ").strip().lower()
        if choice in ['q', 'quit', 'exit']:
            return 'quit'
        if choice in weapons:
            return weapons[choice]
        print("❌ Invalid input! Please select 1, 2, 3, or type Q to exit.")

def get_computer_choice():
    """Generates a random choice for the computer."""
    return random.choice(['rock', 'paper', 'scissors'])

def determine_winner(player, computer):
    """
    Returns the result string from the player's perspective:
    'win', 'lose', or 'tie'
    """
    if player == computer:
        return 'tie'
        
    # Win conditions
    if (player == 'rock' and computer == 'scissors') or \
       (player == 'scissors' and computer == 'paper') or \
       (player == 'paper' and computer == 'rock'):
        return 'win'
        
    return 'lose'

def run_cli_game():
    print_banner()
    print("Type 'q' or 'exit' at the selection prompt to quit.\n")

    # Score Counters
    player_score = 0
    computer_score = 0
    ties = 0

    emoji_map = {
        'rock': '✊',
        'paper': '✋',
        'scissors': '✌️'
    }

    while True:
        player_choice = get_user_choice()
        if player_choice == 'quit':
            print(f"\nFinal Scores | Player: {player_score}  Computer: {computer_score}  Ties: {ties}")
            print("Thank you for playing Rock-Paper-Scissors!")
            break

        computer_choice = get_computer_choice()
        result = determine_winner(player_choice, computer_choice)

        # Update Scores
        if result == 'win':
            player_score += 1
            result_text = "🎉 YOU WIN!"
        elif result == 'lose':
            computer_score += 1
            result_text = "😢 COMPUTER WINS!"
        else:
            ties += 1
            result_text = "🤝 IT'S A TIE!"

        # Display result framed nicely
        p_weapon = f"{player_choice.upper()} ({emoji_map[player_choice]})"
        c_weapon = f"{computer_choice.upper()} ({emoji_map[computer_choice]})"
        
        print("\n" + "═"*54)
        print("  ROUND RESULTS:")
        print(f"  🧑 Player Choice:   {p_weapon}")
        print(f"  🤖 Computer Choice: {c_weapon}")
        print(f"  👉 OUTCOME:         {result_text}")
        print("═"*54)
        print(f"  🏆 Scoreboard | Player: {player_score} | Computer: {computer_score} | Ties: {ties}")
        print("═"*54 + "\n")

        # Prompt to continue
        again = input("Do you want to play another round? (y/n): ").strip().lower()
        if again not in ['y', 'yes', '']:
            print(f"\nFinal Scores | Player: {player_score}  Computer: {computer_score}  Ties: {ties}")
            print("Thank you for playing Rock-Paper-Scissors!")
            break

if __name__ == "__main__":
    try:
        run_cli_game()
    except KeyboardInterrupt:
        print("\n\nGame interrupted. Goodbye!")
        sys.exit(0)
