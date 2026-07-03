import sys
import argparse
import tkinter as tk

def main():
    parser = argparse.ArgumentParser(description="Rock-Paper-Scissors Game - Multi-Mode CLI/GUI")
    parser.add_argument("--cli", action="store_true", help="Launch in command-line CLI mode")
    args = parser.parse_args()

    if args.cli:
        from cli_game import run_cli_game
        try:
            run_cli_game()
        except KeyboardInterrupt:
            print("\nGame closed. Goodbye!")
            sys.exit(0)
    else:
        # Default desktop Tkinter GUI launching
        from gui_game import GUIGame
        try:
            root = tk.Tk()
            app = GUIGame(root)
            app.pack(fill="both", expand=True)
            root.mainloop()
        except Exception as e:
            print(f"❌ Error launching GUI Mode: {e}")
            print("Falling back to CLI Mode...\n")
            from cli_game import run_cli_game
            run_cli_game()

if __name__ == "__main__":
    main()
